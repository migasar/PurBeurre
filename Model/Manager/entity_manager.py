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
        """Insert multiple rows in a table."""

        queries = []

        def parameterize_instance(component):

            # create a row, for each instance
            component_values = []

            # fetch each value of the instance (using an internal method of the instance)
            for value in component.get_values():
                # fetch the values of the instance of product (if the value is not a list)
                if type(value) is list:
                    # if the value is a list, we assume that it is a list of instances of 'Store' or 'Category'
                    parameterize_entity(value)
                else:
                    # take the value as it is
                    component_values.append(value)

            format_query(component, component_values)

        def parameterize_entity(aspect):

            # if the value is a list, we assume that it is a list of instances of 'Store' or 'Category'
            for component in aspect:

                if type(component) is Category or Store:
                    # format the value of the instance
                    compoment_values = [att for att in component.get_values()]

                    format_query(component, compoment_values)

        def format_query(parameter, parameter_values):

            # format a row per instance of product
            if len(parameter_values) == 1:
                instance_single_value = str("'" + str(parameter_values[0]) + "'")
                row_values = str("(" + instance_single_value + ")")
            else:
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
            # filling the list of 'queries'
            queries.append(query)

        # go through the list of instances of 'Product'
        for instance in payload:
            parameterize_instance(instance)

        # queries = []
        #
        # def format_query(load=payload):
        #
        #     for instance in load:
        #
        #         # print(f"instance: {instance}")
        #         # for i in instance.get_values():
        #         #     print(f"element: {i}, {type(i)}")
        #         #     if type(i) is list:
        #         #         for j in i:
        #         #             print(f"atoms: {j}, {type(j)}")
        #
        #         instance_values = []
        #
        #         for element in instance.get_values():
        #
        #             if type(element) is list:
        #                 # Recursion on the list of entities
        #                 format_query(element)
        #
        #             else:
        #                 if type(element) is Category or Store:
        #
        #                     # print(f"instalment: {element}")
        #                     # print(f"instalment type: {type(element)}")
        #
        #                     instalment = eval(element)
        #                     instalment_values = [att for att in instalment.get_values()]
        #
        #                 else:
        #                     instance_values.append(element)
        #
        #                 # Parameters
        #                 if len(instalment_values) == 1:
        #                     instalment_values = str("'" + str(instalment_values[0]) + "'")
        #                     row_values = str("(" + instalment_values + ")")
        #                 else:
        #                     row_values = str(tuple(instalment_values))
        #
        #                 table_name = instalment.__class__.__name__.lower()
        #                 table_headers = str(instalment.get_headers()).replace("'", "")
        #
        #                 # Query
        #                 query = (
        #                         f"INSERT INTO {table_name} "
        #                         f"{table_headers} "
        #                         f"VALUES {row_values}"
        #                 )
        #                 queries.append(query)
        #
        # format_query(payload)

        # queries = []
        # def format_query(instance, queries=queries):
        #     print(f"instance type: {type(instance)}")
        #     print(f"instance: {instance}")
        #     if type(instance) is not list:
        #         instance_values = instance.get_values()
        #     else:
        #         instance_values = instance
        #     print(f"instance_values type: {type(instance_values)}")
        #     print(f"instance_values: {instance_values}")
        #     # for attribute in instance.get_values():
        #     #     pass
        #     # format the value of the instance
        #     if len(instance_values) == 1:
        #         instance_value = str("'" + str(instance_values[0]) + "'")
        #         # format a row per instance
        #         row_values = str("(" + instance_value + ")")
        #     else:
        #         instance_values = []
        #         for attribute in instance_values:
        #             if type(attribute) is not list:
        #                 instance_values.append(attribute)
        #             elif type(attribute) is list:
        #                 format_query(attribute, queries)
        #         # format a row per instance
        #         row_values = str(tuple(instance_values))
        #     # set the parameters of the query, for each instance
        #     table_name = instance.__class__.__name__.lower()
        #     table_headers = str(instance.get_headers()).replace("'", "")
        #     # skeleton of each query
        #     query = (
        #             f"INSERT INTO {table_name} "
        #             f"{table_headers} "
        #             f"VALUES {row_values}"
        #     )
        #     # filling the list of 'queries'
        #     queries.append(query)
        # for instalment in payload:
        #     format_query(instalment)

        # queries = []
        #
        # def format_row_parameter(load):
        #
        #     if isinstance(load, (Product, Category, Store)):
        #         for element in load.get_values():
        #             format_row_parameter(element)
        #
        #     else:
        #         instance_values = []
        #
        #         for element in load:
        #
        #             if isinstance(element, list):
        #                 for component in element:
        #                     instalment = eval(component)
        #                     format_row_parameter(instalment)
        #
        #             else:
        #                 instance_values.append(element)
        #
        #         format_query(load, instance_values)

        # for instance in payload:
        #     format_row_parameter(instance)

        # try to execute every query in one command to the db
        try:
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
        for val in instance.get_values():

            # fetch the values of the instance
            if type(val) is list:
                # if the value is a list, we assume that it is a list of instances of another entity
                continue
            elif type(val) is int:
                # take the value as it is
                record.append(val)
            else:
                # ensure that the value is a string (if it is neither a list or an int)
                record.append(str(val))

        # format a row of the instance
        row = str(tuple(record)).replace("'", "")

        # try to execute the query
        try:
            self.db.cursor.execute(query, row)
            self.db.connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")

    def save_all(self, payload):
        """Insert multiple rows in a table."""

        # parameters of the query
        table_name = payload[0].__class__.__name__.lower()
        table_headers = str(payload[0].get_headers()).replace("'", "")
        headers_count = f"({', '.join(['%s'] * len(payload[0].get_headers()))})"
        # skeleton of the query
        query = (
                f"INSERT INTO {table_name} "
                f"{table_headers} "
                f"VALUES {headers_count}"
        )

        # create an empty list ('records') that will contain one element per viable product
        records = []
        # go through the list of instances of 'Product'
        for prod in payload:
            # for each instance, create a row
            row = []
            for record in prod.get_values():
                # fetch the values of the instance of product (if the value is not a list)
                if type(record) is list:
                    # if the value is a list, we assume that it is a list of instances of 'Store' or 'Category'
                    continue
                    # variation:
                    # in that case, we transform it in a list with only the name of the instances
                    # row.append(
                    #         # f"({', '.join([str(rec) for rec in record])})"
                    #         # [rec for rec in record]
                    #         tuple([f"({str(rec)})" if len(rec) == 0 else rec for rec in record])
                    # )
                else:
                    # take the value as it is
                    row.append(record)
            # format a row for an instance of product
            row_tuple = tuple(row)
            # add the row to a list of rows used for the statement
            records.append(row_tuple)

        # try to execute the query
        try:
            self.db.cursor.executemany(query, records)
            self.db.connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")
