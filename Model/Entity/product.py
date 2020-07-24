""" Create an object 'Product' to carry the data of the products. """

from Model.Entity.category import Category
from Model.Entity.store import Store
from Model.Manager.entity_manager import EntityManager


class Product:
    """Create an object describing one product."""

    # Class variable
    entity_manager = EntityManager()

    def __init__(self, id_product, name, nutriscore, url, categories=None, stores=None):

        self.id_product = id_product
        self.name = name
        self.nutriscore = nutriscore
        self.url = url
        self.categories = categories
        self.stores = stores

    def __repr__(self):
        """Create a more usable representation of the object.

        The idea with this representation is to call a string similar to the command used to instanciate the object.
        """

        values_list = [
                ("'" + str(v) + "'")
                for (k, v) in self.__dict__.items()
                if v is not None and k != 'entity_manager'
        ]

        return (f"{self.__class__.__name__}"
                f"({', '.join([v for v in values_list])})")

    @classmethod
    def from_api(
            cls, name, nutriscore, url, categories, stores, id_product=None
    ):
        instance = cls(id_product, name, nutriscore, url)
        instance.categories = instance.set_categories(categories)
        instance.stores = instance.set_stores(stores)

        return instance

    @classmethod
    def from_db(
            cls, id_product, name=None, nutriscore=None, url=None, categories=None, stores=None
    ):

        if (name or nutriscore or url) is None:
            anchor = 'product'
            selection = 'product.id_product, product.name, product.nutriscore, product.url'
            components = {
                    'where': {
                            'table_adjunct': 'product',
                            'row_key': 'id_product',
                            'row_value': id_product
                    }
            }
            results = cls.entity_manager.read_row(
                    table_anchor=anchor, selection=selection, **components
            )
            result = results[0]

            instance = cls(
                    id_product=result[0],
                    name=result[1],
                    nutriscore=result[2],
                    url=result[3]
            )
        else:
            instance = cls(
                    id_product, name, nutriscore, url, categories, stores
            )

        instance.categories = instance.get_categories()
        instance.stores = instance.get_stores()

        return instance

    @staticmethod
    def set_categories(categories, product=None):
        """Modify the initiation of the attribute depending on its source.

        Create a list of instances of 'Category' from a long string,
        or retrieve a list of instances if they have already been initiated.
        """

        # test if the variable is empty
        if len(categories) == 0:
            raise KeyError

        # test if the content of the variable is not yet an instance
        elif type(categories) is str:
            # create a list of instances
            cats = []
            for cat in categories.split(','):
                # use try/except as a filter, to discard instances of 'Category' with missing values
                try:
                    # try to create an instance of class 'Category' with required values
                    category = Category(
                            name=str(cat).strip(),
                            products=product
                    )
                    # discard this instance and jump to the next, if a value is empty
                    if category.name == "":
                        raise KeyError
                # discard this instance and jump to the next, if a value is missing
                except KeyError:
                    continue
                # finally if no exception is raised, this instance is added to the list
                else:
                    cats.append(category)
            return cats

        # assume that the instances have been initiated
        else:
            return categories

    @staticmethod
    def set_stores(stores, product=None):
        """Modify the initiation of the attribute depending on its source.

        Create a list of instances of 'Store' from a long string,
        or retrieve a list of instances if they have already been initiated.
        """

        # test if the variable is empty
        if len(stores) == 0:
            raise KeyError

        # test if the content of the variable is not yet an instance
        elif type(stores) is str:
            # create a list of instances
            shops = []
            for shop in stores.split(','):
                # use try/except as a filter, to discard instances of 'Store' with missing values
                try:
                    # try to create an instance of class 'Store' with required values
                    store = Store(
                            name=str(shop).strip(),
                            products=product
                    )
                    # discard this instance and jump to the next, if a value is empty
                    if store.name == "":
                        raise KeyError
                # discard this instance and jump to the next, if a value is missing
                except KeyError:
                    continue
                # finally if no exception is raised, this instance is added to the list
                else:
                    shops.append(store)
            return shops

        else:
            # assume that the instances have been initiated
            return stores

    def get_categories(self):

        if self.categories is None:
            # Create an empty list in categories
            self.categories = []

            # Components of the query to retrieve the ids of the categories, from the product
            anchor = 'category_product'
            selection = 'category_product.id_category'
            components = {
                    'join': {
                            'table_adjunct': 'product',
                            'row_key': 'id_product'
                    },
                    'where': {
                            'table_adjunct': 'product',
                            'row_key': 'id_product',
                            'row_value': self.id_product
                    }
            }

            # Launch the query to retrieve the ids of the categories from this product
            cats = self.entity_manager.read_row(
                    table_anchor=anchor,
                    selection=selection,
                    **components
            )

            # Retrieve the attributes of each category from its id
            cat_anchor = 'category'
            cat_selection = 'category.id_category, category.name'
            for cat in cats:
                cat_id = cat[0]
                cat_components = {
                        'where': {
                                'table_adjunct': 'category',
                                'row_key': 'id_category',
                                'row_value': cat_id
                        }
                }

                # Send the query
                cat_row = self.entity_manager.read_row(
                        table_anchor=cat_anchor, selection=cat_selection, **cat_components
                )
                for crow in cat_row:
                    # Create an instance with the result of the query
                    cat_instance = Category(
                            id_category=int(crow[0]),
                            name=str(crow[1]),
                    )
                    # Add the instance to the list of categories related to this product
                    self.categories.append(cat_instance)

        return self.categories

    def get_stores(self):

        if self.stores is None:
            # Create an empty list in stores
            self.stores = []

            # Components of the query to retrieve the ids of the stores, from the product
            anchor = 'store_product'
            selection = 'store_product.id_store'
            components = {
                    'join': {
                            'table_adjunct': 'product',
                            'row_key': 'id_product'
                    },
                    'where': {
                            'table_adjunct': 'product',
                            'row_key': 'id_product',
                            'row_value': self.id_product
                    }
            }

            # Launch the query to retrieve the ids of the stores from this product
            shops = self.entity_manager.read_row(
                    table_anchor=anchor,
                    selection=selection,
                    **components
            )

            # Retrieve the attributes of each store from its id
            shop_anchor = 'store'
            shop_selection = 'store.id_store, store.name'
            for shop in shops:
                shop_id = shop[0]
                shop_components = {
                        'where': {
                                'table_adjunct': 'store',
                                'row_key': 'id_store',
                                'row_value': shop_id
                        }
                }

                # Send the query
                shop_row = self.entity_manager.read_row(
                        table_anchor=shop_anchor, selection=shop_selection, **shop_components
                )

                for srow in shop_row:
                    # Create an instance with the result of the query
                    shop_instance = Store(
                            id_store=int(srow[0]),
                            name=str(srow[1]),
                    )
                    # Add the instance to the list of categories related to this product
                    self.stores.append(shop_instance)

        return self.stores

    def get_items(self):
        """Create a list of tuples with the name and the value of each attribute (which are not empty)."""

        return [
                (k, v)
                if type(v) is not list
                else (k, [x for x in v])
                for (k, v) in self.__dict__.items()
                if v is not None and k != 'entity_manager'
        ]

    def get_values(self):
        """Create a list with the values of attributes (which are not empty).

        It will be used as a parameter in the creation of queries (as a row of values)."""

        return [
                v
                if type(v) is not list
                else [
                    x for x in v
                ]
                for (k, v) in self.__dict__.items()
                if v is not None and k != 'entity_manager'
        ]

    def get_headers(self):
        """Create a list with the name of attributes (which are not empty).

        It will be used as a parameter in the creation of queries (as a string of column names)."""

        return [
                k
                for (k, v) in self.__dict__.items()
                if type(v) is not list and v is not None and k != 'entity_manager'
        ]
