import os
import requests

def mapbox_autocomplete(country_code: str, q: str) -> list:

    HERES_API_KEY = os.getenv('HERES_API_KEY')

    suggestions = []


    try:

        url = f'https://autocomplete.search.hereapi.com/v1/autocomplete?q={q}&apiKey={HERES_API_KEY}&limit=10&in=countryCode:{country_code}'

        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            suggestions = data.get('items')

        return suggestions
    except Exception as e:
        print(e)
        return suggestions



def googlemaps_autocomplete(address, country, session_token='4567w65wtyw') -> list:

    suggestions = []

    if len(address) <= 3:
        return suggestions
    GOOGLEMAPS_API_KEY = os.getenv('google_map_api_key')
    url = "https://places.googleapis.com/v1/places:autocomplete"

    country_code = 'ng' if country == 'nigeria' else 'gh'

    data = {
        "input": address,
        "includedRegionCodes": country_code,
        "sessionToken": session_token
            }

    headers = {
        'Content-Type': 'application/json',
        "X-Goog-Api-Key": GOOGLEMAPS_API_KEY
            }

    try:
        res = requests.post(url, json=data, headers=headers)

        data = res.json().get('suggestions')

        if data:
            for item in data:
                suggestions.append({'title': item.get('placePrediction').get('text').get('text'), 
                    'address' : {'label': item.get('placePrediction').get('text').get('text')},
                    'placeId': item.get('placePrediction').get('placeId')})
        return suggestions
    except Exceotion as e:
        print(e)
        return suggestions
