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
        """Insert multiple rows in a table."""

        queries = []

        # go through the list of instances of 'Product'
        for instance in payload:

            # create a row, for each instance
            insta_values = []
            # fetch each value of the instance (using an internal method of the instance)
            for attribute in instance.get_values():

                # fetch the values of the instance of product (if the value is not a list)
                if type(attribute) is list:

                    # if the value is a list, we assume that it is a list of instances of 'Store' or 'Category'
                    for element in attribute:

                        # create an instance of the entity
                        instalment = eval(element)

                        if type(instalment) is Category or Store:

                            # format the value of the instance
                            instalment_values = [att for att in instalment.get_values()]
                            if len(instalment_values) == 1:
                                instalment_values = str("'" + str(instalment_values[0]) + "'")

                            # format a row per instance
                            row_values = str("("+instalment_values+")")
                            # set the parameters of the query, for each instance
                            table_name = instalment.__class__.__name__.lower()
                            table_headers = str(instalment.get_headers()).replace("'", "")
                            # skeleton of each query
                            query = (
                                    f"INSERT INTO {table_name} "
                                    f"{table_headers} "
                                    f"VALUES {row_values}"
                            )
                            # filling the list of 'queries'
                            queries.append(query)
                else:
                    # take the value as it is
                    insta_values.append(attribute)

            # format a row per instance of product
            row_values = str(tuple(insta_values))
            # set the parameters of the query, for each instance
            table_name = instance.__class__.__name__.lower()
            table_headers = str(instance.get_headers()).replace("'", "")
            # skeleton of each query
            query = (
                    f"INSERT INTO {table_name} "
                    f"{table_headers} "
                    f"VALUES {row_values}"
            )
            # filling the list of 'queries'
            queries.append(query)

        # try to execute every query in one command to the db
        try:
            statement = str('; '.join(queries))
            # yield each statement in the generator expression (created with parameter 'multi=True')
            for _ in (self.db.cursor.execute(statement, multi=True)):
                print(self.db.cursor.statement)
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
        """
        parcours la liste:
            liste les attributs et pour chacune d'eux:
                si l'attribut contient une liste:
                    enregistre (pas dans la base) les objets à insérer
                sinon:
                    enregistrer la valeur (pas dans la base hein)

        ici on se retrouve avec une très grande string de multiples insert into
        """

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
