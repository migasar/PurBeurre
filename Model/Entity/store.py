""" Create an object 'Store' to carry the data of the stores. """

from Model.Entity.product import Product

from Model.Manager.entity_manager import EntityManager


class Store:
    """Create an object describing one store"""

    # Class variable
    entity_manager = EntityManager()

    def __init__(self, name, products=None, id_store=None):

        self.name = name
        self.products = products
        self.id_store = id_store

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
                f"({', '. join([v for v in values_list])})")

    def get_products(self):

        if self.products is None:

            # Create an empty list in stores
            self.products = []

            # Components of the query to retrieve the ids of the products, from the store
            anchor = 'product'
            selection = 'product.id_product, product.name'
            components = {
                'join': {
                        'table_adjunct': 'store_product',
                        'row_key': 'id_store'
                },
                'where': {
                    'table_adjunct': 'store_product',
                    'row_key': 'id_store',
                    'row_value': self.id_store,
                }
            }

            # Launch the query to retrieve the ids of the products, from this store
            production = self.entity_manager.read_row(
                    table_anchor=anchor,
                    selection=selection,
                    **components
            )

            for prod_row in production:
                for prod_id in prod_row:
                    if type(prod_id) is int:
                        self.products.append(Product.from_db(id_product=prod_id))

            # prod_anchor = 'store'
            # prod_selection = 'store.id_store, store.name'
            # # Retrieve the attributes of each store from its id
            # for prod in production:
            #     prod_components = {
            #             'where': {
            #                     'table_adjunct': 'product',
            #                     'row_key': 'id_store',
            #                     'row_value': prod
            #             }
            #     }
            #
            #     # Send the query
            #     prod_row = self.entity_manager.read_row(
            #             table_anchor=prod_anchor, selection=prod_selection, **prod_components
            #     )
            #     for prow in prod_row:
            #         # Create an instance with the result of the query
            #         prod_instance = Store(
            #                 id_store=int(prow[0]),
            #                 name=str(prow[1])
            #         )
            #         # Add the instance to the list of categories related to this product
            #         self.products.append(prod_instance)

        return self.products

    def get_headers(self):
        """Create a list with the name of attributes (which are not empty).

        It will be used as a parameter in the creation of queries (as a string of column names)."""

        return [
                k
                for (k, v) in self.__dict__.items()
                if type(v) is not list and v is not None and k != 'entity_manager'
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

    def get_items(self):
        """Create a list of tuples with the name and the value of each attribute (which are not empty)."""

        return [
                (k, v)
                if type(v) is not list
                else (k, [x for x in v])
                for (k, v) in self.__dict__.items()
                if v is not None and k != 'entity_manager'
        ]
