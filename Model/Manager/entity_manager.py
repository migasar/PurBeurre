"""In charge of the manipulation of the content of the database.

This module is a layer which handle the interactions between the database and the entities of the program
It contains the methods CRUD of the program:
 - Create
 - Read
 - Update
 - Delete
"""

from mysql.connector import Error

from Model.Entity.product import Product
from Model.Entity.category import Category
from Model.Entity.store import Store

from Model.Manager.db_manager import DBManager


class EntityManager:
    """Handle the interactions with the content of the database.

    The variable database is an instance of the class DBManager.
    """

    def __init__(self, db=DBManager()):
        self.db = db
        self.connection = db.connection
        self.cursor = db.cursor

    def insert_all(self, payload):
        """Insert multiple rows in a table.

        The method 'insert_all' orchestrates the call to the methods
        to create a query to insert a row in the db for each instance in 'payload.'

        The result will be a list of queries which will be coerced in a long string,
        and then send to the db.
        """

        # repository for the formatted queries
        queries = []
        # create a query for each instance of the list
        for instance in payload:
            queries.append(self.create_query(instance))

        # unpack the nested lists
        request = self.unpack_listing(queries)
        # reverse back the order of the stack of queries
        request.reverse()

        # try to execute every query in one command to the db
        try:
            # join together the elements of the list of queries, as one unique long string
            statement = str('; '.join(request))
            # yield each statement in the generator expression (created with parameter 'multi=True')
            for _ in (self.db.cursor.execute(statement, multi=True)):
                continue
        except Error as e:
            print(f"The error '{e}' occurred")

    def create_query(self, instance, parent=None):
        """Create a string used as a query, from a formatted string and the variables used as parameters."""

        # repository for the formatted queries
        children = []

        # set the parameters
        table_name = instance.__class__.__name__.lower()
        row_keys = []
        row_values = []
        
        # unpack the attributes of the instance
        for attribute_key, attribute_value in instance.__dict__.items():
            if attribute_value is None:
                pass
            elif type(attribute_value) is list:
                # launch a recursive call if the attribute is a repository of other instances
                for child in attribute_value:
                    children.append(self.create_query(child, instance))
            else:
                # collect the variables needed to create a row of data
                row_keys.append(attribute_key)
                row_values.append(attribute_value)
    
        # format the parameters
        if (len(row_keys) or len(row_values)) == 1:
            single_row_key = str("'" + str(row_keys[0]) + "'")
            row_keys = str("(" + single_row_key + ")").replace("'", "")
            single_row_value = str("'" + str(row_values[0]) + "'")
            row_values = str("(" + single_row_value + ")")
        else:
            row_keys = str(tuple(row_keys)).replace("'", "")
            row_values = str(tuple(row_values))

        # format the query
        query = (
                f"INSERT INTO {table_name}"
                f" {row_keys}"
                f" VALUES {row_values} "
                f"ON DUPLICATE KEY UPDATE"
                f" {table_name}_id=LAST_INSERT_ID({table_name}_id); "
                f"SET @{table_name}_id = LAST_INSERT_ID()"
        )
        
        # depending of the instance, modify the query to add a request for the tables of associations  
        if parent is not None:
            parent_name = parent.__class__.__name__.lower()
            query_tail = (
                    f"; "
                    f"INSERT IGNORE INTO {table_name}_{parent_name}"
                    f" ({table_name}_id, {parent_name}_id)"
                    f" VALUES (@{table_name}_id, @{parent_name}_id)"
            )
            query += query_tail

        # finally, the formatted query is added to the list of 'queries'
        children.append(query)

        return children

    def unpack_listing(self, payload, components=None):
        """Serialize a nested list (of an unknown depth).
        
        It returns a flattened list with the same elements (they are all brought at the same level). 
        """
        
        if components is None:
            atoms = []
        else:
            atoms = components

        for element in payload:
            # if the function encounters another level, it launch a recursive call to bring its elements forward
            if type(element) is list:
                self.unpack_listing(element, atoms)
            else:
                atoms.append(element)
                
        return atoms

    def insert_one(self, instance):
        """Insert one row in a table."""

        # parameters of the query
        table_name = instance.__class__.__name__.lower()
        table_headers = str(instance.get_headers()).replace("'", "")
        headers_count = f"({', '.join(['%s'] * len(instance.get_headers()))})"

        # skeleton of the query
        query = (
                f"INSERT INTO {table_name} "
                f"{table_headers} "
                f"VALUES {headers_count}"
        )

        # create an empty list ('record') that will contain the elements of one row
        record = []
        # fetch the values of the instance
        for val in instance.get_values():
            # if the value is a list, we assume that it is a list of instances of another entity
            if type(val) is list:
                continue
            # if the value is an int, take the value as it is
            elif type(val) is int:
                record.append(val)
            # otherwise, take the value as a string (if it is neither a list or an int)
            else:
                record.append(str(val))

        # format a row of the instance
        row = str(tuple(record)).replace("'", "")

        # try to execute the query
        try:
            self.db.cursor.execute(query, row)
            self.db.connection.commit()

        except Error as e:
            print(f"The error '{e}' occurred")
