# CREATE DATABASE

CREATE_DB_PURBEURRE = " CREATE DATABASE IF NOT EXISTS `purbeurre` DEFAULT CHARACTER SET utf8 ; "
CREATE_DB = " CREATE DATABASE IF NOT EXISTS "


# CREATE TABLES

# Create one of the main table : 'product'
CREATE_TABLE_PRODUCT = """
DROP TABLE IF EXISTS `purbeurre`.`product` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(250) NULL,
  `description` LONGTEXT NULL,
  `nutriscore` INT NULL,
  `off_url` VARCHAR(500) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
"""

# Create one of the main table : 'category'
CREATE_TABLE_CATEGORY = """
DROP TABLE IF EXISTS `purbeurre`.`category` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(250) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
"""

# Create one of the main table : 'store'
CREATE_TABLE_STORE = """
DROP TABLE IF EXISTS `purbeurre`.`store` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`store` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `store_name` VARCHAR(250) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
"""


# Create a (sort of) table of association : 'favorite'
CREATE_TABLE_FAVORITE = """
DROP TABLE IF EXISTS `purbeurre`.`favorite` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`favorite` (
  `old_product_id` INT NOT NULL,
  `substitute_product_id` INT NOT NULL,
  INDEX `fk_favorite_product1_idx` (`old_product_id` ASC),
  INDEX `fk_favorite_product2_idx` (`substitute_product_id` ASC),
  PRIMARY KEY (`old_product_id`, `substitute_product_id`),
  CONSTRAINT `fk_favorite_product1`
    FOREIGN KEY (`old_product_id`)
    REFERENCES `purbeurre`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_favorite_product2`
    FOREIGN KEY (`substitute_product_id`)
    REFERENCES `purbeurre`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
"""

# Create a table of association : 'product_category'
CREATE_TABLE_PROD_CATEGORY = """
DROP TABLE IF EXISTS `purbeurre`.`product_category` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`product_category` (
  `product_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  INDEX `fk_product_category_category_idx` (`category_id` ASC),
  INDEX `fk_product_category_product1_idx` (`product_id` ASC),
  PRIMARY KEY (`product_id`, `category_id`),
  CONSTRAINT `fk_product_category_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `purbeurre`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_category_product1`
    FOREIGN KEY (`product_id`)
    REFERENCES `purbeurre`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
"""

# Create a table of association : 'product_store'
CREATE_TABLE_PROD_STORE = """
DROP TABLE IF EXISTS `purbeurre`.`product_store` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`product_store` (
  `product_id` INT NOT NULL,
  `store_id` INT NOT NULL,
  INDEX `fk_product_store_store1_idx` (`store_id` ASC),
  INDEX `fk_product_store_product1_idx` (`product_id` ASC),
  PRIMARY KEY (`product_id`, `store_id`),
  CONSTRAINT `fk_product_store_store1`
    FOREIGN KEY (`store_id`)
    REFERENCES `purbeurre`.`store` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_store_product1`
    FOREIGN KEY (`product_id`)
    REFERENCES `purbeurre`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
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


# 2nd approach : Insert info with the method cursor.executemany()
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

