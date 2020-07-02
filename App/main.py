"""In charge of the launch of the program.

Call all the elements of the program in an orchestrated manner.
"""

import os
import json

from Model.Entity.category import Category
from Model.Entity.product import Product
from Model.Entity.store import Store

from Model.Manager.api_manager import APIManager
from Model.Manager.db_manager import DBManager
from Model.Manager.entity_manager import EntityManager

import Static.credential as credential
import Static.constant as constant
import Static.sql_queries as queries


#  DB CONNECTION
def create_database():

    # CREATE DATABASE
    db_builder = DBManager()
    db_builder.build_database()
    print("db created !")

    return db_builder


#  API CALL
def call_api():

    # CREATE API
    api_caller = APIManager()
    print("api created !")
    api_caller.get_data()
    print("request executed !")

    return api_caller


#  ENTITY INTERACTION
def create_entity(db_manager):

    # CREATE ENTITY MANAGER
    entity_manager = EntityManager(db_manager)
    print("entity manager created !")

    return entity_manager


#  DATA DOWNLOAD
def download_data(api_manager, entity_manager):

    # SAVE DATA IN DB
    api_manager.download_data(entity_manager)
    print("data saved in db !")

    return api_manager


#  MAIN
def main():
    """Launch the program by calling the first modules of its internal process"""

    ###########
    # ACTIONS #
    ###########
    db = create_database()
    api = call_api()

    entity = create_entity(db)
    download = download_data(api, entity)

    #########
    # TESTS #
    #########

    # DB #
    print(f"type of db: {type(db)}")
    print(f"db class name: {db.__class__.__name__}")

    # ENTITY #
    print(f"type of entity: {type(entity)}")
    print(f"entity class name: {entity.__class__.__name__}")
    # print(f"type of entity.database: {type(entity.database)}")
    # print(f"type of entity.connection: {type(entity.connection)}")
    # print(f"type of entity.cursor: {type(entity.cursor)}")

    # API #
    print(f"type of API: {type(api)}")
    print(f"api class: {api.__class__.__name__}")
    print(f"api attributes: {api.__dict__.keys()}")

    # API PRODUCTS
    print(f"type of api.products: {type(api.products)}")
    print(f"length of api.products: {len(api.products)}")
    # for prod in api.products:
    #     print(f"name: {prod.name}")
    #     print(f"categories: {prod.categories}")
    #     print(f"number of categories: {len(prod.categories)}")
    #     print(f"categories: {[cat.name for cat in prod.categories]}")

    # API CATEGORIES
    # print(f"length of api.categories: {len(api.categories)}")
    # for i in api.categories:
    #     print(f"{i.name}: {i.products}")
    # print(f"api.category[0] attributes: {api.categories[0].__dict__}")

    # API STORES
    # print(f"length of api.stores: {len(api.stores)}")
    # for i in api.stores:
    #     if len(i.name) == 0:
    #         print("!! Lost !!")
    #     print(i.name)

    # SQL #

    # CHECK TABLES
    # db.cursor.execute("SHOW TABLES")
    # tables = db.cursor.fetchall()
    # print("DB tables:")
    # for table in tables:
    #     print(table)
    # py_tables = [tab[0] for tab in tables]
    # print(f"tables: {py_tables}")

    # CHECK COLUMNS IN TABLES
    # db.cursor.execute("DESC product")
    # prod_columns = db.cursor.fetchall()
    # print(prod_columns)
    # for column in prod_columns:
    #     print(column)

    # INSERT PRODUCT IN DB
    # product_data = {
    #         'id': 1,
    #         'name': 'nutella',
    #         'brand': 'ferrero',
    #         'score': 7,
    #         'url': 'url_text',
    #         'description': 'description_text'
    #                 }
    # entity.create_data(queries.PRODUCT_TABLE, queries.PRODUCT_VARIABLES, queries.PRODUCT_VALUES, product_data)
    # print(db.cursor.rowcount, " product inserted !")

    # CHECK PRODUCTS IN TABLE
    # query = "SELECT * FROM product"
    # db.cursor.execute(query)
    # records = db.cursor.fetchall()
    # print("records: ")
    # print(records)

    # LIST COMPREHENSION #
    # sample = ['en:breakfasts', 'en:spreads', 'en:sweet-spreads', 'fr:pates-a-tartiner']
    # extraction = [sam[3:] for sam in sample if ('fr' in sam)]
    # print(f"extraction: {extraction}")

    # STRINGS #
    # print(f"my list: {', '.join(['%s'] * 5)}")
    # my_dict = {
    #         'a': [1, 2],
    #         'b': [3, 4],
    #         'c': [5, 6]
    # }

    # fields = ', '.join(my_dict.keys())
    # values = ', '.join(['%%(%s)s' % x for x in my_dict])
    # query = f"INSERT INTO some_table (%s) VALUES (%s)" % (fields, values)
    # print(f"query: {str(query)}")
    # valco = ', '.join([f'%({x})s' for x in my_dict])
    # print(f"valco: {valco}")

    ############
    ############


if __name__ == "__main__":
    main()
