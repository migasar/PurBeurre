###############
#  SCRATCH OS
###############

# import os
#
# with os.scandir(r'Model\') as entries:
#     for entry in entries:
#         print(entry.name)
#
# # Model\Manager


# from pathlib import Path
#
# data_folder = Path("Model/Static")
# file_to_open = data_folder / "constant.py"
#
# f = open(file_to_open)
# print(f.read())

import os
from pathlib import Path

Path.cwd()

p = Path('.')

print([x for x in p.iterdir() if x.is_dir()])

print(list(p.glob('**/*.py')))

p = Path('/etc')
print(f"p : {p}")

q = p / 'init.d' / 'reboot'
print(f"q : {q}")

q.resolve()
print(q.resolve())

q.exists()
print(q.exists())

print(q.is_dir())

# with q.open() as f:
# 	f.readline()


print(f"cwd : {os.getcwd()}")

print(f" Path cwd : {Path.cwd()}")

print(Path('api_manager.py').exists())
print(Path('Model/').exists())

print(sorted(Path('.').glob('**/*.py')))
print(sorted(Path('.').glob('**/*.py')))


# Walking a directory tree and printing the names of the directories and files
for dirpath, dirnames, files in os.walk('.'):
    print(f'Found directory: {dirpath}')
    for file_name in files:
        print(file_name)


###############
#  SCRATCH DB
###############

import mysql.connector as mysql
from mysql.connector import Error

from Static import setting
# import Static.sql_query as query

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


###############
#  SCRATCH SQL
###############

import mysql.connector as mysql
from mysql.connector import Error

connection = mysql.connect(host_name,
                           user_name,
                           user_password,
                           db_name)

cursor = connection.cursor()


def execute_script(filename):
    fd = open(filename, 'r')
    sql_file = fd.read()
    fd.close()
    sql_commands = sql_file.split(';')

    for command in sql_commands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except IOError as msg:
            print(f"Command skipped: {msg}")


execute_script('sql_file')
