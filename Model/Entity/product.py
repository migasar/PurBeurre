""" Create an object 'Product' to carry the data of the products. """


from Model.Entity.category import Category
from Model.Entity.store import Store


class Product:
    """Create an object describing one product"""

    def __init__(self, name, nutriscore, url, categories=None, stores=None, _id=None):

        self.name = name
        self.nutriscore = nutriscore
        self.url = url

        self.categories = self.set_categories(categories)
        self.stores = self.set_stores(stores)

        self._id = _id

    @staticmethod
    def set_categories(categories, product=None):
        """Modify the initiation of the attribute depending on its source.

        Create a list of instances of 'Category' from a long string,
        or retrieve a list of instances if they have already been initiated.
        """

        if len(categories) == 0:
            # test if the variable is empty
            raise KeyError

        elif type(categories) is str:
            # create a list of instances

            cats = []
            for cat in categories.split(','):

                # use try/except when we create instances of 'Category',
                # as a filter to discard categories with missing values
                try:
                    # try to create an instance of class 'Category' with required values
                    category = Category(
                            name=str(cat).strip(),
                            products=product
                    )
                    # if a value is empty, discard this category and jump to the next
                    if category.name == "":
                        raise KeyError
                # if a value is missing, discard this category and jump to the next
                except KeyError:
                    continue

                # if no exception is raised,
                # this instance of category is not discarded and it is added to the list
                # the else clause is a follow-up to the successfull execution of the try clause
                else:
                    cats.append(category)

            return cats

        else:
            # assume that the instances have been initiated
            return categories

    @staticmethod
    def set_stores(stores, product=None):
        """Modify the initiation of the attribute depending on its source.

        Create a list of instances of 'Store' from a long string,
        or retrieve a list of instances if they have already been initiated.
        """

        if len(stores) == 0:
            # test if the variable is empty
            raise KeyError

        elif type(stores) is str:
            # create a list of instances

            shops = []
            for shop in stores.split(','):

                # use try/except when we create instances of 'Store',
                # as a filter to discard stores with missing values
                try:
                    # try to create an instance of class 'Store' with required values
                    store = Store(
                            name=str(shop).strip(),
                            products=product
                    )
                    # if a value is empty, discard this store and jump to the next
                    if store.name == "":
                        raise KeyError
                # if a value is missing, discard this store and jump to the next
                except KeyError:
                    continue

                # if no exception is raised,
                # this instance of store is not discarded and it is added to the list
                # the else clause is a follow-up to the successfull execution of the try clause
                else:
                    shops.append(store)

            return shops

        else:
            # assume that the instances have been initiated
            return stores

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"({', '. join([str(v) for v in self.__dict__.values()])})")

    def get_headers(self):

        headers = tuple([k for k, v in self.__dict__.items() if v is not None and type(v) is not list])
        return headers

    def get_values(self):

        values = [
                v if type(v) is not list else [
                        str(x) for x in v
                ] for v in self.__dict__.values() if v is not None
        ]
        # values = [
        #         v if type(v) is not list else [
        #                 x for x in v
        #         ] for v in self.__dict__.values() if v is not None
        # ]
        return values

    def get_row(self):

        row_listing = [
                self.__class__.__name__,
                self.get_headers(),
                self.get_values()
        ]
        return row_listing


