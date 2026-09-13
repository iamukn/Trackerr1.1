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

MAX_BROADCAST_ACCURACY = 50.0  # metres
MAX_IMPLAUSIBLE_SPEED = 80.0  # metres / second
LOCATION_CACHE_TIMEOUT = 120

# Hard cap on how many points one request can carry. Without this, a
# misbehaving/compromised client could send an enormous queued_coordinates
# array and force this request to do an unbounded amount of work (loop
# iterations, cache writes, possibly several Map Matching calls) in a
# single HTTP call.
MAX_BATCH_SIZE = 50


# ---------------------------------------------------------
# MAP MATCHING CONFIGURATION
# ---------------------------------------------------------

MAP_MATCHING_BATCH_SIZE = 5
MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN", None)
MAP_MATCHING_URL = "https://api.mapbox.com/matching/v5/mapbox/driving/{coordinates}"
MATCH_BUFFER_TTL = 60  # seconds
MAP_MATCHING_TIMEOUT_S = 5
MIN_REPLAY_GAP_S = 0.3
MAX_REPLAY_GAP_S = 4.0
DENSIFY_STEP_M = 15
MATCHED_POINT_ACCURACY_M = 5.0


def haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two coordinates in metres."""
    earth_radius = 6371000.0
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lng = radians(lng2 - lng1)
    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(delta_lng / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius * c


# ---------------------------------------------------------
# MAP-MATCHING BUFFER HELPERS (unchanged)
# ---------------------------------------------------------

def _match_buffer_key(rider_id):
    return f"rider_{rider_id}_matchbuffer"


def _push_to_match_buffer(rider_id, lat, lng, accuracy, timestamp_ms, speed, heading):
    key = _match_buffer_key(rider_id)
    buffer = cache.get(key) or []
    buffer.append({
        "lat": lat, "lng": lng, "accuracy": accuracy,
        "timestamp": timestamp_ms, "speed": speed, "heading": heading,
    })
    cache.set(key, buffer, timeout=MATCH_BUFFER_TTL)
    return len(buffer)


def _pop_match_buffer(rider_id):
    key = _match_buffer_key(rider_id)
    meta = cache.get(key) or []
    cache.delete(key)

    coords = [f"{point['lng']},{point['lat']}" for point in meta]
    radii = [f"{point['accuracy']:.1f}" for point in meta]
    timestamps = [str(int(point["timestamp"] / 1000)) for point in meta]

    return coords, radii, timestamps, meta


def _request_map_matching(coords, radii, timestamps):
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
        print('MAPMATCHED:::', data)
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
    broadcast = {
        "type": "rider_location_update",
        "lat": lat, "lng": lng,
        "accuracy": accuracy, "timestamp": timestamp_ms,
        "speed": speed, "heading": heading,
    }
    async_to_sync(channel_layer.group_send)(group_name, broadcast)


def _densify_matched_geometry(geometry_coords, start_ts_ms, end_ts_ms, step_m=DENSIFY_STEP_M):
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
    Runs entirely on a background thread (see caller) — including the
    Mapbox Map Matching HTTP call itself, not just the replay. With
    batched requests, a single request can trigger several of these back
    to back; if the Mapbox call were synchronous in the request path, a
    large batch could force one HTTP request to wait on several
    sequential ~5s Mapbox calls before responding at all. Doing the whole
    thing in the background keeps response time independent of how many
    5-point matches a batch happens to trigger.

    Trade-off: the caller can no longer report "matched" vs
    "raw_fallback" synchronously in the HTTP response — that outcome is
    only known once this background work finishes. That's fine here: the
    client's retry/dedup logic only needs to know whether a GPS point was
    accepted (don't resend) vs rejected (maybe resend), which is fully
    decided by validation before this function is ever called — it
    doesn't depend on how the matching turns out.
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
        points = [(p["lat"], p["lng"], p) for p in densified]
        outcome = "raw_fallback"
    else:
        matching = result["matchings"][0]
        geometry_coords = matching["geometry"]["coordinates"]

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
    logger.debug("Background match+broadcast finished: outcome=%s size=%d", outcome, len(meta))


def _dispatch_match_and_broadcast(channel_layer, group_name, coords, radii, timestamps, meta):
    """Fire-and-forget wrapper — the request path calls this and moves on
    immediately rather than waiting for Mapbox + broadcast to finish."""
    threading.Thread(
        target=_match_and_broadcast_batch,
        args=(channel_layer, group_name, coords, radii, timestamps, meta),
        daemon=True,
    ).start()


class BroadcastLocation(APIView):
    """
    Receives one or more GPS readings from TrackerrGo.

    Accepts EITHER:
      - a single point as top-level fields: {lat, lng, accuracy, timestamp, ...}
      - a batch: {"queued_coordinates": [{lat, lng, accuracy, timestamp, ...}, ...]}

    Both shapes are normalized into a list and run through the exact same
    per-point pipeline (validate -> cache -> map-matching buffer), so
    there is only one place this logic lives — a single point is simply
    treated as a batch of length 1. This avoids the two paths silently
    drifting apart the way duplicated logic tends to in this codebase.

    Responsibilities per point:
        1. Validate the GPS payload.
        2. Reject poor-quality GPS readings.
        3. Reject stale readings.
        4. Reject obviously impossible GPS jumps.
        5. Cache the last trusted location.
        6. Buffer trusted readings for Mapbox Map Matching.
        7. Once MAP_MATCHING_BATCH_SIZE readings are buffered, send them
           to Mapbox Map Matching and broadcast the (snapped) result.

    This endpoint does NOT calculate routes, reroute, or animate the
    marker — those stay on the frontend.
    """

    permission_classes = [IsRider]

    def post(self, request, *args, **kwargs):
        rider = request.user
        rider_uuid = rider.logistics_partner.logistics_owner_uuid

        # -------------------------------------------------
        # Normalize input: single point OR queued_coordinates batch
        # -------------------------------------------------

        queued = request.data.get("queued_coordinates")

        if queued is not None:
            if not isinstance(queued, list) or len(queued) == 0:
                return Response(
                    {"status": "ignored", "reason": "empty_batch"},
                    status=status.HTTP_200_OK,
                )
            if len(queued) > MAX_BATCH_SIZE:
                logger.warning(
                    "Batch from rider=%s exceeds MAX_BATCH_SIZE (%d > %d) — rejecting.",
                    rider.id, len(queued), MAX_BATCH_SIZE,
                )
                return Response(
                    {"status": "ignored", "reason": "batch_too_large"},
                    status=status.HTTP_200_OK,
                )
            raw_points = queued
        else:
            # Single-point shape — top-level fields become a one-item batch.
            raw_points = [{
                "lat": request.data.get("lat"),
                "lng": request.data.get("lng"),
                "accuracy": request.data.get("accuracy"),
                "timestamp": request.data.get("timestamp"),
                "speed": request.data.get("speed"),
                "heading": request.data.get("heading"),
            }]

        # Defensive sort for VALIDATION order only — the staleness/
        # implausible-jump pipeline assumes chronological order. Results
        # are still returned in the ORIGINAL input order below, so
        # `results[i]` continues to correlate 1:1 with `queued_coordinates[i]`
        # regardless of this internal reordering.
        indexed_points = list(enumerate(raw_points))

        def _sort_key(item):
            _, p = item
            ts = p.get("timestamp") if isinstance(p, dict) else None
            return (ts is None, ts or 0)

        try:
            ordered = sorted(indexed_points, key=_sort_key)
        except Exception:
            ordered = indexed_points  # fall back to given order if sort itself fails

        results_by_index = {}
        for idx, raw_point in ordered:
            if not isinstance(raw_point, dict):
                results_by_index[idx] = {"status": "ignored", "reason": "invalid_item_type"}
                continue
            results_by_index[idx] = self._process_single_point(rider, rider_uuid, raw_point)

        results = [results_by_index[i] for i in range(len(raw_points))]

        # Preserve the original single-point response shape when the
        # request wasn't a batch, so existing (non-batching) client code
        # keeps working against this endpoint completely unchanged.
        if queued is None:
            return Response(results[0], status=status.HTTP_200_OK)

        return Response(
            {"status": "ok", "results": results},
            status=status.HTTP_200_OK,
        )

    def _process_single_point(self, rider, rider_uuid, raw_point):
        """
        Runs one GPS reading through the full validate -> cache -> buffer
        -> (maybe) match-and-broadcast pipeline. Returns a small dict
        describing the outcome for that specific point — this is what
        ends up in the `results` array for a batch request, or as the
        whole response body for a single-point request.
        """

        # -------------------------------------------------
        # 1. RECEIVE GPS DATA
        # -------------------------------------------------

        lat = raw_point.get("lat")
        lng = raw_point.get("lng")
        accuracy = raw_point.get("accuracy")
        timestamp = raw_point.get("timestamp")
        speed = raw_point.get("speed")
        heading = raw_point.get("heading")

        # -------------------------------------------------
        # 2. BASIC VALIDATION
        # -------------------------------------------------

        if lat is None or lng is None:
            return {"status": "ignored", "reason": "missing_coordinates", "timestamp": timestamp}

        if accuracy is None:
            return {"status": "ignored", "reason": "missing_accuracy", "timestamp": timestamp}

        if timestamp is None:
            return {"status": "ignored", "reason": "missing_timestamp"}

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
            return {"status": "ignored", "reason": "invalid_gps_data", "timestamp": timestamp}

        # -------------------------------------------------
        # 3. COORDINATE RANGE VALIDATION
        # -------------------------------------------------

        if not (-90 <= lat <= 90):
            return {"status": "ignored", "reason": "invalid_latitude", "timestamp": timestamp}

        if not (-180 <= lng <= 180):
            return {"status": "ignored", "reason": "invalid_longitude", "timestamp": timestamp}

        if accuracy < 0:
            return {"status": "ignored", "reason": "invalid_accuracy", "timestamp": timestamp}

        # -------------------------------------------------
        # 4. GPS ACCURACY GATE
        # -------------------------------------------------

        if accuracy > MAX_BROADCAST_ACCURACY:
            logger.info("GPS rejected: rider=%s accuracy=%.2fm", rider.id, accuracy)
            return {"status": "ignored", "reason": "poor_accuracy", "timestamp": timestamp}

        # -------------------------------------------------
        # 5. LOAD LAST TRUSTED LOCATION
        # -------------------------------------------------

        cache_key = f"rider_{rider.id}_location"
        previous = cache.get(cache_key)

        # -------------------------------------------------
        # 6. STALE GPS READING CHECK
        # -------------------------------------------------
        #
        # IMPORTANT for batches: `previous` gets updated (step 9) after
        # EVERY point in the loop, not just once before the whole batch.
        # So point 3 in a batch is checked for staleness against point 2
        # in that same batch, not against whatever was cached before this
        # request started. Without this, a batch of several points sent
        # together would only ever validate the first one meaningfully.

        if previous and timestamp <= previous["timestamp"]:
            return {"status": "ignored", "reason": "stale_location", "timestamp": timestamp}

        # -------------------------------------------------
        # 7. IMPOSSIBLE GPS MOVEMENT CHECK
        # -------------------------------------------------

        if previous:
            elapsed_seconds = (timestamp - previous["timestamp"]) / 1000.0
            if elapsed_seconds > 0:
                distance = haversine_distance(previous["lat"], previous["lng"], lat, lng)
                implied_speed = distance / elapsed_seconds

                if implied_speed > MAX_IMPLAUSIBLE_SPEED:
                    logger.warning(
                        "GPS jump rejected: rider=%s distance=%.2fm elapsed=%.2fs speed=%.2fm/s",
                        rider.id, distance, elapsed_seconds, implied_speed,
                    )
                    return {"status": "ignored", "reason": "implausible_movement", "timestamp": timestamp}

        # -------------------------------------------------
        # 8. BUILD + 9. CACHE TRUSTED LOCATION
        # -------------------------------------------------

        location = {
            "lat": lat, "lng": lng, "accuracy": accuracy,
            "timestamp": timestamp, "speed": speed, "heading": heading,
        }
        cache.set(cache_key, location, timeout=LOCATION_CACHE_TIMEOUT)

        # -------------------------------------------------
        # 10. PUSH TO MAP-MATCHING BUFFER
        # -------------------------------------------------

        try:
            buffer_len = _push_to_match_buffer(
                rider.id, lat, lng, accuracy, timestamp, speed, heading,
            )
        except Exception as exc:  # noqa: BLE001 — cache backend is infra, not user input
            logger.error("Map-matching buffer write failed: %s", exc)
            return {"status": "error", "reason": "buffer_unavailable", "timestamp": timestamp}

        # -------------------------------------------------
        # 11. IF BUFFER FULL: MAP MATCH + BROADCAST
        # -------------------------------------------------

        if buffer_len < MAP_MATCHING_BATCH_SIZE:
            return {"status": "buffered", "buffer_size": buffer_len, "timestamp": timestamp}

        coords, radii, timestamps, meta = _pop_match_buffer(rider.id)
        channel_layer = get_channel_layer()

        # Fire-and-forget: matching + broadcast happen on a background
        # thread. This request returns immediately regardless of how
        # many 5-point matches this batch triggers — see
        # _match_and_broadcast_batch's docstring for why.
        _dispatch_match_and_broadcast(
            channel_layer, f"rider_{rider_uuid}", coords, radii, timestamps, meta,
        )

        return {
            "status": "ok",
            "batch_outcome": "queued_for_matching",
            "batch_size": len(meta),
            "timestamp": timestamp,
        }
