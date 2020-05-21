import mysql.connector as mysql
from mysql.connector import Error

import Static.setting as setting
import Static.sql_query as query

import Model.Manager.db_manager as manager


connect1 = manager.DBConnector(setting.DB_HOST, setting.DB_USER, setting.DB_PASSWORD)
print(connect1)

cursor = connect1.cursor
print("cursor created")

# cursor.execute("DROP DATABASE db_test")
cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()
for database in databases:
    print(database)

# print("......")
# print("creating new database")
#
# db_manager_test = DBManager(setting.DB_HOST, setting.DB_USER, setting.DB_PASSWORD, db_name='db_test')
# db_test = db_manager_test.create_database()
#
# print("......")
# print(connect1)
#
#
# print("......")
# print("creating connection 2")
#
# connect2 = DBConnector(setting.DB_HOST, setting.DB_USER, setting.DB_PASSWORD)
# print(connect2)
# cursor = connect2.cursor
#
# cursor.execute("SHOW DATABASES")
# databases = cursor.fetchall()
#
# for database in databases:
#     print(database)
