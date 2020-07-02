"""In charge of the manipulation of the content of the database.

This module is a layer which handle the interactions between the database and the entities of the program
It contains the methods CRUD of the program:
 - Create
 - Read
 - Update
 - Delete
"""


from mysql.connector import Error

# import for the development of the code:
from Model.Entity.product import Product
from Model.Manager.api_manager import APIManager


class EntityManager:
    """Handle the interactions with the content of the database.

    The variable database is an instance of the class DBManager.
    """

    def __init__(self, db):

        self.db = db
        self.connection = db.connection
        self.cursor = db.cursor

        # attributes for the development of the code:
        self.api = APIManager()
        self.payload = self.api.get_data()  # return self.products: a list of instances of 'Product'

    def save_all(self):
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
        table_name = self.payload[0].__class__.__name__
        # table_headers = self.payload[0].get_headers()
        table_headers = str(self.payload[0].get_headers()).replace("'", "")
        # string made of placeholders symbols (one for each column in the query)
        headers_count = f"({', '.join(['%s'] * len(self.payload[0].get_headers()))})"

        # skeleton of the query
        query = (
                f"INSERT INTO {table_name} "
                f"{table_headers} "
                f"VALUES {headers_count}"
        )

        # create an empty list ('records') that will contain one element per viable product
        records = []

        # go through the list of instances of 'Product'
        for prod in self.payload:

            # for each instance, create a row
            row = []
            for record in prod.get_values():

                # fetch the values of the instance of product
                # as it tests for its type
                if type(record) is list:
                    # if the value is a list, we assume that it is a list of instances of Store or Catgory,
                    # in that case, we don't include it in the query to insert rows in the table 'product'
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

            # format a row for a product
            row_tuple = tuple(row)

            # add the row to a list of rows used for the statement
            records.append(row_tuple)

        # records = (str(tuple(records))).replace("'", "")

        # print(f"Query: {query}")
        # print()
        # print('Records: ')
        # print(records)

        try:
            self.db.cursor.executemany(query, records)
            self.db.connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")

    # def save_many_data(self, table, cols, rows):
    #     """Insert multiple rows in a table."""
    #     """
    #     parcours la liste:
    #         liste les attributs et pour chacune d'eux:
    #             si l'attribut contient une liste:
    #                 enregistre (pas dans la base) les objets à insérer
    #             sinon:
    #                 enregistrer la valeur (pas dans la base hein)
    #
    #     ici on se retrouve avec une très grande string de multiples insert into
    #     """
    #
    #     def fill_statement(element, statement):
    #         """Recursive function to create the components of the dictionary statement."""
    #
    #         for elem in element:
    #             # initiate the dict that will contain the values for one of the entity instances
    #             # it will be used to insert one of the rows in the db
    #             row = dict()
    #
    #             # split names and values of the attributes of a class, to use them separately
    #             for k, v in elem.__dict__.items():
    #                 # the attribute is not used if it has no values
    #                 if v is None:
    #                     pass
    #                 # launch the next layer to the recursion, if the attribute contains a list
    #                 # it is interpreted as a pathway to develop one of the other statements
    #                 elif type(v) is list:
    #                     fill_statement(v, statement)
    #                 # stop the recursion at this layer
    #                 # add the (key, value) as a new item to the row
    #                 elif isinstance(v, Product):
    #                     row[str(k)] = v.name
    #                 else:
    #                     row[str(k)] = v
    #
    #             # add the row
    #             statement[str(elem.__class__.__name__.lower())].append(row)
    #
    #         return statement
    #
    #     def build_statements():
    #         """Create a compilation of statements, as a dictionary.
    #
    #         Use a recursive function to create the components of the dictionary statement,
    #         from  a list of instances of an entity.
    #         """
    #
    #         stm = {
    #                 'product': [],
    #                 'category': [],
    #                 'store': []
    #         }
    #
    #         # launch the recursive call to the function
    #         fill_statement(self.payload, stm)
    #
    #         return stm
    #
    #     def build_insert(statements):
    #         """Take payload (a list of instances of Product) and use it to create parameters for sql queries"""
    #
    #         for k, v in statements.items():
    #
    #             table_name = str(k)
    #             cols_names = list(v[0].keys())
    #             rows_values = []
    #             for row in v:
    #                 rows_values.append(list(row.values()))
    #             self.save_many_data(table_name, cols_names, rows_values)
    #
    #     def insert_statement(statement):
    #
    #         self.statements = build_statements()
    #         build_insert(self.statements)
    #
    #     val_count = ', '.join(['%s'] * len(cols))
    #     # val_count = ', '.join([f'%({x})s' for x in cols])
    #
    #     query = (
    #             f"INSERT INTO {table} "
    #             f"({cols}) "
    #             f"VALUES ({val_count})"
    #     )
    #
    #     try:
    #         self.cursor.executemany(query, rows)
    #         self.connection.commit()
    #         # print("Query executed successfully")
    #
    #     except Error as e:
    #         print(f"The error '{e}' occurred")

    # def save_data(self, table, cols, rows):
    #     """Insert a new row in a table."""
    #
    #     val_count = ', '.join(['%s'] * len(cols))
    #     # val_count = ', '.join([f'%({x})s' for x in cols])
    #
    #     query = (
    #             f"INSERT INTO {table} "
    #             f"({cols}) "
    #             f"VALUES ({val_count})"
    #     )
    #
    #     try:
    #         self.cursor.execute(query, rows)
    #         self.connection.commit()
    #         # print("Query executed successfully")
    #
    #     except Error as e:
    #         print(f"The error '{e}' occurred")

    # def build_statements(self):
    #     """Create a compilation of statements, as a dictionary.
    # 
    #     Use a recursive function to create the components of the dictionary statement,
    #     from  a list of instances of an entity.
    #     """
    # 
    #     stm = {
    #             'product': [],
    #             'category': [],
    #             'store': []
    #     }
    # 
    #     def fill_statement(element, statement):
    #         """Recursive function to create the components of the dictionary statement."""
    #         for e in element:
    #             # initiate the dict that will contain the values for one of the entity instances
    #             # it will be used to insert one of the rows in the db
    #             row = dict()
    #             # split names and values of the attributes of a class, to use them separately
    #             for k, v in e.__dict__.items():
    #                 # the attribute is not used if it has no values
    #                 if v is None:
    #                     pass
    #                 # launch the next layer to the recursion, if the attribute contains a list
    #                 # it is interpreted as a pathway to develop one of the other statements
    #                 elif type(v) is list:
    #                     fill_statement(v, statement)
    #                 # stop the recursion at this layer
    #                 # add the (key, value) as a new item to the row
    #                 elif isinstance(v, Product):
    #                     row[str(k)] = v.name
    #                 else:
    #                     row[str(k)] = v
    #             # add the row
    #             statement[str(e.__class__.__name__.lower())].append(row)
    # 
    #         return statement
    # 
    #     # launch the recursive call to the function
    #     fill_statement(self.payload, stm)
    # 
    #     return stm

    # def build_insert(self, statements):
    #     """Take payload (a list of instances of Product) and use it to create parameters for sql queries"""
    # 
    #     for k, v in statements.items():
    # 
    #         table_name = str(k)
    #         cols_names = list(v[0].keys())
    #         rows_values = []
    #         for row in v:
    #             rows_values.append(list(row.values()))
    #         self.save_many_data(table_name, cols_names, rows_values)

    # def insert_statement(self):
    # 
    #     self.statements = self.build_statements()
    # 
    #     self.build_insert(self.statements)

    # def many_insert(self):
    #     statement_prod = []
    #     statement_cat = []
    #     statement_cat_prod = dict()
    #     statement_store = []
    #     statement_store_prod = dict()
    #
    #     for prod in products:
    #
    #         statement_prod.append(
    #             {
    #                 'name': prod.name,
    #                 'nutriscore': prod.nutriscore,
    #                 'url': prod.url
    #             }
    #         )
    #
    #         for cat in prod.categories:
    #             statement_cat.append(
    #                 {
    #                     'name': cat.name
    #                 }
    #             )
    #
    #         for shop in prod.stores:
    #             statement_store.append(
    #                 {
    #                     'name': shop.name
    #                 }
    #             )
    #
    #     pass

    # def read_data(self, table, cols, condition=None, order=None, desc=False):
    #     """Retrieve data from one or many columns of a table.
    #
    #     with variable 'condition': retrieve data on some conditions
    #     with variable 'order': retrieve data, sorted by a column
    #     with boolean variable 'desc' added to variable 'order': the data is sorted in descending order
    #     """
    #
    #     query = (
    #             f"SELECT {cols} "
    #             f"FROM {table}"
    #     )
    #
    #     if condition is not None:
    #         where_query = f" WHERE {condition}"
    #         query += where_query
    #
    #     if order is not None:
    #         order_query = f" ORDER BY {order}"
    #         query += order_query
    #
    #     if desc is not None:
    #         query += " DESC"
    #
    #     try:
    #         self.cursor.execute(query)
    #         results = self.cursor.fetchall()
    #         for result in results:
    #             print(result)
    #         # print("Query executed successfully")
    #
    #     except Error as e:
    #         print(f"The error '{e}' occurred")
    #
    # def verify_data(self, table, col_name, value):
    #     """Verify if row already exists in a table.
    #
    #     With condition looking like this: "col_name=value".
    #     The query returns 1 if the condition is validated (the data iq already in the db).
    #     """
    #
    #     result = 0
    #
    #     query = (
    #             f"SELECT EXISTS("
    #             f"SELECT * "
    #             f"FROM {table} "
    #             f"WHERE {col_name}"
    #             f"={value}"
    #             f")"
    #     )
    #
    #     try:
    #         result = self.cursor.execute(query, value)
    #         self.connection.commit()
    #         return result
    #         # print("Query executed successfully")
    #
    #         # self.cursor.execute(query, value)
    #         # results = self.cursor.fetchall()
    #         # for result in results:
    #         #     print(result)
    #         # # print("Query executed successfully")
    #
    #     except Error as e:
    #         print(f"The error '{e}' occurred")
    #
    # def update_data(self, table, cols, new_value, condition):
    #     """Modify data from table on condition."""
    #
    #     query = (
    #             f"UPDATE {table} "
    #             f"SET {cols} = {new_value} "
    #             f"WHERE {condition}"
    #     )
    #
    #     try:
    #         self.cursor.execute(query)
    #         self.connection.commit()
    #         # print("Query executed successfully")
    #
    #     except Error as e:
    #         print(f"The error '{e}' occurred")
    #
    # def delete_data(self, table, condition):
    #     """Delete data from table on condition."""
    #
    #     query = (
    #             f"DELETE FROM {table} "
    #             f"WHERE {condition}"
    #     )
    #
    #     try:
    #         self.cursor.execute(query)
    #         self.connection.commit()
    #         print("Query executed successfully")
    #
    #     except Error as e:
    #         print(f"The error '{e}' occurred")
