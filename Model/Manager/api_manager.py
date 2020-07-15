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

    def __init__(self, url=constant.OFF_URL, page_size=5, page_number=5):
        self.url = url
        self.page_size = page_size
        self.page_number = page_number
        self.products = []

    def get_data(self):
        """Make a get request to the API (one page at a time), and fetch specific data.

        From objects of class Response (of package requests), extract the data we need on each product.
        Return a list of objects of class Product contained in 'self.products'.
        """

        parameters = constant.API_PARAMETERS.copy()

        # use 'page_number' to fractionate the call to the api in different requests to cap the load
        for page_number in range(1, self.page_number + 1):

            # iterate on the method, by modifying the parameter 'page_number'
            pages = {
                    'page_size': self.page_size,
                    'page_number': page_number
            }
            parameters.update(pages)

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
                    product = Product(
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

    def download_data(self, entity=EntityManager()):
        """Call an entity manager to use its method to insert a load of data in the DB."""

        # call the method 'get_data()' if it has not been done yet
        if len(self.products) == 0:
            self.get_data()

        # call the method 'insert_all' from entity_manager to save the data in the database
        return entity.insert_all(self.products)
