# CREATE DATABASE

CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS pur_beurre"
CREATE_DB = "CREATE DATABASE IF NOT EXISTS "


# CREATE TABLES

# Create one of the main table : 'product'
CREATE_TABLE_PRODUCT = """
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT,
    product_name VARCHAR(250) NOT NULL, 
    description TEXT, 
    nutriscore INT NOT NULL, 
    off_url VARCHAR(500),
    PRIMARY KEY (id)
) ENGINE = InnoDB
"""

# Create one of the main table : 'category'
CREATE_TABLE_CATEGORY = """
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT,
    category_name VARCHAR(250) NOT NULL, 
    count INT NOT NULL,
    PRIMARY KEY (id)
) ENGINE = InnoDB
"""

CREATE_TABLE_PROD_CATEGORY = """
CREATE TABLE IF NOT EXISTS product_category (
    product_id INT NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY fk_product_id (product_id) REFERENCES product(id),
    FOREIGN KEY fk_category_id (category_id) REFERENCES category(id),
    PRIMARY KEY (product_id, category_id)
) ENGINE = InnoDB
"""


# INSERT RECORDS

# 1st aproach : Insert info in a table
# with the wrapper and the method cursor.execute()
CREATE_PRODUCTS = """
INSERT INTO 
    product (product_name, description, nutriscore, off_url)
VALUES
    ('cookie', 'miam', 5, 'somewhere'),
    ('broccoli', 'beurk', 20, 'somewhere else');
"""
# execute_query(connection, create_products)

CREATE_CATEGORIES = """
INSERT INTO
    category (category_name, count)
VALUES
    ('biscuits', 5),
    ('vegetables', 10);
"""
# execute_query(connection, create_categories)


# 2nd aproach : Insert info with the method cursor.executemany()
# which accept 2 parameters :
# 1. the query string
# 2. the list of records that you want to insert

# delete_prod_category = "DELETE FROM product_category"
# execute_query(connection, delete_prod_category)

# sql = "INSERT INTO product_category (product_id, category_id) VALUES (%s, %s)"
# val = [(1, 1), (2, 2), (1, 2)]  # if I iterates the query, it throws an error
# cursor = connection.cursor()
# cursor.executemany(sql, val)
# connection.commit()


# GENERAL METHODS

DROP_DATABASE = """DROP DATABASE purbeurre"""
DROP_DB = """DROP DATABASE"""

SHOW_DBS = """SHOW DATABASES"""
# databases = cursor.fetchall()
# print(databases)
# for database in databases:
#     print(database)

