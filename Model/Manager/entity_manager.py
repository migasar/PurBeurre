"""In charge of the manipulation of the content of the database.

This module is a layer which handle the interactions between the database and the entities of the program
It contains the methods CRUD of the program:
 - Create
 - Read
 - Update
 - Delete
"""

from mysql.connector import Error

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

        The method 'insert_all' orchestrates a cascading call to its internal methods, 
        to create a query to insert a row in the db for each instance in 'payload.'
        
        The process to create each query will be as follow:
         - Per each instance of 'Product', 
           we go through a process that will create a query for each entity found in this instance
         - 1. a query for the instance of 'Product' per se
         - 2. a query for each instances of 'Category' related to this product
         - 3. a query for each instances of 'Store' related to this product
        This process is initiated by calling the method 'parameterize_product()',
        this method will drive a chain of calls to the other methods as needed.
        
        The result will be a list of queries which will be coerced in a long string,
        and then send to the db.
        """

        # create an empty list where will be stacked the formatted queries (their order of creation matters)
        queries = []

        def parameterize_product(element):
            """Create the parameters for a query, from the attributes of an instance of 'Product'."""

            # create a row, for each instance
            element_values = []
            # fetch each value of the instance (using an internal method of the instance)
            for value in element.get_values():

                # fetch the values of the instance of 'Product' (if the value is not a list)
                if type(value) is list:
                    # if the value is a list, we assume that it is a list of instances of 'Store' or 'Category'
                    parameterize_entities(value)
                else:
                    # take the value as it is
                    element_values.append(value)

            build_query(element, element_values)

        def parameterize_entities(attribute):
            """Create the parameters for a query, from the attributes of an instance of 'Category' or 'Store'."""

            # if the value is a list, we assume that it is a list of instances of 'Store' or 'Category'
            for element in attribute:

                # test if it is indeed an instance of 'Store' or 'Category'
                if type(element) is Category or Store:
                    # format the value of the instance
                    element_values = [att for att in element.get_values()]

                    build_query(element, element_values)

        def build_query(parameter, parameter_values):
            """Create a string used as a query, from a formatted string and the variables used as parameters."""

            # format a row per instance of product
            if len(parameter_values) == 1:
                # if the parameter is from an instance of 'Category' or 'Store',
                # it should have a length of 1, and it wouldn't work well to coerce it in a tuple
                instance_single_value = str("'" + str(parameter_values[0]) + "'")
                row_values = str("(" + instance_single_value + ")")
                
            else:
                # if the parameter is from an instance of 'Product',
                # it should have a length of more than 1, and it would be easy to format it by coercing it in a tuple
                row_values = str(tuple(parameter_values))

            # set the parameters of the query, for each instance
            table_name = parameter.__class__.__name__.lower()
            table_headers = str(parameter.get_headers()).replace("'", "")

            # skeleton of each query
            query = (
                    f"INSERT INTO {table_name} "
                    f"{table_headers} "
                    f"VALUES {row_values}"
            )

            # finally, the formatted query is added to the list of 'queries'
            queries.append(query)

        # go through the list of instances of 'Product'
        for instance in payload:
            # for each instance of 'Product', start the chained call to the internal methods 
            # to create a query for each entity contained in the instance of 'Product' 
            parameterize_product(instance)

        # try to execute every query in one command to the db
        try:
            # join together the elements of the list of queries, as one unique long string
            statement = str('; '.join(queries))

            # yield each statement in the generator expression (created with parameter 'multi=True')
            for _ in (self.db.cursor.execute(statement, multi=True)):
                continue
            self.db.connection.commit()

        except Error as e:
            print(f"The error '{e}' occurred")

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
