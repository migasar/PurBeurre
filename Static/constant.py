"""Regroup the constants of the program: settings, parameters..."""


import os


# addresses of connection to the API of OpenFoodFacts
OFF_URL = 'https://fr.openfoodfacts.org/cgi/search.pl'

CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories'


# parameters for the connection to the API of OpenFoodFacts
API_ACTION = 'process'
API_SORT_BY = 'unique_scans_n'
API_PAGE_SIZE = 10
API_JSON = 'true'
API_PAGE = 3

API_PARAMETERS = {
        "action": API_ACTION,
        "sort_by": API_SORT_BY,
        "page_size": API_PAGE_SIZE,
        # "page_size": API_PAGE_SIZE,
        "json": API_JSON,
        "page": API_PAGE
}

API_OFF_PARAMETERS = {
        "action": 'process',
        "sort_by": 'unique_scans_n',
        "page_size": 2,
        # "page_size": 100,
        "json": 'true',
        "page": 5
}


# parameters to set the paths around the project structure
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCHEMA_PATH = os.path.join(PROJECT_ROOT, 'Static', 'schema_purbeurre.sql')

JSON_PATH = os.path.join(PROJECT_ROOT, 'Static', 'samples', 'payload.json')


def get_path(*args):
    """Create a path to any component of the project."""
    return os.path.join(PROJECT_ROOT, *args)
