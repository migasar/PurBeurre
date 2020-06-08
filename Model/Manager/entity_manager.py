"""
In charge of the manipulation of the content of the database

This module is a layer which handle the interactions between the database and the entities of the program
It contains the methods CRUD of the program :
 - Create
 - Read
 - Update
 - Delete
"""


class EntityManager:
    """
    Handle the interactions with the content of the database
    """
    
    def __init__(self):
        pass

    def create_in_db(self):
        pass

    def read_in_db(self):
        pass

    def update_in_db(self):
        pass

    def delete_in_db(self):
        pass


class CategoryManager:

    def save(self, instance):
        data = vars(instance)
        db.query(
            """
            INSERT INTO category (id, name)
            VALUES (null, %(category)s)
            ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
            """,
            **data
        )
        instance.id = db.get_last_insert_id()


class Category:

    def __init__(self, name, id=None, **kwargs):
        self.id = id
        self.name = name


def main():
    category_manager = CategoryManager()
    python = Category(name="python")
    category_manager.save(python)


if __name__ == "__main__":
    main()

