""" Regroup the constants of the program : settings, parameters... """


import os


# addresses of connection to the API of OpenFoodFacts
PRODUCTS_URL = 'https://fr.openfoodfacts.org/cgi/search.pl'

CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories'


# parameters for the connection to the API of OpenFoodFacts
PRODUCTS_ACTION = 'process'
PRODUCTS_SORT_BY = 'unique_scans_n'
PRODUCTS_PAGE_SIZE = 100
PRODUCTS_JSON = 'true'
PRODUCTS_PAGE = 1
PRODUCTS_PARAMETERS = {
    "action": 'process',
    "sort_by": 'unique_scans_n',
    "page_size": 100,
    "json": 'true',
    # "page": 1
}

CATEGORIES_SORT_BY = 'products'
CATEGORIES_JSON = 'true'
CATEGORIES_PARAMETERS = {
    "sort_by": 'products',
    "json": 'true'
}


# parameters to set the paths around the project structure
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCHEMA_PATH = os.path.join(PROJECT_ROOT, 'Static', 'schema_purbeurre.sql')


def get_path(*args):
    """create a path to any component of the project"""
    return os.path.join(PROJECT_ROOT, *args)
