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


def main():
    """Launch the program by calling the first modules of its internal process"""

    # FUNCTIONS

    def create_database():
        # CREATE DATABASE AND DB CONNECTION

        db_builder = DBManager()
        db_builder.build_database()
        print("DB created !")

        return db_builder

    def call_api():
        # CREATE API

        api_caller = APIManager()
        api_caller.get_load()
        print("API called !")

        return api_caller

    def create_entity_manager(db_manager):
        # CREATE ENTITY MANAGER

        entity_manager = EntityManager(db_manager)
        print("Entity Manager created !")

        return entity_manager

    def download_data(api_manager, entity_manager):
        # SAVE DATA IN DB

        api_manager.download_data(entity_manager)
        print("Data downloaded !")

        return api_manager

    # ACTIONS
    db = create_database()
    api = call_api()
    entity = create_entity_manager(db)
    download = download_data(api, entity)


if __name__ == "__main__":
    main()
