from os import walk
import os

dir_path = r'C:\\Users\\PC\\Desktop\\Coding\\django_auth\\auth_site'

folder_paths = []
files_for_delete = []

def filter_folders(path_to_search):
    for entry_name in os.listdir(path_to_search):
        entry_path = os.path.join(path_to_search, entry_name)
        if os.path.isdir(entry_path):
            if entry_path.endswith('\\media') is not True and entry_path.endswith('\\auth_site') is not True:
                folder_paths.append(entry_path)
    return folder_paths

def find_files(folder_paths, db_file_name, main_path):
    sub_folder_paths = []

    for folder in folder_paths:
        for entry_name in os.listdir(folder):
            entry_path = os.path.join(folder, entry_name)
            if os.path.isdir(entry_path):
                if entry_path.endswith('\\migrations') is True:
                    sub_folder_paths.append(entry_path)

    files_in_directory = []

    for folder in sub_folder_paths:
        for entry_name in os.listdir(folder):
            entry_path = os.path.join(folder, entry_name)
            if os.path.isfile(entry_path):
                if entry_path.endswith('__init__.py') is False:
                    files_in_directory.append(entry_path)

    for root, dirs, files in os.walk(main_path):
            if db_file_name in files:
                files_in_directory.append(os.path.join(root, db_file_name))

    return files_in_directory

def delete_files(delete_files):
    for file in delete_files:
        os.remove(file)
    print('Was deleted ' + str(len(delete_files) - 1) + ' migrations and db file')

def find_and_delete_migrations(dir_path):
    folder_paths = filter_folders(dir_path)
    files_for_delete = find_files(folder_paths, 'db.sqlite3', dir_path)
    if len(files_for_delete) != 0:
        delete_files(files_for_delete)
    else:
        print('No migration files to delete')

find_and_delete_migrations(dir_path)