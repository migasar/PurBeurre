""" Create an object 'Product' to carry the data of the products. """


class Product:
    """Create an object describing one product"""

    def __init__(self, name, nutriscore, code, categories, stores, url, id=None):

        self.id = id
        self.name = name

        self.nutriscore = nutriscore
        self.code = code
        self.url = url
        self.categories = []
        # for cat in categories.split(',')
        #   try:
        #       cat = Categorie(name)
        #       ajouter la categorie à self.categories

        # self.categories = categories
        # self.stores = stores

    def view_name(self):
        return self.__class__.__name__.lower()

    def view_attributes(self):
        return self.__dict__.keys()


# protest = Product(1, 'foo', 2, ['bar'], ['ham'])
#
# print(f" name of class : {protest.view_name()}")
# print(f"list of attributes : {protest.view_attributes()}")
#
# print(type(protest.__dict__.keys()))
#
# for i in protest.__dict__.keys():
#     print(type(i))

