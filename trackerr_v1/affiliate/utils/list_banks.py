#!/usr/bin/python3
from os import environ
from requests import get
from django.core.cache import cache

APIKEY = environ.get('PAYSTACK_SECRET_KEY')


def list_banks():

    banks = cache.get('all_banks')
    if banks:
        print('cache')
        return banks

    regions = ['nigeria', 'ghana']

    headers = {
        "Authorization": "Bearer {}".format(APIKEY),
        "Content-Type": "application/json"
            }

    banks = []
    seen = set()

    for country in regions:
        url = f"https://api.paystack.co/bank?country={country}"
        res = get(url, headers=headers)
        if not res.status_code == 200:
            print(res.json())
            return []

        res_data = res.json()

        status = res_data.get('status')

        if not status:
            return []


        data = res_data.get('data')

        for bank in data:
            if bank.get('currency') == 'USD':
                continue

            name = bank.get("name", "").lower()

            if name in seen:
                continue

            seen.add(name)

            country = bank.get('country', '').lower()
            currency = bank.get('currency')
            code = bank.get('code')

            if name == 'mtn' and country == 'ghana':
                name = 'Mtn Momo Gh'

            banks.append({"name": name.title(), "code": code,
                        "country": country, "currency": currency.lower()
                        })

    cache.set('all_banks', banks, timeout=86400)
    return banks
