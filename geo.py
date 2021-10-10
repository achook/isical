from urllib.parse import quote
from typing import List

from requests import get
from json import loads
from os import environ

def get_coordinates(buildings: List[str]):
    geo_api_key = environ['GEO_API_KEY']

    coordinates = {}

    for building in buildings:
        search_phrase = f'AGH {building}, Kraków'
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={quote(search_phrase)}'
        url += f'&key={geo_api_key}'

        # Get and parse response from Google API
        # No https because it never works on macOS
        resp = get(url, verify=False)
        data = loads(resp.text)

        coords = data['results'][0]['geometry']['location']
        coordinates[building] = coords

    return coordinates