"""In charge of the launch of the program.

Call all the elements of the program in an orchestrated manner.
"""


import os
import json

from Model.Entity.category import Category
from Model.Entity.product import Product
from Model.Entity.store import Store

from Model.Manager.api_manager import API, APICaller, DataCleaner, DataDownloader
from Model.Manager.db_manager import DBConnection, DBManager
from Model.Manager.entity_manager import EntityManager

import Static.credential as credential
import Static.constant as constant
import Static.sql_queries as queries


#  DB CONNECTION

def create_database():

    # CREATE DATABASE
    db_builder = DBManager(credential.DB_HOST, credential.DB_USER, credential.DB_PASSWORD, db_name='purbeurre')
    db_builder.build_database(constant.SCHEMA_PATH)
    print("db created !")

    return db_builder


def create_entity(db_manager):

    # CREATE ENTITY MANAGER
    entity_manager = EntityManager(db_manager)
    print("entity manager created !")

    return entity_manager


#  API CALL

def call_api():

    # CREATE API
    api_off = API(constant.OFF_URL, constant.API_PARAMETERS)
    api_caller = APICaller(api_off)
    print("api created !")
    api_caller.get_data()
    print("request executed !")

    return api_caller


def create_data_api(api_call):

    # CREATE A DATA STRUCTURE WITH AN API REQUEST
    api_request = api_call.responses
    print("Creating data container from an api request.")

    return api_request


#  DATA CLEANING

def clean_data_api(api_data):

    # EXTRACT VALUES FROM A DATA STRUCTURE
    api_clean = DataCleaner(api_data)
    print("Create object with extracted values from a file.")

    return api_clean


def create_data_json():

    # CREATE A DATA STRUCTURE WITH THE CONTENT OF A JSON FILE
    data_dump = []
    filepath = constant.JSON_PATH  # using the file 'payload.json'
    with open(filepath, encoding="utf8") as file:
        print("deserialzing !")
        json_file = json.loads(file.read())
        for p in json_file['products']:
            data_dump.append(p)
        print("Creating data container from a json file.")

    return data_dump


def clean_data(data_dump):

    # EXTRACT VALUES FROM A DATA STRUCTURE
    data_clean = DataCleaner(data_dump)
    data_clean.extract_values()
    print("Create an object with extracted values.")

    return data_clean.payload


#  DOWNLOAD

def create_downloader(db_manager, entity_manager, data_payload):

    # CREATE DATA DOWNLOADER
    data_downloader = DataDownloader(db_manager, entity_manager, data_payload)
    print("data downloader created !")

    return data_downloader


#  MAIN

def main():
    """Launch the program by calling the first modules of its internal process"""

    # ACTIONS

    db = create_database()
    entity = create_entity(db)
    api = call_api()

    # print()
    api.get_category_census()
    print(f"length of categories list: {len(api.categories)}")
    print(f"length of categories set: {len(api.category_census)}")
    # print(f"fifth element of categories set: {api.category_census[5]}")
    # print(f"category_census[5] attributes: {api.category_census[5].__dict__}")
    # print(f"type of 'products' in category_census[5] : {type(api.category_census[5].products[0])}")
    # print(f"'products' in category_census[5] : ")
    # for i in api.category_census[5].products:
    #     print(i.name)

    # print()
    api.get_store_census()
    print(f"length of stores set: {len(api.store_census)}")
    # print(f"fifth element of stores set: {api.store_census[5]}")
    # print(f"store_census[5] attributes: {api.store_census[1].__dict__}")
    # print()

    # data_api = create_data_api(api)
    # data_api_clean = clean_data(data_api)

    # data_json = create_data_json()
    # data = clean_data(data_json)
    # download = create_downloader(db, entity, data)

    # TESTS

    # print(f"type of db: {type(db)}")
    # print(f"status code of api: {api.test_status()}")

    # print(f"type of entity: {type(entity)}")
    # print(f"entity class name: {entity.__class__.__name__}")
    # print(f"lower entity class name: {entity.__class__.__name__.lower()}")
    # print(f"attributes of entity: {entity.__dir__()}")
    # print(f"type of entity attributes: ")
    # print(f"type of entity.database: {type(entity.database)}")
    # print(f"type of entity.connection: {type(entity.connection)}")
    # print(f"type of entity.cursor: {type(entity.cursor)}")

    # print(f"type of API: {type(api)}")
    # print(f"api class: {api.__class__}")
    # print(f"api class name: {api.__class__.__name__}")
    # print(f"attributes of api: {api.__dir__()}")
    # print(f"type of api.products: {type(api.products)}")

    # print(f"length of api.products: {len(api.products)}")
    # print(f"type of api.products[0]: {type(api.products[0])}")
    # print(f"api.products[0].name: {api.products[0].name}")
    # for prod in api.products:
    #     print(f"name: {prod.name}")
    #     print(f"categories: {prod.categories}")
    #     print()

    # print(f"api attributes: {api.__dict__.keys()}")
    # print(f"length of api.products: {len(api.products)}")
    # print(f"length of api.categories: {len(api.categories)}")
    # for i in api.categories:
    #     print(f"{i.name}: {i.products}")

    # print(f"api.category[0] attributes: {api.categories[0].__dict__}")

    # print(f"length of api.stores: {len(api.stores)}")
    # for i in api.stores:
    #     if len(i.name) == 0:
    #         print("!! Lost !!")
    #     print(i.name)

    # print(f"product attributes: {api.products[0].__dict__}")

    # print(f"attributes of api.products[0]: {''}")
    # for i in api.products[0].__dict__:
    #     print(f"{i}: {api.products[0].__dict__[i]}")

    # print(api.products[0].__dict__)

    # for i in api.products:
    #     print(f"product name: {i.name}")
    #     print(f"product categories: {i.categories}")
    #     print(f"number of categories: {len(i.categories)}")
    #     print(f"product categories[0]: {i.categories[0].name}")

    # print(f"First Product")
    # print(f"product attributes: {api.products[0].__dict__}")
    # print(f"product name: {api.products[0].name}")
    # for c in api.products[0].categories:
    #     print(f"category: {c.name}")
    # for s in api.products[0].stores:
    #     print(f"store: {s.name}")

    # print(f"type of data_api: {type(data_api)}")
    # print(f"length of data_api: {len(data_api)}")
    # print(f"type of data_api[0]: {type(data_api[0])}")

    # print(f"type of data_json: {type(data_json)}")
    # print(f"length of data_json: {len(data_json)}")
    # print(f"type of data_json[0]: {type(data_json[0])}")
    # print(f"length of data_json[0]: {len(data_json[0])}")

    # print(f"type of data_api_clean: {type(data_api_clean)}")
    # print(f"keys of data_api_clean: {data_api_clean.keys()}")
    # print(f"type of data_api_clean[1]: {type(data_api_clean[1])}")
    # print(f"keys of data_api_clean[1]: {data_api_clean[1].keys()}")
    # for i in data_api_clean:
    #     print(data_api_clean[i]['countries_lc'])

    # print(f"type of data: {type(data)}")
    # print(f"keys of data: {data.keys()}")
    # print(f"type of data[1]: {type(data[1])}")
    # print(f"keys of data[1]: {data[1].keys()}")
    # print(f"list of data[1].keys(): {list(data[1].keys())}")
    # print(f"values of data[1]: {data[1].values()}")
    # print(f"list of data[1].values(): {list(data[1].values())}")

    # for i in data:
    #     print(type(i))
    #     print(i)
    #     print(data[i]['countries_lc'])

    # print(f"type of payload: {type(download.payload)}")
    # print(f"keys of payload: {download.payload.keys()}")
    # print(f"length of payload[1]: {len(download.payload[1])}")
    # print(f"keys of payload[1]: {download.payload[1].keys()}")

    # sample = ['en:breakfasts', 'en:spreads', 'en:sweet-spreads', 'fr:pates-a-tartiner']
    # extraction = [sam[3:] for sam in sample if ('fr' in sam)]
    # print(f"extraction: {extraction}")

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
    #
    # py_product_header = [col[0] for col in prod_columns]
    # print(f"product headers: {py_product_header}")
    # py_product_col = [col for col in prod_columns]
    # print(f"product columns: {py_product_col}")
    # print()
    # py_product = dict(zip(py_product_header, py_product_col))
    # print(f"product table: {py_product}")

    # INSERT PRODUCT IN DB
    # product_data = {
    #         'id': 1,
    #         'name': 'nutella',
    #         'brand': 'ferrero',
    #         'score': 7,
    #         'url': 'url_text',
    #         'description': 'description_text'
    #                 }
    #
    # entity.create_data(queries.PRODUCT_TABLE, queries.PRODUCT_VARIABLES, queries.PRODUCT_VALUES, product_data)
    #
    # print(db.cursor.rowcount, " product inserted !")

    # CHECK PRODUCTS IN TABLE
    # query = "SELECT * FROM product"
    # db.cursor.execute(query)
    # records = db.cursor.fetchall()
    # print("records: ")
    # print(records)

    ######


if __name__ == "__main__":
    main()
