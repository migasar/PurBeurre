""" Repository of all SQL queries

(except for the schema to create the database)
"""

# INSERT QUERIES

PRODUCT_TABLE = "product"
PRODUCT_VARIABLES = "(id, name, score, url, description)"
PRODUCT_VALUES = "(%(id)s, %(name)s, %(score)s, %(url)s, %(description)s)"

CATEGORY_TABLE = "category"
CATEGORY_VARIABLES = "(id, name)"
CATEGORY_VALUES = "(%(id)s, %(name)s)"

STORE_TABLE = "store"
STORE_VARIABLES = "(id, name)"
STORE_VALUES = "(%(id)s, %(name)s)"

FAVORITE_PRODUCT_TABLE = "favorite_product"
FAVORITE_PRODUCT_VARIABLES = "(base_product_id, substitute_product_id)"
FAVORITE_PRODUCT_VALUES = "(%(base_product_id)s, %(substitute_product_id)s)"

CATEGORY_PRODUCT_TABLE = "category_product"
CATEGORY_PRODUCT_VARIABLES = "(category_id, product_id)"
CATEGORY_PRODUCT_VALUES = "(%(category_id)s, %(product_id)s)"

STORE_PRODUCT_TABLE = "store_product"
STORE_PRODUCT_VARIABLES = "(store_id, product_id)"
STORE_PRODUCT_VALUES = "(%(store_id)s, %(product_id)s)"


# ADD_PRODUCT = (
#         """
#         INSERT INTO product (id, name, score, url, description)
#         VALUES (:id, :name, :score, :url, :description)
#         """
# )

# EXAMPLE OF THIS SYNTAX FOR THE INSERTION
# data = {
#     "id": ...,
#     "col1": ...,
#     "col2":...
# }
# db.query(
#     """
#     INSERT INTO mytable (id, col1, col2)
#     VALUES (:id, :col1, :col2)
#     """,
#     **data
# )
