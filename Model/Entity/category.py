""" Create an object 'Category' to carry the data of the categories. """


class Category:
    """Create an object describing one category"""

    def __init__(self, table_name='category', id=None, **kwargs):

        self.table_name = table_name
        self.id = id

        self.name = name
        self.products = products
