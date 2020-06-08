""" Create an object 'Store' to carry the data of the stores. """


class Store:
    """Create an object describing one store"""

    def __init__(self, table_name='store', id=None, **kwargs):

        self.table_name = table_name
        self.id = id

        self.name = name
        self.products = products
