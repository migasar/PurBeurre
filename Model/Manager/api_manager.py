"""Handle the recovery of the data.

Fetch the data from an external repository,
and deal with the reformatting of the data.
"""


import requests

from Model.Entity.category import Category
from Model.Entity.product import Product
from Model.Entity.store import Store

import Static.credential as credential
import Static.constant as constant
import Static.sql_queries as queries


class APIManager:
    """Create a request to connect with an API and to collect data from a website.

    - Take the elements from the class API to use as variables for the methods of requests.
    - Create 'responses': a list of objects of class Response (from package requests).
    """

    def __init__(self, url=constant.OFF_URL, page_size=5, page=2):

        self.url = url
        self.page_size = page_size
        self.page = page
        self.products = []
        # self.categories = []  # variable used only for the development
        # self.stores = []  # variable used only for the development
        # self.category_census = []  # variable used only for the development
        # self.store_census = []  # variable used only for the development

    def get_data(self):
        """Make a get request to the API (one page at a time), and fetch specific data.

        From objects of class Response (of package requests), extract the data we need on each product.
        Return a list of objects of class Product contained in 'self.products'.
        """

        parameters = constant.API_PARAMETERS.copy()

        # use page to fractionate the call to the api in different requests to cap the load
        for page_number in range(1, self.page + 1):
            # iterate on the method, by modifying the parameter 'page'
            pages = {
                    'page_size': self.page_size,
                    'page': page_number
            }
            parameters.update(pages)

            # execute the request
            answer = requests.get(self.url, params=parameters)

            # call the function iteratively, to extract the data
            self.clean_response(answer)

        return self.products

    def clean_response(self, request):
        """Get the data of interest from an object, used as a container of data.

        - Open the container, to extract the content.
        - Filter the content, to discad unwanted data.
        """

        # loop over each product in the json content of 'request' (an object of class Response)
        for outline in request.json()['products']:

            # filter products to keep exclusively those with complying values
            # use if/else as a filter, to keep products with categories in french
            if outline['categories_lc'] == 'fr':

                # use try/except when we create instances of 'Product',
                # as a filter to discard products with missing values
                try:
                    # try to create an instance of class 'Product' with every required value
                    product = Product(
                            name=outline['product_name_fr'],
                            nutriscore=outline['nutriscore_score'],
                            url=outline['url'],
                            categories=outline['categories'],
                            stores=outline['stores']
                    )

                    # if a value is empty, discard this product and jump to the next
                    if any(product.get_values()) == "":
                        raise KeyError

                # if a value is missing, discard this product and jump to the next
                except KeyError:
                    continue

                # if no exception is raised,
                # this instance of product is not discarded and it is added to the list
                # the else clause is a follow-up to the successfull execution of the try clause
                else:
                    self.products.append(product)

            # if the product has no categories in french,
            # discard it and continue to the next product
            else:
                continue

        return self.products

    def download_data(self):
        pass

#     # method used only for the development
#     def set_category_instances(self):
#         """Create a list with every instances of 'Category'.
#
#         Iterate on a method of class Product.
#         """
#
#         for p in self.products:
#             self.categories += p.categories
#         return self.categories
#
#     # method used only for the development
#     def set_category_census(self):
#         """Create an object listing every instances of 'Category'
#
#         with no duplicates,
#         and with a listing per category of every product related to them.
#         """
#
#         # launch the method 'set_category_instances' to ensure that 'self.categories' is ready
#         self.set_category_instances()
#         # ensure that the variable 'self.category_census' is clean
#         self.category_census = []
#
#         # create a list with the name of the categories (without duplicates)
#         cat_set = sorted(set([cat.name for cat in self.categories]))
#
#         # use the listing of category names to set the loop
#         for cat in cat_set:
#
#             # initiate a list to save every instance of Product related to this category name
#             cat_prods = []
#
#             # loop over the elements of self.categories to catch every occurence of this category name
#             for c in self.categories:
#                 if str(cat) == c.name:
#                     # catch each instance of Product associated with an occurence of this category name
#                     cat_prods.append(c.products)
#
#             # modify the list cat_prods to improve it (sort it by the name of the products and discard the duplicates)
#             cat_prod_set = sorted(list(set(cat_prods)), key=lambda prod: prod.name)
#             # create an instance of this category (and attach the related instances of product)
#             case = Category(name=str(cat), products=cat_prod_set)
#
#             # add this instance of Category to the listing of categories
#             self.category_census.append(case)
#
#         return self.category_census
#
#     # method used only for the development
#     def set_store_instances(self):
#         """Create a list with every instances of 'Store'.
#
#         Iterate on a method of class Product.
#         """
#
#         for p in self.products:
#             self.stores += p.stores
#         return self.stores
#
#     # method used only for the development
#     def set_store_census(self):
#         """Create an object listing every instances of 'Store'
#
#         with no duplicates,
#         and with a listing per category of every product related to them.
#         """
#
#         # launch the method 'set_store_instances' to ensure that 'self.stores' is ready
#         self.set_store_instances()
#         # ensure that the variable 'self.category_census' is clean
#         self.store_census = []
#
#         # create a list with the name of the stores (without duplicates)
#         shop_set = sorted(set([shop.name for shop in self.stores]))
#
#         # use the listing of store names to set the loop
#         for shop in shop_set:
#
#             # initiate a list to save every instance of Product related to this store name
#             shop_prods = []
#
#             # loop over the elements of self.stores to catch every occurence of this store name
#             for s in self.stores:
#                 if str(shop) == s.name:
#                     # catch each instance of Product associated with an occurence of this store name
#                     shop_prods.append(s.products)
#
#             # modify the list shop_prods to improve it (sort it by the name of the products and discard duplicates)
#             shop_prod_set = sorted(list(set(shop_prods)), key=lambda prod: prod.name)
#             # create an instance of this store (and attach the related instances of product)
#             showcase = Store(name=str(shop), products=shop_prod_set)
#
#             # add this instance of Store to the listing of stores
#             self.store_census.append(showcase)
#
#         return self.store_census

#     # method used only for the development
#     def test_status(self):
#         """Print the status code of the response."""
#
#         response = requests.get(self.url, params=self.parameters)
#
#         if response is None:
#             return "The request has yet to be made."
#
#         else:
#             return "status code of the API: {}".format(str(response.status_code))
#
#     # method to be developed (if needed)
#     def call_db(self):
#         # use self.products when it is full
#         pass
#
#         # BROUILLONS
#         # objets = []
#         # for p in range(1, page_number + 1):
#         #     # iterate on the method, by modifying the parameter 'page'
#         #     self.parameters["page"] = p
#         #     answer = requests.get(self.url, params=self.parameters)
#         #     recupère le json dans answzer.request
#         #     for chaque obket dans la listye json:
#         #         try:
#         #           objet = Product(info 1, info 2 info 3)
#         #           ajouter l'objet a la liste'
#         #         except ERREUR:
#         #           continue
#         # apelle la database en lui envoyant la liste d'objets
#
#         # self.responses.append(answer)
#
#         # self.parameters["page"] = page_number
#         # # cancel the modifications made to the variable 'page'
#
#         # return self.responses


# class DataDownloader:
#     """Handle the data, and load it in a database.
#
#     - 'payload': a dictionary of products. Each product is an item (<key = int>: <value = data of one product>).
#         - 'payload' comes from DataCleaner
#     - 'db':  a connector in charge of the connection with the database.
#         - 'db' comes from DBManager in Model.Manager.db_manager
#     - 'manager': an entity manager handling the sql queries to interact with the databse.
#         - 'manager' comes from EntityManager in Model.Manager.entity_manager
#
#     Process to load the data:
#     1. for each product, as a dictionary in 'payload':
#         1.1. create an instance of class 'Product'
#         1.2. call the instance of 'Product' with the entity_manager to create a new row in the table 'product'
#         1.3. for each category referenced in the attribute 'categories' of the instance 'Product':
#             - test if an instance of class 'Category' has already been created for this category:
#                 - if it exists:
#                     - modify the attribute 'products' in this instance of 'Category',
#                         to add the name of this instance of 'Product' in the list
#                 - if it doesn't exist yet:
#                     - create an instance of this category,
#                         with the name of this instance 'Product' referenced in its attribute 'products'
#         1.4. for each store referenced in the attribute 'store' of the instance 'Product':
#             - test if an instance of class 'Store' has already been created for this store:
#                 - if it exists:
#                     - modify the attribute 'products' in this instance of 'Store',
#                         to add the name of this instance of 'Product' in the list
#                 - if it doesn't exist yet:
#                     - create an instance of this store,
#                         with the name of this instance 'Product' referenced in its attribute 'products'
#     2. for each category, as an instance in memory:
#         2.1. call the instance of 'Category' with the entity_manager to create a new row in the table 'category'
#         2.2. for each product referenced in the attribute 'products' of this instance of 'Category':
#             - use the entity_manager to create a new row in the table 'category_product',
#                 which associates the id of this instance of 'Category', and the id of this instance of 'Product'
#     3. for each store, as an instance in memory:
#         3.1. call the instance of 'Store' with the entity_manager to create a new row in the table 'store'
#         3.2. for each product referenced in the attribute 'products' of this instance of 'Store':
#             - use the entity_manager to create a new row in the table 'store_product',
#                 which associates the id of this instance of 'Store', and the id of this instance of 'Product'
#     """
#
#     def __init__(self, db, entity, payload):
#
#         self.db = db  # db connector from DBManager (Model.Manager.db_manager)
#         self.entity = entity  # entity manager from EntityManager (Model.Manager.entity_manager)
#         self.payload = payload  # payload is self.products from APICaller
#         self.statements = dict()
#
#     def build_statements(self):
#         """Create a compilation of statements, as a dictionary.
#
#         Use a recursive function to create the components of the dictionary statement,
#         from  a list of instances of an entity.
#         """
#
#         stm = {
#                 'product': [],
#                 'category': [],
#                 'store': []
#         }
#
#         def fill_statement(element, statement):
#             """Recursive function to create the components of the dictionary statement."""
#             for e in element:
#                 # initiate the dict that will contain the values for one of the entity instances
#                 # it will be used to insert one of the rows in the db
#                 row = dict()
#                 # split names and values of the attributes of a class, to use them separately
#                 for k, v in e.__dict__.items():
#                     # the attribute is not used if it has no values
#                     if v is None:
#                         pass
#                     # launch the next layer to the recursion, if the attribute contains a list
#                     # it is interpreted as a pathway to develop one of the other statements
#                     elif type(v) is list:
#                         fill_statement(v, statement)
#                     # stop the recursion at this layer
#                     # add the (key, value) as a new item to the row
#                     elif isinstance(v, Product):
#                         row[str(k)] = v.name
#                     else:
#                         row[str(k)] = v
#                 # add the row
#                 statement[str(e.__class__.__name__.lower())].append(row)
#
#             return statement
#
#         # launch the recursive call to the function
#         fill_statement(self.payload, stm)
#
#         return stm
#
#     def insert_data(self):
#
#         self.statements = self.build_statements()
#
#         self.entity.multiple_insert(self.statements)
#
#     def register_data(self):
#
#         dict_products = {}  # dictionary listing every product
#         dict_categories = {}  # dictionary listing every category
#         dict_stores = {}  # dictionary listing every store
#
#         count_categories = 1  # incremented count that will serves as id in dict_categories
#         count_stores = 1  # incremented count that will serves as id in dict_stores
#
#         for p in self.payload:
#
#             # register the product as an entry in dict_products
#             dict_products[p] = {
#                     'id': p,
#                     'name': p['product_name_fr'],
#                     'nutriscore': p['nutriscore_score'],
#                     'url': p['url']
#             }
#
#             # register the category as an entry in dict_categories
#             for c in p['categories_tags']:
#
#                 # verify if the category has already been registered in the dedicated dictionary
#                 if c not in dict_categories.keys():
#                     # register the category as an entry in dict_categories
#                     dict_categories[c] = {
#                             'id': count_categories,
#                             'name': c,
#                             'products': list(p['product_name_fr'])
#                     }
#                     count_categories += 1
#                 else:
#                     # this category is already registered in the dictionary
#                     # update its entry, to associate the name of the related product to this category
#                     dict_categories[c]['products'].append(p['product_name_fr'])
#
#             # register the store as an entry in dict_stores
#             for s in p['stores_tags']:
#
#                 # verify if the store has already been registered in the dedicated dictionary
#                 if s not in dict_stores.keys():
#                     # register the category as an entry in dict_categories
#                     dict_stores[s] = {
#                             'id': count_stores,
#                             'name': s,
#                             'products': list(p['product_name_fr'])
#                     }
#                     count_stores += 1
#                 else:
#                     # this store is already registered in the dictionary
#                     # update its entry, to associate the name of the related product to this store
#                     dict_stores[s]['products'].append(p['product_name_fr'])
#
#         return dict_products, dict_categories, dict_stores
#
#     def download_products(self, table_name, col_names, val_names, values):
#         self.entity.save_data(table_name, col_names, val_names, values)
#
#     def download_categories(self):
#         pass
#
#     def download_stores(self):
#         pass
#
#     def download_product_to_category(self):
#         pass
#
#     def download_product_to_store(self):
#         pass
