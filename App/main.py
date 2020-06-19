"""
In charge of the launch of the program

Call all the elements of the program in an orchestrated manner
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


def main():
    """Launch the program by calling the first modules of its internal process"""

    ######
    # FUNCTIONS

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

    def create_api():
        # CREATE API
        api_off = API(constant.OFF_URL, constant.API_PARAMETERS)
        api_caller = APICaller(api_off)
        api_caller.get_responses()
        print("api created !")

        return api_caller

    def create_data_api(api_call):
        # CREATE A DATA STRUCTURE WITH AN API REQUEST
        api_request = api_call.responses
        print("Creating data container from an api request.")

        return api_request

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

    def create_downloader(db_manager, entity_manager, data_payload):
        # CREATE DATA DOWNLOADER
        data_downloader = DataDownloader(db_manager, entity_manager, data_payload)
        print("data downloader created !")

        return data_downloader

    ######
    # ACTIONS

    db = create_database()
    entity = create_entity(db)
    api = create_api()

    # data_api = create_data_api(api)
    # data_api_clean = clean_data(data_api)

    data_json = create_data_json()
    data = clean_data(data_json)

    download = create_downloader(db, entity, data)

    ######
    # TESTS

    print()

    # print(f"type of db : {type(db)}")
    # print(f"status code of api : {api.test_status()}")

    print(f"type of entity : {type(entity)}")
    print(f"entity class name : {entity.__class__.__name__}")
    print(f"lower entity class name : {entity.__class__.__name__.lower()}")
    # print(f"attributes of entity : {entity.__dir__()}")
    # print(f"type of entity attributes : ")
    # print(f"type of entity.database : {type(entity.database)}")
    # print(f"type of entity.connection : {type(entity.connection)}")
    # print(f"type of entity.cursor : {type(entity.cursor)}")

    # print(f"type of data_api : {type(data_api)}")
    # print(f"length of data_api : {len(data_api)}")
    # print(f"type of data_api[0] : {type(data_api[0])}")

    # print(f"type of data_json : {type(data_json)}")
    # print(f"length of data_json : {len(data_json)}")
    # print(f"type of data_json[0] : {type(data_json[0])}")
    # print(f"length of data_json[0] : {len(data_json[0])}")

    # print(f"type of data_api_clean : {type(data_api_clean)}")
    # print(f"keys of data_api_clean : {data_api_clean.keys()}")
    # print(f"type of data_api_clean[1] : {type(data_api_clean[1])}")
    # print(f"keys of data_api_clean[1] : {data_api_clean[1].keys()}")
    # for i in data_api_clean:
    #     print(data_api_clean[i]['countries_lc'])

    print(f"type of data : {type(data)}")
    print(f"keys of data : {data.keys()}")
    print(f"type of data[1] : {type(data[1])}")
    print(f"keys of data[1] : {data[1].keys()}")
    print(f"list of data[1].keys() : {list(data[1].keys())}")
    # print(f"values of data[1] : {data[1].values()}")
    print(f"list of data[1].values() : {list(data[1].values())}")

    # for i in data:
    #     print(type(i))
    #     print(i)
    #     print(data[i]['countries_lc'])

    print(f"type of payload : {type(download.payload)}")
    print(f"keys of payload : {download.payload.keys()}")
    print(f"length of payload[1] : {len(download.payload[1])}")
    print(f"keys of payload[1] : {download.payload[1].keys()}")

    print()

    # CHECK TABLES
    # db.cursor.execute("SHOW TABLES")
    # tables = db.cursor.fetchall()
    # for table in tables:
    #     print(table)

    # CHECK COLUMNS IN TABLES
    # db.cursor.execute("DESC product")
    # table = db.cursor.fetchall()
    # print(table)
    # for col in table:
    #     print(col)

    # INSERT PRODUCT IN DB
    # product_data = {
    #         'id': 1,
    #         'name': 'nutella',
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
    # print("records : ")
    # print(records)

    ######
    ######


if __name__ == "__main__":
    main()
