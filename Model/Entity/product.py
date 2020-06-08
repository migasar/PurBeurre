""" Create an object 'Product' to carry the data of the products. """


class Product:
    """Create an object describing one product"""

    def __init__(self, table_name='product', id=None, **kwargs):

        self.table_name = table_name
        self.id = id

        self.name = name
        self.score = score
        self.url = url
        self.description = description
        self.categories = categories
        self.stores = stores

    # objects = ProductRepository()
    # objects.get_all() # to call all the instances of product from ProductRepository

    # methods to be dev in the class ProductRepository :
    # def get_all(self):
    #     pass
    #
    # def get_all_by_category(self, category):
    #     pass
    #
    # def get_all_by_store(self, store):
    #     pass
    #
    # def get_all_with_score_larger_than(self, score):
    #     pass
    #
    # def get_unhealthy_products_by_category(self, category):
    #     pass
    #
    # def save(self, product):
    #     pass
    #
    # def create(self,
    #            name=None,
    #            score=None,
    #            description=None,
    #            url=None,
    #            categories=None,
    #            stores=None
    #            ):
    #     pass
