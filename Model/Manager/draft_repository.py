"""
Handle the interaction of the database with the program.
Collect specified elements of the data from the database,
and bring it as suitable python objects.

Part of the ORM (object-relational mapping) :
The ORM handles every transaction between the database of the program and the other elements of the program.
Every coding elements with SQL should be regrouped in the ORM.
"""


class ProductManager:
    """
    Handle the interactions with the database,
    and give methods to save and search based on various criteria.
    """

    def __init__(self):
        pass
    pass


class Product:  # mentored
    """
    Describe a product,
    and deal with the methods regarding an unique product.
    """

    def __init__(self):
        self.category = None

    def get_category(self):
        """Select the category of the product. """
        if self.category is None:
            pass
        return self.category


class CategoryManager:
    """
    Handle the interactions with the database,
    and give methods to save and search based on various criteria.
    """

    def __init__(self):
        pass
    pass


class Category:  # mentored
    """
    Describe a category,
    and deal with the methods regarding an unique category.
    """

    def __init__(self, data, id=None):
        self.id = id
        self.category_name = data[1]

    @classmethod
    def get_categories(cls):
        """Select all categories from db. """
        result = []
        categories = []
        for category in result:
            categories.append(cls(category[1:], category[0]))
        return result

    def update(self):
        """Modify the data in db. """
        cursor = DBConnector.get_instance().get_cursor()
        'UPDATE in db WHERE id = ' + self.id
        pass

    def get_products(self):
        """Select the products of the category. """
        result = 'SELECT * FROM Products WHERE category_id = ' + self.id
        products = list()
        for p in result:
            product = Product(p)
            product.category = self
            products.append(product)
        self.products = products


class StoreManager:
    """
    Handle the interactions with the database,
    and give methods to save and search based on various criteria.
    """

    def __init__(self):
        pass
    pass


class FavoriteManager:
    """
    Handle the interactions with the database,
    and give methods to save and search based on various criteria.
    """

    def __init__(self):
        pass
    pass
