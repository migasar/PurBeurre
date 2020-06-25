"""Handle the recovery of the data.

Fetch the data from an external repository,
and deal with the reformatting of the data.
"""


import requests

from Model.Entity.category import Category
from Model.Entity.product import Product
from Model.Entity.store import Store

from Model.Manager.entity_manager import EntityManager


class API:
    """Set the API."""

    def __init__(self, url, parameters):
        self.url = url
        self.parameters = parameters


class APICaller:
    """Create a request to connect with an API and to collect data from a website.

    - Take the elements from the class API to use as variables for the methods of requests.
    - Create 'responses': a list of objects of class Response (from package requests).
    """

    def __init__(self, api):
        self.url = api.url
        self.parameters = api.parameters
        self.products = []

        self.categories = []  # variable used only for the development
        self.stores = []  # variable used only for the development

        self.category_census = []  # variable used only for the development
        self.store_census = []  # variable used only for the development

    def get_data(self):
        """Make a get request to the API (one page at a time), and fetch specific data.

        From objects of class Response (of package requests), extract the data we need on each product.
        Return a list of objects of class Product contained in 'self.products'.
        """

        def request_api():
            """Make a get request to the API (one page at a time)."""

            # use the parameter 'page' to set the range of the loop
            page_number = self.parameters["page"]

            for page in range(1, page_number + 1):

                # iterate on the method, by modifying the parameter 'page'
                self.parameters["page"] = page

                # execute the request
                answer = requests.get(self.url, params=self.parameters)

                # call the function iteratively, to extract the data
                clean_response(answer)

            # clean the variable 'page' by canceling its modifications
            self.parameters["page"] = page_number

            return self.products

        def clean_response(answer):
            """Get the data of interest from an object, used as a container of data.

            - Open the container, to extract the content.
            - Filter the content, to discad unwanted data.
            """

            # loop over each product in the json content of 'answer.requests' (an object of class Response)
            for p in answer.json()['products']:
                """
                for each product:
                    filter out product without complying values:
                        discard product without values in french
                        discard product with missing values
                    creates instances of our entities
                        create an instance of class Product 
                            with specified basic values as variables
                        create an instance of class Category for each category of the product
                            modify the variable category of the instance of Product
                                append a list composed of every instance of Category related to the product
                        create an instance of class Store for each store of the product
                            modify the variable store  of the instance of Product
                                append a list composed of every instance of Store related to the product
                """

                # filter products to keep exclusively those with complying values

                # use if/else as a filter, to keep products with categories in french
                if p['categories_lc'] == 'fr':

                    # use try/except as a filter to discard products with missing values, when we create instances of our entities
                    try:

                        # create an instance of class 'Product' with base values
                        product = Product(
                                name=p['product_name_fr'],
                                brands=[b.strip() for b in p['brands'].split(',')],
                                nutriscore=p['nutriscore_score'],
                                code=p['code'],
                                url=p['url']
                        )

                    # if a value is missing, discard this product and continue to the next
                    except KeyError:
                        continue

                    else:

                        # use dedicated static methods in the class 'Product', to create the instances of 'Category' and'Store'
                        try:

                            # create an instance of class 'Category' for each category of this product
                            # make a list with all these instances of 'Category'
                            # append this list to the variable 'categories' of this instance of 'Product'
                            product.categories = product.get_categories(p['categories'], product)

                            # create an instance of class 'Store' for each store of this product
                            # make a list with all these instances of 'Store'
                            # append this list to the variable 'stores' of this instance of 'Product'
                            product.stores = product.get_stores(p['stores'], product)

                            self.products.append(product)

                        # if a value is missing for the categories or the stores, discard this product and continue to the next
                        except KeyError:
                            continue

                # if the product has no categories in french, discard it and continue to the next product
                else:
                    continue

            return self.products

        # launch the cascading call to the functions
        request_api()

        return self.products

    def get_category_instances(self):  # method used only for the development
        """Create a list with every instances of 'Category'.

        Iterate on a method of class Product.
        """

        for p in self.products:
            self.categories += p.categories

        return self.categories

    def get_category_census(self):  # method used only for the development
        """Create an object listing every instances of 'Category'

        with no duplicates,
        and with a listing per category of every product related to them.
        """

        # launch the method 'get_category_instances' to ensure that 'self.categories' is ready
        self.get_category_instances()
        # ensure that the variable 'self.category_census' is clean
        self.category_census = []

        # create a list with the name of the categories (without duplicates)
        cat_set = sorted(set([cat.name for cat in self.categories]))

        # use the listing of category names to set the loop
        for cat in cat_set:

            # initiate a list to save every instance of Product related to this category name
            cat_prods = []
            # loop over the elements of self.categories to catch every occurence of this category name
            for c in self.categories:
                if str(cat) == c.name:
                    # catch each instance of Product associated with an occurence of this category name
                    cat_prods.append(c.products)

            # modify the list cat_prods to improve it (sort it by the name of the products and discard the duplicates)
            cat_prod_set = sorted(list(set(cat_prods)), key=lambda prod: prod.name)

            # create an instance of this category (and attach the related instances of product)
            case = Category(
                    name=str(cat),
                    products=cat_prod_set
            )
            # add this instance of Category to the listing of categories
            self.category_census.append(case)

        return self.category_census

    def get_store_instances(self):  # method used only for the development
        """Create a list with every instances of 'Store'.

        Iterate on a method of class Product.
        """

        for p in self.products:
            self.stores += p.stores

        return self.stores

    def get_store_census(self):  # method used only for the development
        """Create an object listing every instances of 'Store'

        with no duplicates,
        and with a listing per category of every product related to them.
        """

        # launch the method 'get_store_instances' to ensure that 'self.stores' is ready
        self.get_store_instances()
        # ensure that the variable 'self.category_census' is clean
        self.store_census = []

        # create a list with the name of the stores (without duplicates)
        shop_set = sorted(set([shop.name for shop in self.stores]))

        # use the listing of store names to set the loop
        for shop in shop_set:

            # initiate a list to save every instance of Product related to this store name
            shop_prods = []
            # loop over the elements of self.stores to catch every occurence of this store name
            for s in self.stores:
                if str(shop) == s.name:
                    # catch each instance of Product associated with an occurence of this store name
                    shop_prods.append(s.products)

            # modify the list shop_prods to improve it (sort it by the name of the products and discard the duplicates)
            shop_prod_set = sorted(list(set(shop_prods)), key=lambda prod: prod.name)

            # create an instance of this store (and attach the related instances of product)
            showcase = Store(
                    name=str(shop),
                    products=shop_prod_set
            )
            # add this instance of Store to the listing of stores
            self.store_census.append(showcase)

        return self.store_census

    # LIST OF PRODUCT IN DB
    # call the DB to send the list of objects
    def call_db(self):
        # use self.products when it is full
        pass

        # BROUILLONS
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

        # self.responses.append(answer)

        # self.parameters["page"] = page_number
        # # cancel the modifications made to the variable 'page'

        # return self.responses

    def test_status(self):
        """Print the status code of the response."""

        response = requests.get(self.url, params=self.parameters)

        if response is None:
            return "The request has yet to be made."

        else:
            return "status code of the API: {}".format(str(response.status_code))


class DataCleaner:
    """Handle a complex container of data (with many layers of structure), open it and manipulate its content.

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
        """Ensure that the object 'container' has the apropriate internal structure (a list of dict).

        Test if the container is list of object of class Response (a special class of the package requests),
        If it's the case, it applyies the method 'filter_container()' to modify the structure of 'container'

        'container' is a list of Response objects when it comes from a call to an API (it is the expected way).
        'test_container' was made to have the option to use also a sapmle of data from a json file.
        """

        def filter_container(responses):
            """Open an object used as container, and extract the data in an usable format.

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
        """Method orchestrating the use of the other methods to iterate over the container.

        - search for specific data (for each product, fetch only values that we specified)
        - test the viability of the data (product with missing values are discarded)
        - format the data (for each viable product, create a dict with the values that we fetched)
        - structure the data (agregate the results in a dict (payload), using numbers as keys for each product/dict)
        """

        def test_values(freight, vessel):
            """Test if a dict contains all the data that we requested.

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
            """Retrieve the data that we requested and copy it in vessel.

            - takes 'freight': a dict from which comes the values
            - takes 'vessel': a dict used as a repository of the values

            'vessel' is a dict with its keys already established, but with no values for the keys.
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
    """Handle the data, and load it in a database.

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
