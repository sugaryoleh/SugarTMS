import urllib.parse

import requests
from urllib3.exceptions import HTTPError

from app.models.facility import Facility
from maps.api_key import ApiKey


class PlaceResolver:
    base_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={places}&inputtype=textquery&fields={arguments}&key={api_key}'
    allowed_arguments = ('rating',)

    def __init__(self, facility):
        if not isinstance(facility, Facility):
            raise TypeError('PlaceResolver got an argument with type different from Facility')
        self.facility = facility

    def get_place_details(self, *args):
        valid_arguments = self.validate_request_arguments(args)
        arguments_string = urllib.parse.quote_plus(','.join(valid_arguments))
        places_string = urllib.parse.quote_plus(str(self.facility)+str(self.facility.address))
        api_key = ApiKey.get_key()
        url = self.base_url.format(places=places_string, arguments=arguments_string, api_key=api_key)
        r = requests.get(url)
        # print(url)
        if r.status_code == 200:
            r = r.json()
            if len(r['candidates']):
                return r['candidates'][0]
            else:
                raise HTTPError('Could not match the location')
        else:
            raise HTTPError('Could not resolve the place')

    @staticmethod
    def validate_request_arguments(*args):
        arguments = PlaceResolver.intersection(*args, PlaceResolver.allowed_arguments)
        if not arguments:
            raise ValueError('Arguments to request place are not specified')
        return arguments

    @staticmethod
    def intersection(l1, l2):
        result = []
        l1 = set(l1)
        l2 = set(l2)
        for el in l1:
            if el in l2:
                result.append(el)
        return result
