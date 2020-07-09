""" Create an object 'Product' to carry the data of the products. """

from Model.Entity.category import Category
from Model.Entity.store import Store


class Product:
    """Create an object describing one product."""

    def __init__(self, name, nutriscore, url, categories=None, stores=None, _id=None):

        self.name = name
        self.nutriscore = nutriscore
        self.url = url
        self.categories = self.set_categories(categories)
        self.stores = self.set_stores(stores)
        self._id = _id

    def __repr__(self):
        """Create a more usable representation of the object.

        The idea with this representation is to call a string similar to the command used to instanciate the object.
        """

        values_list = [("'" + str(v) + "'") for v in self.__dict__.values() if v is not None]
        return (f"{self.__class__.__name__}"
                f"({', '.join([v for v in values_list])})")

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
                # this instance is added to the list, if no exception is raised
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
                # this instance is added to the list, if no exception is raised
                else:
                    shops.append(store)

            return shops

        else:
            # assume that the instances have been initiated
            return stores

    def get_headers(self):
        """Create a tuple with the name of attributes (which are not empty).

        It will be used as a parameter in the creation of queries (as a string of column names)."""

        headers = tuple([k for k, v in self.__dict__.items() if v is not None and type(v) is not list])
        if len(headers) == 1:
            headers = ("("+str(headers[0])+")")

        return headers

    def get_values(self):
        """Create a list with the values of attributes (which are not empty).

        It will be used as a parameter in the creation of queries (as a row of values)."""

        # values = [
        #         v if type(v) is not list else [
        #                 str(x) for x in v
        #         ] for v in self.__dict__.values() if v is not None
        # ]

        values = [
                v if type(v) is not list else [
                        x for x in v
                ] for v in self.__dict__.values() if v is not None
        ]

        return values
