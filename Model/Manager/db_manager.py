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

import os

import Static.setting as setting  # module with private settings
import Static.sql_query as query


class Borg:
    """
    Metaclass to apply the Borg pattern to a subclass.
    It makes sure that only one instance of a class is created.

    The Borg pattern is an alternative to the Singleton.
    It doesn't really block the creation of over instances,
    but it ensures that all instances share state and behavior.

    The subclass behaves as if only the last created instance is callable,
    which gives the possibility to modify the instance.
    """

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state


class DBConnector(Borg):
    """
    Initiate the connection to MySQL server,
    and create an object to interact with it.
    """

    def __init__(self, host_name, user_name, user_password, db_name=None):
        Borg.__init__(self)

        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name

        self.connection = self.set_connection()

        self.cursor = self.get_cursor()

    def set_connection(self):
        """
        Create a connection with MySQL server,
        if db_name is specified, create a connection specifically to a database
        """

        if self.db_name is None:
            # create a general connection to MySQL server

            connection = None
            try:
                connection = mysql.connect(
                    host=self.host_name,
                    user=self.user_name,
                    passwd=self.user_password
                )
                print("Connection to server successful")

            except Error as e:
                print(f"The error'{e}' occured")
            self.connection = connection

            return self.connection

        else:
            # create a specific connection to a database
            connection = None

            try:
                connection = mysql.connect(
                    host=self.host_name,
                    user=self.user_name,
                    passwd=self.user_password,
                    database=self.db_name
                )
                print("Connection to database successful")

            except Error as e:
                print(f"The error'{e}' occured")
            self.connection = connection

            return self.connection

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

    def __init__(self, host_name, user_name, user_password, db_name):

        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password

        self.db_name = db_name

        self.connection = None
        self.cursor = None

    def get_connection(self, _dbalive=True):

        if _dbalive is True:
            """Create a connection to the server"""

            self.connection = DBConnector(self.host_name, self.user_name, self.user_password)
            self.cursor = self.connection.cursor

            return self.connection, self.cursor

        else:  # _dbalive is False
            """Create a connection to the database"""

            self.connection = DBConnector(self.host_name, self.user_name, self.user_password,
                                          db_name=self.db_name)
            self.cursor = self.connection.cursor

            return self.connection, self.cursor

    def build_database(self, *args):
        """Fetch a SQL file and use it as a schema to build the database"""

        # create a path object to reach the sql file
        filename = os.path.join(os.getcwd(), *args)  # args='database_creation.sql'

        # open, read and close the file
        with open(filename, 'r') as f:
            sql_file = f.read()

        sql_commands = sql_file.split(';')

        # execute the queries from the sql file
        for command in sql_commands:
            try:
                self.cursor.execute(command)

            except IOError as msg:
                print(f"Commands skipped : {msg}")

        self.get_connection(_dbalive=True)

    def execute_query(self, sql):
        """Wrapper function to handle SQL queries """

        try:
            self.cursor.execute(sql)
            # self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occured")

    # def create_database(self):
    #     """Create the database with the function execute_query() """
    #
    #     self.get_connection(_dbalive=True)
    #     try:
    #         db_query = query.CREATE_DB + str(self.db_name)
    #         self.execute_query(db_query)
    #         print("Database created")
    #
    #         return self.get_connection(_dbalive=False)
    #
    #     except Error as e:
    #         print(f"The error '{e}' occured")
    #
    # def create_table(self, sql):
    #     """Create a table with the function execute_query() """
    #
    #     try:
    #         self.execute_query(sql)
    #         print("Table created")
    #     except Error as e:
    #         print(f"The error '{e}' occured")
    #
    # def build_database(self):
    #     """Regroup the methods to build the database 'purbeurre' """
    #
    #     try:
    #         self.create_table(query.CREATE_TABLE_PRODUCT)
    #         print("Table product created")
    #
    #         self.create_table(query.CREATE_TABLE_CATEGORY)
    #         print("Table category created")
    #
    #         self.create_table(query.CREATE_TABLE_PROD_CATEGORY)
    #         print("Table prod_category created")
    #
    #     except Error as e:
    #         print(f"The error '{e}' occured")


# class Database:
#     """
#     Describe the database.
#     """
#
#     def __init__(self, host_name, user_name, user_password, db_name):
#
#         self.db_name = db_name
#
#         self.host_name = host_name
#         self.user_name = user_name
#         self.user_password = user_password
#
#         self.connector = DBConnector(self.host_name, self.user_name, self.user_password)
#         self.cursor = self.connector.cursor
#
#         self.manager = DBManager(self.host_name, self.user_name, self.user_password, db_name=self.db_name)
#         self.db = self.manager.create_database()
#
#     def get_instance(self):
#         """Return an instance of the database. """
#         pass
#
#     def get_name(self):
#         """Return the name of the database. """
#         pass
#
#     def get_column_name(self):
#         """Return the name of the columns. """
#         pass
#
#     def get_column_type(self):
#         """Return the type of the columns. """
#         pass
#
#
# class TableManager:
#     """
#     Create the tables of the database and handle methods to modify the tables.
#     """
#     def __init__(self, name):
#         self.name = name
#
#       pass
#
#
# class Table:
#     """Describe a table. """
#     pass
#
#
# class DataInsertionTable:
#     """
#     Create data in a table and handle methods to modify them.
#     """
#     pass

