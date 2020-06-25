""" Create an object 'Store' to carry the data of the stores. """


class Store:
    """Create an object describing one store"""

    def __init__(self, name, products=None, id=None):

        self.id = id
        self.name = name
        self.products = products

    def view_name(self):
        return self.__class__.__name__.lower()

    def view_attributes(self):
        return self.__dict__.keys()
