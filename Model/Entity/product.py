""" Create an object 'Product' to carry the data of the products. """


from Model.Entity.category import Category
from Model.Entity.store import Store


class Product:
    """Create an object describing one product"""

    def __init__(self, name, brands, nutriscore, code, url, categories=None, stores=None, id=None):

        self.id = id
        self.name = name
        self.brands = brands

        self.nutriscore = nutriscore
        self.code = code
        self.url = url

        self.categories = categories
        # for cat in categories.split(',')
        #   try:
        #       cat = Categorie(name)
        #       ajouter la categorie à self.categories

        self.stores = stores

    @staticmethod
    def get_categories(categories, product=None):
        """Create a list of instances of 'Category' and append the list to 'self.categories'."""

        cats = []
        for cat in categories.split(','):
            try:
                category = Category(
                        name=str(cat).strip(),
                        products=product
                )
                cats.append(category)
            except KeyError:
                continue
        return cats

    @staticmethod
    def get_stores(stores, product=None):
        """Create a list of instances of 'Store' and append the list to 'self.stores'."""

        shops = []
        for shop in stores.split(','):
            try:
                store = Store(
                        name=str(shop).strip(),
                        products=product
                )
                shops.append(store)
            except KeyError:
                continue
        return shops

    def view_name(self):
        return self.__class__.__name__.lower()

    def view_attributes(self):
        return self.__dict__.keys()
