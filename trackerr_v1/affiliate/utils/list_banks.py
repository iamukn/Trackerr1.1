#!/usr/bin/python3
from os import environ
from requests import get
from django.core.cache import cache

APIKEY = environ.get('PAYSTACK_SECRET_KEY')


def list_banks():

    banks = cache.get('all_banks')
    if banks:
        return banks

    url="https://api.paystack.co/bank"

    headers = {
        "Authorization": "Bearer {}".format(APIKEY),
        "Content-Type": "application/json"
            }

    res = get(url, headers=headers)
    if not res.status_code == 200:
        print(res.json())
        return []

    res_data = res.json()

    status = res_data.get('status')

    if not status:
        print(res.json())
        return []

    banks = []

    data = res_data.get('data')

    for bank in data:
        banks.append({"name": bank.get('name').title(), "code": bank.get('code'),
                      "country": bank.get('country').lower(), "currency": bank.get('currency')
                      })


    cache.set('all_banks', banks, timeout=86400)
    return banks
