""" Create an object 'Category' to carry the data of the categories. """


class Category:
    """Create an object describing one category"""

    def __init__(self, name, products=None, id=None):

        self.id = id
        self.name = name
        self.products = products

    def view_name(self):
        return self.__class__.__name__.lower()

    def view_attributes(self):
        return self.__dict__.keys()
