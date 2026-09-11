import logging
import threading
import time
from math import radians, sin, cos, sqrt, atan2

import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from logistics.permissions.logistics_owner_permissions import IsRider
import os

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# GPS QUALITY CONFIGURATION
# ---------------------------------------------------------

# Only GPS readings with an estimated accuracy at or below
# this value are allowed to update the live rider position.
#
# This is deliberately configurable. Tune this with real
# outdoor TrackerrGo testing.
MAX_BROADCAST_ACCURACY = 50.0  # metres


# This is NOT a normal driving speed limit.
#
# It exists only to catch obviously corrupted GPS jumps.
# 80 m/s = 288 km/h.
MAX_IMPLAUSIBLE_SPEED = 80.0  # metres / second


# How long the last trusted location should remain in Redis.
LOCATION_CACHE_TIMEOUT = 120


# ---------------------------------------------------------
# MAP MATCHING CONFIGURATION
# ---------------------------------------------------------

# Number of accepted fixes to accumulate before calling Mapbox
# Map Matching. Mapbox snaps noisy raw GPS onto the actual road
# network, which is what was causing the rider marker to drift
# off-route / onto buildings when raw points were broadcast directly.
MAP_MATCHING_BATCH_SIZE = 5

MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN", None)

MAP_MATCHING_URL = "https://api.mapbox.com/matching/v5/mapbox/driving/{coordinates}"

# The buffer for an in-progress batch shouldn't outlive a short GPS gap —
# if the rider's connection drops mid-batch, we don't want stale points
# from before the gap silently combined with fresh ones after it.
MATCH_BUFFER_TTL = 60  # seconds

MAP_MATCHING_TIMEOUT_S = 5

# When replaying a matched batch to the frontend, space broadcasts out to
# roughly match the real gap between the original GPS fixes (derived from
# their timestamps) rather than firing all N points back-to-back. Clamped
# so one weirdly-large gap in the raw data can't stall playback, and one
# near-zero gap can't still slip past the frontend's WS_THROTTLE_MS.
MIN_REPLAY_GAP_S = 0.3
MAX_REPLAY_GAP_S = 4.0

# Resample the matched road geometry into points roughly this far apart,
# so the frontend animates through a smooth run of real road positions
# instead of jumping between the batch's original 5 fixes.
DENSIFY_STEP_M = 15

# Reported accuracy for a map-matched (road-snapped) point — these are no
# longer raw GPS, they're Mapbox's best estimate of where on the road
# network the rider actually was, so a small fixed value is more honest
# than reusing the original device accuracy.
MATCHED_POINT_ACCURACY_M = 5.0


def haversine_distance(lat1, lng1, lat2, lng2):
    """
    Calculate distance between two coordinates in metres.
    """

    earth_radius = 6371000.0

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    delta_lat = radians(lat2 - lat1)
    delta_lng = radians(lng2 - lng1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lng / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


# ---------------------------------------------------------
# MAP-MATCHING BUFFER HELPERS
# ---------------------------------------------------------

# ---------------------------------------------------------
# MAP-MATCHING BUFFER HELPERS
# ---------------------------------------------------------
#
# django.core.cache only exposes get/set/delete — there's no atomic
# "append to a list" primitive the way a native Redis client would give
# you (RPUSH). So the buffer is kept as a single JSON-serializable list
# under one cache key, using read-modify-write on each accepted fix.
#
# This is safe here because a single rider's mobile app posts its own
# location updates sequentially — there's no scenario where two of that
# rider's requests are in flight at once, so the lack of atomicity isn't
# a practical risk. (If that assumption ever changes — e.g. multiple
# devices posting under one rider — this would need a proper lock.)

def _match_buffer_key(rider_id):
    return f"rider_{rider_id}_matchbuffer"


def _push_to_match_buffer(rider_id, lat, lng, accuracy, timestamp_ms, speed, heading):
    """Appends one accepted fix to the rider's buffer and returns the new
    buffer length."""
    key = _match_buffer_key(rider_id)
    buffer = cache.get(key) or []

    buffer.append({
        "lat": lat,
        "lng": lng,
        "accuracy": accuracy,
        "timestamp": timestamp_ms,
        "speed": speed,
        "heading": heading,
    })

    cache.set(key, buffer, timeout=MATCH_BUFFER_TTL)
    return len(buffer)


def _pop_match_buffer(rider_id):
    """Reads the full batch and clears the buffer. Also builds the exact
    coordinate/radius/timestamp string formats Mapbox Map Matching's
    request expects, from the buffered points."""
    key = _match_buffer_key(rider_id)
    meta = cache.get(key) or []
    cache.delete(key)

    coords = [f"{point['lng']},{point['lat']}" for point in meta]
    radii = [f"{point['accuracy']:.1f}" for point in meta]
    timestamps = [str(int(point["timestamp"] / 1000)) for point in meta]

    return coords, radii, timestamps, meta


def _request_map_matching(coords, radii, timestamps):
    """
    Calls Mapbox Map Matching for a batch of coordinates.

    Returns the parsed response dict on success, or None on any failure
    (network error, non-2xx, or Mapbox returning a non-"Ok" code) so the
    caller can fall back to broadcasting raw points instead of dropping
    the batch entirely.
    """
    if not MAPBOX_ACCESS_TOKEN:
        logger.error("MAPBOX_ACCESS_TOKEN is not configured — skipping map matching.")
        return None

    coordinates_path = ";".join(coords)
    url = MAP_MATCHING_URL.format(coordinates=coordinates_path)

    params = {
        "geometries": "geojson",
        "radiuses": ";".join(radii),
        "timestamps": ";".join(timestamps),
        "tidy": "true",
        "access_token": MAPBOX_ACCESS_TOKEN,
    }

    try:
        resp = requests.get(url, params=params, timeout=MAP_MATCHING_TIMEOUT_S)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        logger.error("Map matching request failed: %s", exc)
        return None
    except ValueError:
        logger.error("Map matching returned non-JSON response.")
        return None

    if data.get("code") != "Ok":
        logger.warning("Map matching returned code=%s", data.get("code"))
        return None

    return data


def _broadcast_point(channel_layer, group_name, lat, lng, accuracy, timestamp_ms, speed, heading):
    """
    Sends one location update in the exact shape already consumed by the
    existing Channels consumer / frontend — unchanged from the original
    broadcast payload, just now potentially carrying a map-matched
    lat/lng instead of the raw GPS fix.
    """
    broadcast = {
        "type": "rider_location_update",

        "lat": lat,
        "lng": lng,

        "accuracy": accuracy,
        "timestamp": timestamp_ms,

        "speed": speed,
        "heading": heading,
    }

    async_to_sync(channel_layer.group_send)(group_name, broadcast)


def _densify_matched_geometry(geometry_coords, start_ts_ms, end_ts_ms, step_m=DENSIFY_STEP_M):
    """
    Resamples a Map Matching LineString into evenly-spaced points, so the
    frontend gets a smooth run of positions to animate through instead of
    just the batch's original 5 fixes.

    This is safe in a way that interpolating the *raw* GPS input before
    matching is not: `geometry_coords` already came back from Mapbox as
    the real road-following path (every curve, turn, one-way street it
    knows about) between the matched points. Resampling it doesn't invent
    anything — it just adds more points along a path Mapbox already
    computed, rather than guessing a straight line and hoping the road
    agrees.

    Synthetic timestamps are distributed proportionally to distance
    traveled along the path (not point index), so a point twice as far
    along gets roughly twice the elapsed time — a reasonable
    constant-speed assumption within one short (~15s) batch.
    """
    path = [{"lat": lat, "lng": lng} for lng, lat in geometry_coords]

    if len(path) < 2:
        return [dict(path[0], timestamp=start_ts_ms)] if path else []

    cum_dist = [0.0]
    for a, b in zip(path, path[1:]):
        cum_dist.append(cum_dist[-1] + haversine_distance(a["lat"], a["lng"], b["lat"], b["lng"]))
    total_dist = cum_dist[-1]

    if total_dist == 0:
        return [dict(path[0], timestamp=start_ts_ms)]

    resampled = [path[0]]
    for a, b, d0, d1 in zip(path, path[1:], cum_dist, cum_dist[1:]):
        seg_len = d1 - d0
        if seg_len <= 0:
            continue
        steps = max(1, round(seg_len / step_m))
        for s in range(1, steps + 1):
            t = s / steps
            resampled.append({
                "lat": a["lat"] + (b["lat"] - a["lat"]) * t,
                "lng": a["lng"] + (b["lng"] - a["lng"]) * t,
            })

    out = [dict(resampled[0], timestamp=start_ts_ms)]
    running = 0.0
    prev = resampled[0]
    for point in resampled[1:]:
        running += haversine_distance(prev["lat"], prev["lng"], point["lat"], point["lng"])
        frac = running / total_dist
        out.append(dict(point, timestamp=start_ts_ms + frac * (end_ts_ms - start_ts_ms)))
        prev = point

    return out


def _densify_raw_points(meta, step_m=DENSIFY_STEP_M):
    """
    Naive straight-line interpolation between raw fixes. Used ONLY as a
    last-resort fallback when Map Matching itself failed and there's no
    road-accurate geometry to resample instead.

    Unlike _densify_matched_geometry, this CAN cut corners on a curved
    road — it's exactly the kind of guess we avoid feeding into Map
    Matching itself. It's acceptable here only because this whole branch
    is already a degraded fallback (unsnapped raw GPS), not the normal
    path, and something road-shaped-ish beats one big jump across 5
    unmatched points.
    """
    if len(meta) < 2:
        return meta

    out = [meta[0]]
    for a, b in zip(meta, meta[1:]):
        dist = haversine_distance(a["lat"], a["lng"], b["lat"], b["lng"])
        steps = max(1, round(dist / step_m))
        for s in range(1, steps + 1):
            t = s / steps
            out.append({
                "lat": a["lat"] + (b["lat"] - a["lat"]) * t,
                "lng": a["lng"] + (b["lng"] - a["lng"]) * t,
                "timestamp": a["timestamp"] + (b["timestamp"] - a["timestamp"]) * t,
                "accuracy": max(a["accuracy"], b["accuracy"]),
                "speed": b["speed"],
                "heading": b["heading"],
            })
    return out


def _dispatch_paced_broadcast(channel_layer, group_name, points):
    """
    Broadcasts a batch's points spaced out to match the real-world time
    gaps between the original GPS fixes, instead of firing all of them
    back-to-back (which would blow straight through the frontend's
    WS_THROTTLE_MS and make the rider appear to teleport across the
    whole batch in under a second).

    Runs on a background thread so the HTTP request that triggered this
    batch can return immediately rather than blocking a web worker on
    time.sleep() for the ~batch-duration of the replay.

    NOTE: this is a lightweight stopgap, not a production job queue. A
    thread per batch works for moderate rider counts, but has no retry,
    no monitoring, and (since threads aren't shared across worker
    processes) no cross-process ordering guarantee if this rider's next
    batch fills and starts replaying before this one finishes. If you
    already run Celery/RQ/Huey elsewhere, moving this into a proper task
    (ideally one queue per rider, so batches replay strictly in order)
    is the more robust long-term fix.
    """

    def _run():
        prev_ts = None
        for lat, lng, point in points:
            if prev_ts is not None:
                gap_s = (point["timestamp"] - prev_ts) / 1000.0
                gap_s = max(MIN_REPLAY_GAP_S, min(gap_s, MAX_REPLAY_GAP_S))
                time.sleep(gap_s)
            prev_ts = point["timestamp"]

            _broadcast_point(
                channel_layer, group_name,
                lat, lng,
                point["accuracy"], point["timestamp"],
                point["speed"], point["heading"],
            )

    threading.Thread(target=_run, daemon=True).start()


def _match_and_broadcast_batch(channel_layer, group_name, coords, radii, timestamps, meta):
    """
    Runs the batch through Mapbox Map Matching, densifies the result into
    a smooth run of points, and hands them to a paced background
    broadcast.

    On success: resamples the matched road geometry (real curves and
    turns, not a guess) into ~15m-spaced points spanning the batch's
    actual elapsed time, so the frontend animates through many small
    steps instead of jumping between 5 sparse ones.

    On matching failure: falls back to naive straight-line interpolation
    between the raw points instead of dropping the whole batch silently —
    less accurate on a curved road, but still better than the frontend
    going quiet or jumping across the whole batch at once.
    """
    result = _request_map_matching(coords, radii, timestamps)
    start_ts = meta[0]["timestamp"]
    end_ts = meta[-1]["timestamp"]

    if result is None:
        logger.warning(
            "Map matching unavailable for batch of %d — using raw interpolation fallback.",
            len(meta),
        )
        densified = _densify_raw_points(meta)
        points = [
            (p["lat"], p["lng"], p)
            for p in densified
        ]
        outcome = "raw_fallback"
    else:
        matching = result["matchings"][0]
        geometry_coords = matching["geometry"]["coordinates"]  # [[lng, lat], ...]

        densified = _densify_matched_geometry(geometry_coords, start_ts, end_ts)
        points = [
            (
                p["lat"], p["lng"],
                {
                    "accuracy": MATCHED_POINT_ACCURACY_M,
                    "timestamp": p["timestamp"],
                    "speed": None,
                    "heading": None,
                },
            )
            for p in densified
        ]
        outcome = "matched"

    _dispatch_paced_broadcast(channel_layer, group_name, points)
    return outcome


class BroadcastLocation(APIView):
    """
    Receives a GPS reading from TrackerrGo.

    Responsibilities:
        1. Validate the GPS payload.
        2. Reject poor-quality GPS readings.
        3. Reject stale readings.
        4. Reject obviously impossible GPS jumps.
        5. Cache the last trusted location.
        6. Buffer trusted readings in Redis in Mapbox Map Matching's
           expected coordinate-string format.
        7. Once MAP_MATCHING_BATCH_SIZE readings are buffered, send them
           to Mapbox Map Matching and broadcast the (snapped) result.

    This endpoint does NOT:
        - calculate routes
        - perform rerouting
        - animate the marker

    Those responsibilities belong to the frontend. Road-snapping of the
    live position now happens here via Map Matching; the frontend's own
    route-deviation / reroute logic is unaffected and still operates on
    whatever points it receives.
    """

    permission_classes = [IsRider]

    def post(self, request, *args, **kwargs):

        rider = request.user
        rider_uuid = (
            rider.logistics_partner.logistics_owner_uuid
        )

        # -------------------------------------------------
        # 1. RECEIVE GPS DATA
        # -------------------------------------------------

        lat = request.data.get("lat")
        lng = request.data.get("lng")
        accuracy = request.data.get("accuracy")
        timestamp = request.data.get("timestamp")

        # Optional metadata
        speed = request.data.get("speed")
        heading = request.data.get("heading")


        # -------------------------------------------------
        # 2. BASIC VALIDATION
        # -------------------------------------------------

        if lat is None or lng is None:
            return Response(
                {
                    "status": "ignored",
                    "reason": "missing_coordinates",
                },
                status=status.HTTP_200_OK,
            )

        if accuracy is None:
            return Response(
                {
                    "status": "ignored",
                    "reason": "missing_accuracy",
                },
                status=status.HTTP_200_OK,
            )

        if timestamp is None:
            return Response(
                {
                    "status": "ignored",
                    "reason": "missing_timestamp",
                },
                status=status.HTTP_200_OK,
            )

        try:
            lat = float(lat)
            lng = float(lng)
            accuracy = float(accuracy)
            timestamp = float(timestamp)

            if speed is not None:
                speed = float(speed)

            if heading is not None:
                heading = float(heading)

        except (TypeError, ValueError):

            return Response(
                {
                    "status": "ignored",
                    "reason": "invalid_gps_data",
                },
                status=status.HTTP_200_OK,
            )

        # -------------------------------------------------
        # 3. COORDINATE RANGE VALIDATION
        # -------------------------------------------------

        if not (-90 <= lat <= 90):
            return Response(
                {
                    "status": "ignored",
                    "reason": "invalid_latitude",
                },
                status=status.HTTP_200_OK,
            )

        if not (-180 <= lng <= 180):
            return Response(
                {
                    "status": "ignored",
                    "reason": "invalid_longitude",
                },
                status=status.HTTP_200_OK,
            )

        if accuracy < 0:
            return Response(
                {
                    "status": "ignored",
                    "reason": "invalid_accuracy",
                },
                status=status.HTTP_200_OK,
            )

        # -------------------------------------------------
        # 4. GPS ACCURACY GATE
        # -------------------------------------------------

        if accuracy > MAX_BROADCAST_ACCURACY:

            logger.info(
                "GPS rejected: rider=%s accuracy=%.2fm",
                rider.id,
                accuracy,
            )

            return Response(
                {
                    "status": "ignored",
                    "reason": "poor_accuracy",
                },
                status=status.HTTP_200_OK,
            )

        # -------------------------------------------------
        # 5. LOAD LAST TRUSTED LOCATION
        # -------------------------------------------------

        cache_key = f"rider_{rider.id}_location"

        previous = cache.get(cache_key)

        # -------------------------------------------------
        # 6. STALE GPS READING CHECK
        # -------------------------------------------------

        if previous:

            previous_timestamp = previous["timestamp"]

            if timestamp <= previous_timestamp:

                return Response(
                    {
                        "status": "ignored",
                        "reason": "stale_location",
                    },
                    status=status.HTTP_200_OK,
                )

        # -------------------------------------------------
        # 7. IMPOSSIBLE GPS MOVEMENT CHECK
        # -------------------------------------------------

        if previous:

            elapsed_seconds = (
                timestamp - previous["timestamp"]
            ) / 1000.0

            if elapsed_seconds > 0:

                distance = haversine_distance(
                    previous["lat"],
                    previous["lng"],
                    lat,
                    lng,
                )

                implied_speed = (
                    distance / elapsed_seconds
                )

                if implied_speed > MAX_IMPLAUSIBLE_SPEED:

                    logger.warning(
                        "GPS jump rejected: rider=%s "
                        "distance=%.2fm elapsed=%.2fs "
                        "speed=%.2fm/s",
                        rider.id,
                        distance,
                        elapsed_seconds,
                        implied_speed,
                    )

                    return Response(
                        {
                            "status": "ignored",
                            "reason": "implausible_movement",
                        },
                        status=status.HTTP_200_OK,
                    )

        # -------------------------------------------------
        # 8. BUILD TRUSTED LOCATION
        # -------------------------------------------------

        location = {
            "lat": lat,
            "lng": lng,
            "accuracy": accuracy,
            "timestamp": timestamp,
            "speed": speed,
            "heading": heading,
        }

        # -------------------------------------------------
        # 9. CACHE TRUSTED LOCATION
        # -------------------------------------------------

        cache.set(
            cache_key,
            location,
            timeout=LOCATION_CACHE_TIMEOUT,
        )

        # -------------------------------------------------
        # 10. PUSH TO MAP-MATCHING BUFFER
        # -------------------------------------------------

        try:
            buffer_len = _push_to_match_buffer(
                rider.id, lat, lng, accuracy, timestamp, speed, heading,
            )
        except Exception as exc:  # noqa: BLE001 — cache backend is infra, not user input
            logger.error("Map-matching buffer write failed: %s", exc)
            return Response(
                {
                    "status": "error",
                    "reason": "buffer_unavailable",
                },
                status=status.HTTP_200_OK,
            )

        # -------------------------------------------------
        # 11. IF BUFFER FULL: MAP MATCH + BROADCAST
        # -------------------------------------------------

        if buffer_len < MAP_MATCHING_BATCH_SIZE:
            return Response(
                {
                    "status": "buffered",
                    "buffer_size": buffer_len,
                },
                status=status.HTTP_200_OK,
            )

        coords, radii, timestamps, meta = _pop_match_buffer(rider.id)

        channel_layer = get_channel_layer()
        outcome = _match_and_broadcast_batch(
            channel_layer,
            f"rider_{rider_uuid}",
            coords, radii, timestamps, meta,
        )

        logger.debug(
            "Batch processed: rider=%s outcome=%s size=%d",
            rider.id, outcome, len(meta),
        )

        # -------------------------------------------------
        # 12. RESPOND
        # -------------------------------------------------

        return Response(
            {
                "status": "ok",
                "batch_outcome": outcome,
                "batch_size": len(meta),
            },
            status=status.HTTP_200_OK,
        )
