"""
Handle the storage of the data,
from the creation of the database and its components
to the insertion of the data in the database.

Part of the ORM (object-relational mapping) :
The ORM handles every transaction between the database of the program and the other elements of the program.
Every coding elements with SQL should be regrouped in the ORM.
"""


import mysql.connector as mysql
from mysql.connector import Error

import Static.setting as setting 
import Static.sql_query as query


params_server = {
    'host_name': setting.DB_HOST,
    'user_name': setting.DB_USER,
    'user_password': setting.DB_PASSWORD,
    # 'db_name': setting.DB_NAME
}

params_database = {
    'host_name': setting.DB_HOST, 
    'user_name': setting.DB_USER, 
    'user_password': setting.DB_PASSWORD, 
    'db_name': setting.DB_NAME
    }

create_database_query = "CREATE DATABASE IF NOT EXISTS pur_beurre"
create_db_query = "CREATE DATABASE IF NOT EXISTS " + str(db_name)


class DBConnector:

    __shared_state = {}  # Borg design pattern, shared state

    def __init__(self, **params):
        self.__dict__ = self.__shared_state
        self.connection = self.get_connection(params)

    def get_connection(self, host_name, user_name, user_password, db_name=None):
        """
        Create a connection with MySQL server, 
        if db_name is specified, create a connection specifically to a database
        """

        if db_name is not None:  # get a connection to a specific database
            connection = None
            try:
                connection = mysql.connect(
                    host=host_name,
                    user=user_name,
                    passwd=user_password,
                    database=db_name
                )
                print("Connection to MySQL database successful")
            except Error as e:
                print(f"The error'{e}' occured")
            self.connection = connection
            return self.connection
            
        else:  # get a connection to the server
            connection = None
            try:
                connection = mysql.connect(
                    host=host_name,
                    user=user_name,
                    passwd=user_password
                )
                print("Connection to MySQL server successful")
            except Error as e:
                print(f"The error'{e}' occured")
            self.connection = connection
            return self.connection


        # def get_connection_server(self, host_name, user_name, user_password):
        #     connection = None
        #     try:
        #         connection = mysql.connect(
        #             host=host_name,
        #             user=user_name,
        #             passwd=user_password
        #         )
        #         print("Connection to MySQL server successful")
        #     except Error as e:
        #         print(f"The error'{e}' occured")
        #     self.connection = connection
        #     return self.connection
        
        # def get_connection_db(self, host_name, user_name, user_password, db_name=None):
        #     connection = None
        #     try:
        #         connection = mysql.connect(
        #             host=host_name,
        #             user=user_name,
        #             passwd=user_password,
        #             database=db_name
        #         )
        #         print("Connection to MySQL database successful")
        #     except Error as e:
        #         print(f"The error'{e}' occured")
        #     self.connection = connection
        #     return self.connection

    def get_cursor(self):
        """
        Return the instance of cursor.
        The cursor is the object that interact with the DB server.
        It execute operations such as SQL statements.
        """
        if self.connection is None:
            print("No connection on DB to instantiate the cursor ")
        else:
            self.cursor = self.connection.cursor()
        return self.cursor


class DBHandler:
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = DBConnector()
        self.cursor = connection.get_cursor()


    def execute_query(self, query):
        """Wrapper function to handle SQL queries """
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occured")


    def create_database(self, db_name):
        """Create the database with the function execute_query() """
        try:
            #  db_query = "CREATE DATABASE IF NOT EXISTS " + str(self.db_name)
            db_query = query.CREATE_DB_QUERY + str(self.db_name)
            self.execute_query(db_query)
            print("Database created")
        except Error as e:
            print(f"The error '{e}' occured")

    def create_table(self):
        """Create the tables with the function execute_query() """
        try:
            table_product_query = query.CREATE_TABLE_PRODUCT
            self.execute_query(table_product_query)
            print("Table product created")
        except Error as e:
            print(f"The error '{e}' occured")



######
######


class DBConnection:  # mentored
    """
    Initiate the connection to MySQL server,
    and create an object to interact with it.
    """

    def __init__(self):
        self.connector = None

    @classmethod  # singleton pattern
    def get_instance(cls):
        """
        Return the instance of DBConnector.
        If no instance exists, create one.
        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def get_cursor(self):
        """
        Return the instance of cursor.
        The cursor is the object that interact with the DB server.
        It execute operations such as SQL statements.
        """
        if self.connection is None:
            print("No connection on DB to instantiate the cursor ")
        else:
            self.cursor = self.connection.cursor()
        return self.cursor


class DBManager:
    """
    Initiate the interaction with the database, if it already exists.
    Create the database otherwise.
    """

    def __init__(self):
        self.creator = None

    @classmethod  # singleton pattern
    def get_instance(cls):
        """
        Return  the instance of DBManager.
        If no instance exists, create one.
        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance


class Database:
    """
    Describe the database.
    """

    def __init__(self, name):
        self.name = name

    def get_instance(self):
        """Return an instance of the database. """

    def get_name(self):
        """Return the name of the database. """
        pass

    def get_column_name(self):
        """Return the name of the colimns. """
        pass

    def get_column_type(self):
        """Return the type of the columns. """
        pass


class TableManager:
    """
    Create the tables of the database and handle methods to modify the tables.
    """

    def __init__(self, name):
        self.name = name


class Table:
    """Describe a table. """
    pass


class DataInsertionTable:
    """
    Create data in a table and handle methods to modify them.
    """
    pass
