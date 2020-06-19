"""
Handle the storage of the data

From the creation of the database and its components
to the insertion of the data in the database.

Part of the ORM (object-relational mapping) :
The ORM handles every transaction between the database of the program and the other elements of the program.
Every coding elements with SQL should be regrouped in the ORM.
"""


import mysql.connector as mysql
from mysql.connector import Error

import Static.constant as constant


class Borg:
    """
    Metaclass to apply the Borg pattern to a subclass.

    It makes sure that there is only one instance of a class that is in use.
    The Borg pattern is an alternative to the Singleton.
    It doesn't really block the creation of over instances,
    but it ensures that all instances share state and behavior.

    The subclass behaves as if only the last created instance is callable,
    which gives the possibility to modify the instance.
    """

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state


class DBConnection(Borg):
    """ Initiate the connection to MySQL server or a database """

    def __init__(self, host_name, user_name, user_password, db_name=None):

        # ensure that only one instance of DBConnection is at play
        Borg.__init__(self)

        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name

        # initiate the connection
        self.connection = self.create_connection()

    def create_connection(self):
        """
        Create a connection with MySQL server,
        if db_name is specified, create a connection specifically to a database
        """

        if self.db_name is None:
            # create a general connection to MySQL server

            try:
                self.connection = mysql.connect(
                        host=self.host_name,
                        user=self.user_name,
                        passwd=self.user_password
                )
            except Error as e:
                print(f"The error'{e}' occured")

            return self.connection

        else:
            # create a connection specifically to a database

            try:
                self.connection = mysql.connect(
                        host=self.host_name,
                        user=self.user_name,
                        passwd=self.user_password,
                        database=self.db_name
                )
            except Error as e:
                print(f"The error'{e}' occured")

            return self.connection


class DBManager:
    """Create the database or initiate its connection, if it already exists."""

    def __init__(self, host_name, user_name, user_password, db_name):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name

        # initiate a connection to the server
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor()

    def get_connection(self, db_name=None):
        """
        Retrieve a connection.

        Connect with a database if db_name is specified, otherwise connect with the server
        """

        _cnx = DBConnection(self.host_name, self.user_name, self.user_password, db_name)

        return _cnx.connection

    def build_database(self, filepath=constant.SCHEMA_PATH):
        """
        Initiate the creation of the database.

        Take the path to a sql file as variable, and use the file as a schema to build the database
        """

        # open the sql file as an object to pass its content to other methods
        with open(filepath, 'r') as f:
            sql_file = f.read()
            # methods to format the content of the sql file
            # delete all the end lines in the file
            sql_file = sql_file.replace("\n", "")
            # explicitly split every query inside the file
            sql_file = sql_file.split(';')

        # execute, one by one,every query from the schema
        for line in sql_file:
            self.cursor.execute(line)

        # renew get_connection() to initiate a connection with the database
        self.connection = self.get_connection(self.db_name)
        self.cursor = self.connection.cursor()
        return self.connection, self.cursor
