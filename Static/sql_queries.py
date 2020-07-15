""" Repository of all SQL queries

(except for the schema to create the database)
"""

# INSERT QUERIES

PRODUCT_TABLE = "product"
PRODUCT_VARIABLES = "(product_id, name, score, url, description)"
PRODUCT_VALUES = "(%(product_id)s, %(name)s, %(score)s, %(url)s, %(description)s)"

CATEGORY_TABLE = "category"
CATEGORY_VARIABLES = "(product_id, name)"
CATEGORY_VALUES = "(%(product_id)s, %(name)s)"

STORE_TABLE = "store"
STORE_VARIABLES = "(product_id, name)"
STORE_VALUES = "(%(product_id)s, %(name)s)"

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
#         INSERT INTO product (product_id, name, score, url, description)
#         VALUES (:product_id, :name, :score, :url, :description)
#         """
# )

# EXAMPLE OF THIS SYNTAX FOR THE INSERTION
# data = {
#     "product_id": ...,
#     "col1": ...,
#     "col2":...
# }
# db.query(
#     """
#     INSERT INTO mytable (product_id, col1, col2)
#     VALUES (:product_id, :col1, :col2)
#     """,
#     **data
# )
