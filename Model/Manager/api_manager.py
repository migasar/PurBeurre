"""
Handle the recovery of the data.

Fetch the data from an external repository,
and deal with the reformatting of the data.
"""

import requests

from Model.Entity.category import Category
from Model.Entity.product import Product
from Model.Entity.store import Store

from Model.Manager.entity_manager import EntityManager


class API:
    """Set the API. """

    def __init__(self, url, parameters):
        self.url = url
        self.parameters = parameters


class APICaller:
    """
    Create a request to connect with an API and to collect data from a website.

    - take the elements from the class API to use as variables for the methods of requests
    - create 'responses' : a list of objects of class Response (from package requests)
    """

    def __init__(self, api):
        self.url = api.url
        self.parameters = api.parameters
        self.responses = []

    def get_responses(self):
        """
        Make a get request to the API (one page at a time).

        Return 'responses': a list of objects of class Response (from package requests)
        """

        if self.parameters["page"] is None:
            # send a get request for only one page

            answer = requests.get(self.url, params=self.parameters)
            self.responses.append(answer)

        else:
            # send a get request for each page iteratively

            page_number = self.parameters["page"]
            # use the parameter 'page' to set the range of the loop
            # objets = []
            # for p in range(1, page_number + 1):
            #     # iterate on the method, by modifying the parameter 'page'
            #     self.parameters["page"] = p
            #     answer = requests.get(self.url, params=self.parameters)
            #     recupère le json dans answzer.request
            #     for chaque obket dans la listye json:
            #         try:
            #           objet = Product(info 1, info 2 info 3)
            #           ajouter l'objet a la liste'
            #         except ERREUR:
            #           continue
            # apelle la database en lui envoyant la liste d'objets



                #self.responses.append(answer)

            self.parameters["page"] = page_number
            # cancel the modifications made to the variable 'page'

        return self.responses

    def test_status(self):
        """Print the status code of the response. """

        response = requests.get(self.url, params=self.parameters)

        if response is None:
            return "The request has yet to be made. "

        else:
            return "status code of the API : {}".format(str(response.status_code))


class DataCleaner:
    """
    Handle a complex container of data (with many layers of structure), open it and manipulate its content.

    - take 'container':  data structure that can be of 2 possible types
        - list concatenating many objects of class Response, coming from an instance of 'APICaller'
        - list of dictionaries (with similar internal elements)
    - modify 'container' (if needed): ensure that it is a list of dictionaries before applying the other methods
    - create 'payload': elements of data extracted and formated from the variable 'data'.

    'payload' is a dictionary which associates a number as key with the data of one product as value.
    """

    def __init__(self, container):
        self.container = container
        self.payload = {}

        self.test_container()
        # test the initial structure of container and modify it if needed

    def test_container(self):
        """
        Ensure that the object 'container' has the apropriate internal structure (a list of dict)

        Test if the container is list of object of class Response (a special class of the package requests),
        If it's the case, it applyies the method 'filter_container()' to modify the structure of 'container'

        'container' is a list of Response objects when it comes from a call to an API (it is the expected way).
        'test_container' was made to have the option to use also a sapmle of data from a json file.
        """

        def filter_container(responses):
            """
            Open an object used as container, and extract the data in an usable format.

            - take 'responses': a list of objects of class Response (from package requests)
            - return 'data_dump': a list of dict (and a modified version of 'data_responses')

            for each elements contained in 'responses':
            - use a dedicated method on the element (an object Response) to retrieve its content in a json object
            - iterate over the different layers of the json object, to access 'products'
                - 'products' is a list
                - each element of this list is a dictionary representing one specific product)
            - append a copy of each product (as an object of type dict) in 'data_dump'
            """

            data_dump = []

            for i in responses:
                # retrieve the content of the Response as a json object
                response_json = i.json()

                for j in response_json['products']:
                    # append a copy of each product (as a dict) in 'data_dump'
                    data_dump.append(j)

            return data_dump

        # apply 'filter_container' if the internal structure of 'container' requires it
        if type(self.container[0]) is requests.models.Response:
            print("Data comes from the API")
            self.container = filter_container(self.container)
            return self.container
        else:
            print("Data comes from a JSON file")

    def extract_values(self):
        """
        Method orchestrating the use of the other methods to iterate over the container.

        - search for specific data (for each product, fetch only values that we specified)
        - test the viability of the data (product with missing values are discarded)
        - format the data (for each viable product, create a dict with the values that we fetched)
        - structure the data (agregate the results in a dict (payload), using numbers as keys for each product/dict)
        """

        def test_values(freight, vessel):
            """
            Test if a dict contains all the data that we requested.

            - takes 'freight': a dict on which to perform the search
            - takes 'vessel': a dict used as a point of comparison

            'vessel' is a dict structured to use its keys as a pointer to perform the tests
            """

            test = True
            # variable used as the result of the tests

            for key in vessel.keys():
                if freight[key] is None:
                    # test for missing data
                    test = False
                    break

            if freight['countries_lc'] != 'fr':
                # test for data in french
                test = False

            return test

        def get_values(freight, vessel):
            """
            Retrieve the data that we requested and copy it in vessel.

            - takes 'freight': a dict from which comes the values
            - takes 'vessel': a dict used as a repository of the values

            vessel is a dict with its keys already established, but with no values for the keys
            Its keys are used as a pointer for the method.
            """

            for key in vessel.keys():
                # for each key of 'vessel', associate the value of the same key in 'freight'
                vessel[key] = freight[key]

            return vessel

        count = 0  # incremented values to be used as keys in the dictionary 'payload'
        for product in self.container:
            # go through the content of each product in the list

            cargo = {
                    'product_name_fr': None,
                    'nutriscore_score': None,
                    'code': None,
                    'url': None,
                    'categories_tags': None,
                    'stores_tags': None,
                    'countries_lc': None
            }
            # 'cargo' is a dictionary with its keys already established, but with no values associated yet
            # First, its keys are used as a pointer for the methods,
            # and finally, it will be used to store the data that we want

            if test_values(product, cargo) is True:
                # test if a product has the required data

                get_values(product, cargo)
                # fetch the data
                count += 1
                # increment the value of count
                # the values of count are used as keys in the dictionary 'payload'
                self.payload[count] = cargo.copy()
                # add an item to the dictionary 'payload'
                # the new item associates -> key(='count'): value(='cargo')

            else:
                continue
                # if the product fails the tests, the loop moves to the next product

        return self.payload


class DataDownloader:
    """
    Handle the data, and load it in a database.

    - 'payload': a dictionary of products. Each product is an item (<key = int>: <value = data of one product>).
        - 'payload' comes from DataCleaner
    - 'db':  a connector in charge of the connection with the database.
        - 'db' comes from DBManager in Model.Manager.db_manager
    - 'manager': an entity manager handling the sql queries to interact with the databse.
        - 'manager' comes from EntityManager in Model.Manager.entity_manager

    Process to load the data:
    1. for each product, as a dictionary in 'payload':
        1.1. create an instance of class 'Product'
        1.2. call the instance of 'Product' with the entity_manager to create a new row in the table 'product'
        1.3. for each category referenced in the attribute 'categories' of the instance 'Product':
            - test if an instance of class 'Category' has already been created for this category:
                - if it exists:
                    - modify the attribute 'products' in this instance of 'Category',
                        to add the name of this instance of 'Product' in the list
                - if it doesn't exist yet:
                    - create an instance of this category,
                        with the name of this instance 'Product' referenced in its attribute 'products'
        1.4. for each store referenced in the attribute 'store' of the instance 'Product':
            - test if an instance of class 'Store' has already been created for this store:
                - if it exists:
                    - modify the attribute 'products' in this instance of 'Store',
                        to add the name of this instance of 'Product' in the list
                - if it doesn't exist yet:
                    - create an instance of this store,
                        with the name of this instance 'Product' referenced in its attribute 'products'
    2. for each category, as an instance in memory:
        2.1. call the instance of 'Category' with the entity_manager to create a new row in the table 'category'
        2.2. for each product referenced in the attribute 'products' of this instance of 'Category':
            - use the entity_manager to create a new row in the table 'category_product',
                which associates the id of this instance of 'Category', and the id of this instance of 'Product'
    3. for each store, as an instance in memory:
        3.1. call the instance of 'Store' with the entity_manager to create a new row in the table 'store'
        3.2. for each product referenced in the attribute 'products' of this instance of 'Store':
            - use the entity_manager to create a new row in the table 'store_product',
                which associates the id of this instance of 'Store', and the id of this instance of 'Product'
    """

    def __init__(self, db, entity, payload):
        self.db = db  # db connector from DBManager (Model.Manager.db_manager)
        self.entity = entity  # entity manager from EntityManager (Model.Manager.entity_manager)
        self.payload = payload  # payload from DataCleaner

    def register_data(self):

        dict_products = {}  # dictionary listing every product
        dict_categories = {}  # dictionary listing every category
        dict_stores = {}  # dictionary listing every store

        count_categories = 1  # incremented count that will serves as id in dict_categories
        count_stores = 1  # incremented count that will serves as id in dict_stores

        for p in self.payload:

            # register the product as an entry in dict_products
            dict_products[p] = {
                    'id': p,
                    'name': p['product_name_fr'],
                    'nutriscore': p['nutriscore_score'],
                    'code': p['code'],
                    'url': p['url']
            }

            # register the category as an entry in dict_categories
            for c in p['categories_tags']:

                # verify if the category has already been registered in the dedicated dictionary
                if c not in dict_categories.keys():
                    # register the category as an entry in dict_categories
                    dict_categories[c] = {
                            'id': count_categories,
                            'name': c,
                            'products': list(p['product_name_fr'])
                    }
                    count_categories += 1
                else:
                    # this category is already registered in the dictionary
                    # update its entry, to associate the name of the related product to this category
                    dict_categories[c]['products'].append(p['product_name_fr'])

            # register the store as an entry in dict_stores
            for s in p['stores_tags']:

                # verify if the store has already been registered in the dedicated dictionary
                if s not in dict_stores.keys():
                    # register the category as an entry in dict_categories
                    dict_stores[s] = {
                            'id': count_stores,
                            'name': s,
                            'products': list(p['product_name_fr'])
                    }
                    count_stores += 1
                else:
                    # this store is already registered in the dictionary
                    # update its entry, to associate the name of the related product to this store
                    dict_stores[s]['products'].append(p['product_name_fr'])

        return dict_products, dict_categories, dict_stores

    def download_products(self, table_name, col_names, val_names, values):
        self.entity.save_data(table_name, col_names, val_names, values)

    def download_categories(self):
        pass

    def download_stores(self):
        pass

    def download_product_to_category(self):
        pass

    def download_product_to_store(self):
        pass

