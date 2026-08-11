#!/usr/bin/python3
from environ import Env
from requests import get
from pathlib import Path
from typing import Dict
from django.core.cache import cache
from tracking_information.serializer import GeoLocationSerializer
from tracking_information.models import GeoLocationData


env = Env(
    debug=(bool, False)
        )

BASE_DIR = Path(__file__).resolve().parent.parent
Env.read_env(BASE_DIR / '.env')
""" Verifies a Shipping address and also provide its coordinates """

def verify_address(address: str, placeId: str) -> Dict:
    """ validates and verifies  an address
    Arg:
        address: shipping address to validate
    Return:
        A dictionary of the validated address and its position
    """

    # get the old address and check if it's in the cache, serve that instead
    old_addr = address
    cached_addr = cache.get(f'addr_info:{old_addr.lower()}')
    if cached_addr:
        print('from cache')
        return cached_addr

    # if it's not in the cache check if it's in the db
    try:
        data = GeoLocationData.objects.get(raw_address=old_addr.lower())
        if data:
            serializer = GeoLocationSerializer(data=data)
            if serializer.is_valid():
                cache.set(f'addr_info:{old_addr.lower()}', serializer.data, timeout=None)
                print('Removed from DB and added to cache')
                return serializer.data
    except GeoLocationData.DoesNotExist:
        ...
    # else, geocode the address

    if not isinstance(address, str):
        raise ValueError('address must be string!')

    try:
        # google query 

        GOOGLE_API_KEY = env('google_map_api_key')

        base_url = f'https://places.googleapis.com/v1/places/{placeId}'

        headers = {
          "X-Goog-Api-Key": GOOGLE_API_KEY,
          "X-Goog-FieldMask": "location,addressComponents",
        }

        res = get(base_url, headers=headers)

        res_data = res.json()
        address_component = res_data.get('addressComponents')


        for component in address_component:
            if component.get('types'):
                if 'locality' in component.get('types'):
                    city = component.get('longText')
                elif 'country' in component.get('types'):
                    country = component.get('longText')

        location = res_data.get('location')

        data = {
            'raw_address': old_addr.lower(),
            'address': address_component[0].get('longText').lower(),
            'city' : city.lower(),
            'country' : country.lower(),
            'latitude' : location.get('latitude', ''),
            'longitude' : location.get('longitude', ''),
                }

        # save to the database
        serializer = GeoLocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        # cache it
        cache.set(f'addr_info:{old_addr.lower()}', data, timeout=None)
        return data

    except IndexError as e:
        raise(e)
        return {'error': 'incorrect address, please enter a correct address'}

    except Exception as error:
        return error
