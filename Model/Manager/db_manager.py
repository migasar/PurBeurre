"""
Handle the storage of the data,
from the creation of the database and its components
to the insertion of the data in the database.

Part of the ORM (object-relational mapping) :
The ORM handles every transaction between the database of the program and the other elements of the program.
Every coding elements with SQL should be regrouped in the ORM.
"""


import os
import mysql.connector as mysql
from mysql.connector import Error

import Static.setting as setting  # module with private settings


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


class DBConnector(Borg):
    """
    Initiate the connection to MySQL server or a database,
    and create an object to interact with it.
    """

    def __init__(self, host_name, user_name, user_password, db_name=None):

        # ensure that only one instance of DBConnector is at play
        Borg.__init__(self)

        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name

        # initiate the connection
        self.connection = self.set_connection()
        self.cursor = self.set_cursor()

    def set_connection(self):
        """
        Create a connection with MySQL server,
        if db_name is specified, create a connection specifically to a database
        """

        if self.db_name is None :
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

    def set_cursor(self):
        """
        Return an instance of cursor.
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

        # initiate a connection to the server
        self._connector = self.get_connector()
        self.connection = self._connector.connection
        self.cursor = self._connector.cursor

        # initiate the creation of the database
        self.build_database('schema_purbeurre.sql')

    def get_connector(self, db_name=None):
        """
        Connect with a database if db_name is specified, otherwise connect with the server
        It returns the cursor to the connection as well
        """

        self._connector = DBConnector(self.host_name, self.user_name, self.user_password, db_name)

        return self._connector

    def build_database(self, *args):
        """Fetch a SQL file and use it as a schema to build the database"""

        # create a path object to reach the sql file
        filename = os.path.join(os.getcwd(), *args)  # args='schema_purbeurre.sql'

        # open the sql file with as an object to pass its content to other methods
        with open(filename, 'r') as f:
            sql_file = f.read()
            # methods to format the content of the sql file
            # delete all the end lines in the file
            sql_file = sql_file.replace("\n", "")
            # explicitly split every query inside the file
            sql_file = sql_file.split(';')

        # execute, one by one,every query from the schema
        for line in sql_file:
            self.cursor.execute(line)

        # renew _connector to initiate a connection with the database
        self._connector = self.get_connector(self.db_name)
        self.connection = self._connector.connection
        self.cursor = self._connector.cursor

        return self.connection, self.cursor


def main():

    # INSTANCIATE A CONNECTION TO SERVER
    # connection = DBConnector(setting.DB_HOST, setting.DB_USER, setting.DB_PASSWORD)
    # cursor = connection.cursor

    # CHECK DATABASES
    # cursor.execute("DROP DATABASE purbeurre")
    # cursor.execute("SHOW DATABASES")
    # databases = cursor.fetchall()
    # for database in databases:
    #     print(database)

    # CREATE DATABASE
    db_test = DBManager(setting.DB_HOST, setting.DB_USER, setting.DB_PASSWORD, db_name='purbeurre')

    # CHECK TABLES
    db_test.cursor.execute("SHOW TABLES")
    tables = db_test.cursor.fetchall()
    for table in tables:
        print(table)


if __name__ == "__main__":
    main()
