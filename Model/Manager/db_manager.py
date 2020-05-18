"""
Handle the storage of the data,
from the creation of the database and its components
to the insertion of the data in the database.

Part of the ORM (object-relational mapping) :
The ORM handles every transaction between the database of the program and the other elements of the program.
Every coding elements with SQL should be regrouped in the ORM.
"""


class DBConnector:  # mentored
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
        pass


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
