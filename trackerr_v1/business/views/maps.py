from rest_framework.permissions import AllowAny
from .business_owner_permission import IsBusinessOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from requests import get, post
from django.core.cache import cache
from business.utils.autocomplete import mapbox_autocomplete, googlemaps_autocomplete

# auto complete call and polyline fetch route

class Polyline(APIView):
    permission_classes = [AllowAny,]

    def get(self, requests, *arg, **kwargs):
        rider_lat = requests.query_params.get('rider_lat')
        rider_lng = requests.query_params.get('rider_lng')
        dest_lat = requests.query_params.get('dest_lat')
        dest_lng = requests.query_params.get('dest_lng')
        MAPBOX_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')

        cache_key = f'polyline_{rider_lat}_{rider_lng}:{dest_lat}_{dest_lng}'

        cached_polyline = cache.get(cache_key)
        # if the polyline already exists, serve it
        if cached_polyline:
            return Response(cached_polyline, status=status.HTTP_200_OK)

        url = f'https://api.mapbox.com/directions/v5/mapbox/driving/{rider_lng},{rider_lat};{dest_lng},{dest_lat}?geometries=geojson&access_token={MAPBOX_TOKEN}'
        res = get(url)
        if res.status_code == 200:
            data = res.json()
            # set as cached
            cache.set(cache_key, data, timeout=60 * 60 * 24 * 7)
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=res.status_code)

class Autocomplete(APIView):
    permission_classes = [IsBusinessOwner,]

    def get(self, requests, *arg, **kwargs):

        country = requests.user.country.lower()
        countryCode = 'NGA' if country == 'nigeria' else 'GHA' if country == 'ghana' else ''
        q = requests.query_params.get('q')
    
        HERES_API_KEY = os.getenv('HERES_API_KEY')

        cache_key = f"autocomplete:{q.lower()}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        #suggestions = mapbox_autocomplete(country_code=countryCode, q=q)
        session_token = requests.query_params.get('sessionToken')
        
        suggestions = googlemaps_autocomplete(address=q, country=country, session_token=session_token)

        if len(suggestions) > 0:
            cache.set(
                cache_key,
                suggestions,
                timeout=60 * 60 * 24 # 24 hours caching
                )
        return Response(suggestions, status=status.HTTP_200_OK)
