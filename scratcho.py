import os


# print()
# print("######")
# print()
#
# # Walking a directory tree and printing the names of the directories and files
# for dirpath, dirnames, files in os.walk('.'):
#     print(f'DIRECTORY: {dirpath}')
#     for file_name in files:
#         print(f"  - FILE: {file_name}")

# example of opening a file
# my_file = open('my_file.txt')

# path = '\Users\Mica\Dropbox\Scripts\OpenClassrooms\OC_Py05\OC_P5-PurBeurre'


# print(os.path.realpath())
# print(os.listdir('OC_P5-PurBeurre'))

# path = os.getcwd()

# print(path)
# print(os.path.basename(path))
# print(os.listdir(path))

# names = os.listdir(path)
# print(names)

# get all regular files
# names = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
# print(names)

# names = []
# for name in os.listdir(path):
#     if os.path.isfile(os.path.join(path, name)):
#         # print(f"name : {name}")
#         names.append(name)
#
# print(f"all names : {names}")

# get all dirs
# dirnames = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

# print(dirnames)


# rootpath = os.getcwd()
# basename = os.path.basename(rootpath)
#
# print(basename)
# print(os.listdir(rootpath))
#
# print(f"reach_file basename : {reach_file(basename, 'Static')}")
# print(f"reach_file rootpath : {reach_file(rootpath, 'Static')}")
#
# print('database_creation.sql' in os.listdir(reach_file(rootpath, 'Static')))

# ROOT = os.path.dirname(os.path.abspath(__file__))
# FILE = "file.txt"
#
# filename = os.path.join(ROOT, FILE)
# print(f"filename : {filename}")


def reach_file(*args):
    """Method to create a path to load a file """

    # create a path object to the root directory
    rootpath = os.getcwd()

    fullpath = os.path.join(rootpath, *args)
    return fullpath


sql_schema = reach_file('Static', 'database_creation.sql')
print(sql_schema)

print(os.path.join(os.getcwd(), 'Static', 'database_creation.sql'))
