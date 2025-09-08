import requests
from os import getenv

'''
curl --request GET \
--url "https://api.openaq.org/v3/locations/8118" \
--header "X-API-Key: YOUR-OPENAQ-API-KEY"
'''


def get_results():
    BASE_URL = 'https://api.openaq.org/v3/parameters/'

    headers = {
    'X-API-Key': f'{getenv('OPENAQ_KEY')}'
    }

    query_url = BASE_URL + '2/latest'

    # Query the OPENAQ API for the location
    response = requests.get(query_url, headers=headers)

    # Parse the response into a dictionary (JSON)
    response = response.json()

    return response


def get_parameters():
    BASE_URL = 'https://api.openaq.org/v3/parameters'

    headers = {
    'X-API-Key': f'{getenv('OPENAQ_KEY')}'
    }

    # Query the OPENAQ API for the location
    response = requests.get(BASE_URL, headers=headers)

    # Parse the response into a dictionary (JSON)
    response = response.json()

    return response


def get_location_id(location_name):
    BASE_URL = 'https://api.openaq.org/v3/locations/'

    headers = {
    'X-API-Key': f'{getenv('OPENAQ_KEY')}'
    }

    # Query the OPENAQ API for the location
    response = requests.get(BASE_URL, headers=headers)

    # Parse the response into a dictionary (JSON)
    response = response.json()

    # Match the location to get the id
    locations = response['results']
    for loc in locations:
        if loc["country"]["name"].lower() == location_name.lower():
            return loc["country"]["id"]
    return None


def get_measurements_by_location(location):
    BASE_URL = 'https://api.openaq.org/v3/locations/'

    headers = {
    'X-API-Key': f'{getenv('OPENAQ_KEY')}'
    }

    locations_id = get_location_id(location)

    query_url = BASE_URL + f'{locations_id}/latest'

    # Query the OPENAQ API for the location
    response = requests.get(query_url, headers=headers)

    # Parse the response into a dictionary (JSON)
    response = response.json()

    return response


if __name__ == '__main__':
    pass
    # Test things out down here