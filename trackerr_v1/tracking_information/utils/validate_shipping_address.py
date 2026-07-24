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

def verify_address(address:str) -> Dict:
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
    # url to query
    here_url = 'https://geocode.search.hereapi.com/v1/geocode'
    mapbox_url = 'https://api.mapbox.com/search/geocode/v6/forward'
    google_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    api_key = env('apikey')
    google_api_key = env('google_map_api_key')
    here_params = {'q': address, 'apikey':api_key}
    google_params = {'address': address, 'key':google_api_key}

    try:
        # google query 

        google_response = get(google_url, google_params)

        google_base = google_response.json()
        res_data = google_base.get('results')[0]
        
        location = res_data.get('geometry').get('location')
        address_components = res_data.get('address_components')
        # fetch city 
        city_3 = ''
        city_2 = ''
        city_1 = ''
        city = ''
        for addr in address_components:
            if addr.get('types')[0] == 'administrative_area_level_3':
                city_3 = addr.get('long_name') + ' '
            elif addr.get('types')[0] == 'administrative_area_level_2':
                city_2 = addr.get('long_name') + ' '
            elif addr.get('types')[0] == 'administrative_area_level_1':
                city_1 = addr.get('long_name') + ''

        city = city_3 + city_2 + city_1
        address = address_components[0].get('long_name') + ' ' + city
        country = [country.get('long_name') for country in address_components if country.get('types')[0] == 'country']

        data = {
            'raw_address': old_addr.lower(),
            'address': address.lower(),
            'city' : city,
            'country' : country[0],
            'latitude' : location.get('lat', ''),
            'longitude' : location.get('lng', ''),
                }

        print('From google', data)
        # save to the database
        serializer = GeoLocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('data for ', f'addr_info:{old_addr.lower()}', 'saved and cache as', data)
        # cache it
        print(f"Cache set for addr_info:{old_addr}")
        cache.set(f'addr_info:{old_addr.lower()}', data, timeout=None)
        return data
    


        # Below is when using here API
        response = get(here_url, params=here_params)
        base = response.json().get('items')
        # get the address data
        base = base[0]

        data = {
            'address' : base.get('address').get('label'),
            'city' : base.get('address').get('city'),
            'country' : base.get('address').get('countryName'),
            'latitude' : base.get('position').get('lat'),
            'longitude' : base.get('position').get('lng'),
                }
        return data

    except IndexError as e:
        return {'error': 'incorrect address, please enter a correct address'}

    except Exception as error:
        return error
