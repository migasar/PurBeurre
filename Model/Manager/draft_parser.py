"""
Handle a JSON object to structure it and to manipulate its content
"""


from Model.Manager.api_manager import cargo, manifest


# Create a list with products to filter payload
# the object "products_list" is a list
# but each one of the elements in the list is a dictionary
products_list = cargo['products']
product_elements = products_list[0]

categories_list = manifest['tags']
category_elements = categories_list[0]


# Create a dictionary of keys containing 'name' in them, and their values
dict_with_name = dict()
for k in product_elements:
    if 'name' in str(k):
        k_duplicate = k
        dict_with_name[k_duplicate] = product_elements[k]

# Create a dictionary of keys containing 'category' in them, and their values
dict_with_category = dict()
for k in product_elements:
    if 'cate' in str(k):
        k_duplicate = k
        dict_with_category[k_duplicate] = product_elements[k]

# Create a dictionary of keys containing 'lang' or 'fr' in them, and their values
dict_with_lang = dict()
for k in product_elements:
    if ('lang' or 'fr') in str(k):
        k_duplicate = k
        dict_with_lang[k_duplicate] = product_elements[k]


# Create a list of products with their names in French, by refining "products_list"
products_french = [
    product for product in products_list if 'product_name_fr' in product.keys()]


class DataCleaner:
    """
    Handle a JSON object to structure it and to manipulate its content
    """

    def __init__(self, dump):
        self.dump = dump
        self.payload = None

    def slice_dump(self, keeper):
        self.payload = self.dump[keeper]
        return self.payload

    def refine_data(self, *giver):
        for piece in giver:
            try:
                pass
            except foo as bar:
                pass
            pass
    pass
