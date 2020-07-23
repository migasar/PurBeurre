"""Handle the recovery of the data.

Fetch the data from an external repository,
and deal with the reformatting of the data.
"""

import requests

from Model.Entity.product import Product
from Model.Manager.entity_manager import EntityManager

import Static.constant as constant


class APIManager:
    """Create a request to connect with an API and to collect data from a website.

    - Take the elements from the class API to use as variables for the methods of requests.
    - Create 'responses': a list of objects of class Response (from package requests).
    """

    def __init__(self, url=None, page_size=None, page_number=None):

        # parameters of the call to the API (with default values as fallback)
        self.url = url if url is not None else constant.OFF_URL
        self.page_size = page_size if page_size is not None else 2
        self.page_number = page_number if page_number is not None else 1

        # repository of the result from the call to the API
        self.products = []

    def get_load(self):
        """Make a get request to the API (one page at a time), and fetch specific data.

        From objects of class Response (of package requests), extract the data we need on each product.
        Return a list of objects of class Product contained in 'self.products'.
        """

        # set the parameters that are constant for the API
        parameters = constant.API_PARAMETERS.copy()
        parameters.update({'page_size': self.page_size})

        # use 'page_number' to fractionate the call to the api in different requests to cap the load
        for page in range(1, self.page_number + 1):
            # iterate on the method, by modifying the parameter 'page_number'
            parameters.update({'page_number': page})
            # execute the request
            answer = requests.get(self.url, params=parameters)
            # call the method to extract the data
            self.clean_response(answer)

        return self.products

    def clean_response(self, request):
        """Get the data of interest from an object, used as a container of data.

        - Open the container, to extract the content.
        - Filter the content, to discad unwanted data.
        """

        # loop over each product in the json content of 'request' (an object of class Response)
        for outline in request.json()['products']:

            # use if/else as a filter, to keep products with categories in french
            if outline['categories_lc'] == 'fr':
                # use try/except as a filter, to discard instances of 'Product' with missing values
                try:
                    # try to create an instance of class 'Product' with required values
                    product = Product.from_api(
                            name=outline['product_name_fr'],
                            nutriscore=outline['nutriscore_score'],
                            url=outline['url'],
                            categories=outline['categories'],
                            stores=outline['stores']
                    )
                    # discard this instance and jump to the next, if a value is empty
                    if any(product.get_values()) == "":
                        raise KeyError
                # discard this instance and jump to the next, if a value is missing
                except KeyError:
                    continue
                # finally if no exception is raised, this instance is added to the list
                else:
                    self.products.append(product)

            # discard this instance of product, if it has no categories in french
            else:
                continue

        return self.products

    def download_data(self, entity_manager=EntityManager()):
        """Call an entity manager to use its method to insert a load of data in the DB."""

        # call the method 'get_load()' if it has not been done yet
        if len(self.products) == 0:
            self.get_load()

        # call the method 'insert_all' from entity_manager to save the data in the database
        return entity_manager.insert_all(self.products)
