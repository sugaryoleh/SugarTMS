import urllib

import requests
from urllib3.exceptions import HTTPError

from app.models.address import Address
from maps.api_key import ApiKey


class DistanceCalculator:
    mode = 'driving'
    units = 'imperial'
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins_string}&destinations={destinations_string}&units={units}&key={api_key}'

    @staticmethod
    def check_types(points):
        if not isinstance(points, list):
            raise TypeError('Distance calculator got an argument with the type different from list')
        elif not all(isinstance(el, Address) for el in points):
            raise TypeError('One of point is not an Address object')
        return True

    @staticmethod
    def get_matrix(points_string):
        api_key = ApiKey.get_key()
        url = DistanceCalculator.base_url.format(origins_string=points_string, destinations_string=points_string,
                                                 units=DistanceCalculator.units, api_key=api_key)
        r = requests.get(url)
        if r.status_code != 200:
            raise HTTPError('Cannot set check distances between points')
        distance = r.json()['rows']['distance']['text']
        distance = int(distance.split()[1])
        return distance

    @staticmethod
    def calculate(points):
        DistanceCalculator.check_types(points)
        points_string = DistanceCalculator.points_to_sting(points)
        points_string_encoded = urllib.parse.quote_plus(points_string)
        matrix = DistanceCalculator.get_matrix(points_string_encoded)
        for i in range(len(matrix)-1):
            print(matrix[i]['elements'][i+1])

    @staticmethod
    def points_to_sting(points):
        return '|'.join((str(point) for point in points))

