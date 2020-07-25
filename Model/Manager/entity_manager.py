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

    # Class variable:
    register = {
            'product': Product,
            'category': Category,
            'store': Store
    }

    def __init__(self, db=DBManager()):
        self.db = db
        self.connection = db.connection
        self.cursor = db.cursor

    def unpack_listing(self, listing, components=None):
        """Serialize a nested list (of an unknown depth).

        It returns a flattened list with the same elements (they are all brought at the same level).
        """

        atoms = [] if components is None else components

        for element in listing:
            # if the function encounters another level, it launch a recursive call to bring its elements forward
            if type(element) is list:
                self.unpack_listing(element, atoms)
            else:
                atoms.append(element)

        return atoms

    def create_query(self, entity, parent=None):
        """Create a string used as a query, from a formatted string and the variables used as parameters."""

        # repository for the formatted queries
        children = []

        # set the parameters
        table_name = entity.__class__.__name__.lower()
        row_keys = []
        row_values = []

        # unpack the attributes of the entity
        for item in entity.get_items():
            attribute_key = item[0]
            attribute_value = item[1]
            if attribute_value is None:
                pass
            elif type(attribute_value) is list:
                # launch a recursive call if the attribute is a repository of other instances
                for child in attribute_value:
                    children.append(self.create_query(child, entity))
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
                f"INSERT INTO {table_name} "
                f"  {row_keys} "
                f"  VALUES {row_values} "
                f"ON DUPLICATE KEY UPDATE "
                f"  id_{table_name} = LAST_INSERT_ID(id_{table_name}); "
                f"SET @id_{table_name} = LAST_INSERT_ID() "
        )

        # depending of the instance, modify the query to add a request for the tables of associations
        if parent is not None:
            parent_name = parent.__class__.__name__.lower()
            query_tail = (
                    f"; "
                    f"INSERT IGNORE INTO {table_name}_{parent_name} "
                    f"  (id_{table_name}, id_{parent_name}) "
                    f"  VALUES (@id_{table_name}, @id_{parent_name}) "
            )
            query += query_tail

        # finally, the formatted query is added to the list of 'queries'
        children.append(query)

        return children

    def create_instance(self, entity, **attributes):

        if entity == 'product':

            for key, value in attributes.items():

                if key == 'categories':
                    if type(value) is str:
                        categories = []
                        for cat in value.split(','):
                            try:
                                category = Category(
                                        name=str(cat).strip()
                                )
                                if category.name == "":
                                    raise KeyError
                            except KeyError:
                                continue
                            else:
                                categories.append(category)
                        attributes[key] = categories

                elif key == 'stores':
                    if type(value) is str:
                        stores = []
                        for shop in value.split(','):
                            try:
                                store = Store(
                                        name=str(shop).strip()
                                )
                                if store.name == "":
                                    raise KeyError
                            except KeyError:
                                continue
                            else:
                                stores.append(store)
                        attributes[key] = stores

            return Product(**attributes)

        else:
            return self.register[entity](**attributes)

    def insert_all(self, payload):
        """Insert rows in a table.

        The method 'insert_all' orchestrates the call to the methods
        to create a query to insert a row in the db for each instance in 'payload.'

        The result will be a list of queries which will be coerced in a long string,
        and then send to the db.
        """

        # repository for the formatted queries
        queries = []

        # create queries from the objects in payload
        if type(payload) is list:
            # create a query for each instance of the list
            for instance in payload:
                queries.append(self.create_query(instance))
        else:
            # in case payload is a single instance
            queries.append(self.create_query(payload))

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

    def read_row(self, table_anchor, selection='*', distinct=True, **claims):

        # Query
        claim = []

        # SELECT
        claim_select = f"SELECT DISTINCT " if distinct is True else f"SELECT "

        headers = [str(head) for head in selection]
        columns = [f"{table_anchor}.{col}" for col in headers]
        selection = ', '.join([c for c in columns])
        print(f"target: {selection}")

        claim_select += f"{selection}  "
        claim.append(claim_select)
        print(f"claim_select: {claim_select}")

        # FROM
        claim_from = f"FROM {table_anchor} "
        claim.append(claim_from)

        # JOIN
        if 'join' in claims:
            claim_join = (
                    f"INNER JOIN {claims['join']['table_adjunct']} "
                    f"ON {claims['join']['table_adjunct']}.{claims['join']['row_key']} "
                    f"= {table_anchor}.{claims['join']['row_key']} "
            )
            claim.append(claim_join)
        # WHERE
        if 'where' in claims:
            claim_where = (
                    f"WHERE {claims['where']['table_adjunct']}.{claims['where']['row_key']} "
                    f"= {claims['where']['row_value']} "
            )
            claim.append(claim_where)
        # ORDER
        if 'order' in claims:
            claim_order = f"ORDER BY {claims['order']} "
            claim.append(claim_order)

        # Punctuation
        claim_tail = ";"
        claim.append(claim_tail)

        # Format the query
        statement = str(' '.join(claim))

        # execute the query
        try:
            self.db.cursor.execute(statement)
            records = self.db.cursor.fetchall()

            for record in records:
                values = list(record)
                attrs = dict(zip(headers, values))

                return self.create_instance(table_anchor, **attrs)

        except Error as e:
            print(f"The error '{e}' occurred")
