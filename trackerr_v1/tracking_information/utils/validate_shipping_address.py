#!/usr/bin/python3
from environ import Env
from requests import get
from pathlib import Path
from typing import Dict


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

    if not isinstance(address, str):
        raise ValueError('address must be string!')
    # url to query
    url = 'https://geocode.search.hereapi.com/v1/geocode'

    api_key = env('apikey')
    params = {'q': address, 'apikey':api_key}
    try:
        response = get(url, params=params)
        base = response.json().get('items')[0]

        data = {
            'address' : base.get('address').get('label'),
            'city' : base.get('address').get('city'),
            'country' : base.get('address').get('countryName'),
            'latitude' : base.get('position').get('lat'),
            'longitude' : base.get('position').get('lng'),
                }
        return data
    except Exception as error:
        return error
