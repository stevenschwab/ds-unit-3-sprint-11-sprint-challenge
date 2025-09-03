import requests
from os import getenv

'''
curl --request GET \
--url "https://api.openaq.org/v3/locations/8118" \
--header "X-API-Key: YOUR-OPENAQ-API-KEY"
'''

def get_locations():
    BASE_URL = 'https://api.openaq.org/v3/'

    headers = {
    'X-API-Key': f'{getenv('OPENAQ_KEY')}'
    }

    query_url = BASE_URL + 'locations'

    # Query the OPENAQ API for the location
    response = requests.get(query_url, headers=headers)

    # Parse the response into a dictionary (JSON)
    response = response.json()

    return response


def get_location_by_id(id):
    BASE_URL = 'https://api.openaq.org/v3/'

    headers = {
    'X-API-Key': f'{getenv('OPENAQ_KEY')}'
    }

    query_url = BASE_URL + f'locations/{id}'

    # Query the OPENAQ API for the location
    response = requests.get(query_url, headers=headers)

    # Parse the response into a dictionary (JSON)
    response = response.json()

    return response


def get_results():
    BASE_URL = 'https://api.openaq.org/v3/parameters/'

    headers = {
    'X-API-Key': f'{getenv('OPENAQ_KEY')}'
    }

    query_url = BASE_URL + f'2/latest'

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


if __name__ == '__main__':
    pass
    # Test things out down here