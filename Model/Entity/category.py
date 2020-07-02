""" Create an object 'Category' to carry the data of the categories. """


class Category:
    """Create an object describing one category"""

    def __init__(self, name, products=None, _id=None):

        self.name = name
        self.products = products
        self._id = _id

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"({', '. join([str(v) for v in self.__dict__.values()])})")

    def __str__(self):
        return f"{self.name}"
