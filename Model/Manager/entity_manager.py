"""
In charge of the manipulation of the content of the database

This module is a layer which handle the interactions between the database and the entities of the program
It contains the methods CRUD of the program :
 - Create
 - Read
 - Update
 - Delete
"""


from mysql.connector import Error


class EntityManager:
    """
    Handle the interactions with the content of the database

    The variable database is an instance of the class DBManager
    """

    def __init__(self, database):

        self.database = database
        self.connection = database.connection
        self.cursor = database.cursor

    def save_data(self, table_name, col_names, val_count, values):
        """Insert a new row in a table. """

        query = (
                f"INSERT INTO {table_name} "
                f"{col_names} "
                f"VALUES {val_count}"
        )

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            # print("Query executed successfully")

        except Error as e:
            print(f"The error '{e}' occurred")

    def save_many_data(self, table_name, col_names, val_count, values):
        """Insert multiple rows in a table. """
        """
        parcours la liste:
            liste les attributs et pour chacune d'eux:
                si l'attribut contient une liste:
                    enregistre (pas dans la base) les objets à insérer                
                sinon:
                    enregistrer la valeur (pas dans la base hein)
        
        ici on se retrouve avec une très grande string de multiples insert into
        
        
        
        """

        query = (
                f"INSERT INTO {table_name} "
                f"{col_names} "
                f"VALUES {val_count}"
        )

        try:
            self.cursor.executemany(query, values)
            self.connection.commit()
            # print("Query executed successfully")

        except Error as e:
            print(f"The error '{e}' occurred")

    def read_data(self, table_name, col_names, condition=None, order=None, desc=False):
        """
        Retrieve data from one or many columns of a table.

        with variable 'condition' : retrieve data on some conditions
        with variable 'order' : retrieve data, sorted by a column
        with boolean variable 'desc' added to variable 'order' : the data is sorted in descending order
        """

        query = (
                f"SELECT {col_names} "
                f"FROM {table_name}"
        )

        if condition is not None:
            where_query = f" WHERE {condition}"
            query += where_query

        if order is not None:
            order_query = f" ORDER BY {order}"
            query += order_query

        if desc is not None:
            query += " DESC"

        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            for result in results:
                print(result)
            # print("Query executed successfully")

        except Error as e:
            print(f"The error '{e}' occurred")

    def verify_data(self, table_name, col_name, value):
        """
        Verify if row already exists in a table.

        with condition looking like this "col_name=value"
        the query returns 1 if the condition is validated (the data iq already in the db)
        """

        result = 0

        query = (
                f"SELECT EXISTS("
                f"SELECT * "
                f"FROM {table_name} "
                f"WHERE {col_name}"
                f"={value}"
                f")"
        )

        try:
            result = self.cursor.execute(query, value)
            self.connection.commit()
            return result
            # print("Query executed successfully")

            # self.cursor.execute(query, value)
            # results = self.cursor.fetchall()
            # for result in results:
            #     print(result)
            # # print("Query executed successfully")

        except Error as e:
            print(f"The error '{e}' occurred")

    def update_data(self, table_name, col_names, new_value, condition):
        """modify data from table on condition"""

        query = (
                f"UPDATE {table_name} "
                f"SET {col_names} = {new_value} "
                f"WHERE {condition}"
        )

        try:
            self.cursor.execute(query)
            self.connection.commit()
            # print("Query executed successfully")

        except Error as e:
            print(f"The error '{e}' occurred")

    def delete_data(self, table_name, condition):
        """delete data from table on condition"""

        query = (
                f"DELETE FROM {table_name} "
                f"WHERE {condition}"
        )

        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")

        except Error as e:
            print(f"The error '{e}' occurred")

