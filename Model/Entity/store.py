""" Create an object 'Store' to carry the data of the stores. """


class Store:
    """Create an object describing one store"""

    def __init__(self, name, products=None, _id=None):

        self.name = name
        self.products = products
        self._id = _id

    # def __repr__(self):
    #     """Create a more usable representation of the object.
    #
    #     The idea with this representation is to call a string similar to the command used to instanciate the object.
    #     """
    #
    #     values_list = [("'"+str(v)+"'") for v in self.__dict__.values() if v is not None]
    #
    #     return (f"{self.__class__.__name__}"
    #             f"({', '. join([v for v in values_list])})")

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

        values = [
                v if type(v) is not list else [
                        x for x in v
                ] for v in self.__dict__.values() if v is not None
        ]

        return values
