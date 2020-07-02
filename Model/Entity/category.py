""" Create an object 'Category' to carry the data of the categories. """


class Category:
    """Create an object describing one category"""

    def __init__(self, name, products=None, _id=None):

        self.name = name
        self.products = products
        self._id = _id

    def __repr__(self):
        """Create a more usable representation of the object.

        The idea with this representation is to call a string similar to the command used to instanciate the object.
        """

        return (f"{self.__class__.__name__}("
                f"({', '. join([str(v) for v in self.__dict__.values()])})")

    def __str__(self):
        """Create a more readable string representation of the object.

        The idea with this string method is to print a representation with just the name attribute of the instance/
        """

        return f"{self.name}"
