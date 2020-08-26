import os
import shutil


def create_folder(dest_dir, name):
    """
    Creates a new folder in destination directory and modifies the name if it already exists.

    Parameters:
        dest_dir (string): Directory where the new folder will be created.
        name (string): Name of the new folder.

    Returns:
        new_folder_dir (string): Directory where new folder is created.
    """
    new_folder_name = name
    new_folder_path = os.path.join(dest_dir, new_folder_name)

    identifier = 0
    while os.path.exists(new_folder_path):  # Creates new folder
        identifier += 1
        new_folder_name = name + " " + "(" + str(identifier) + ")"
        new_folder_path = os.path.join(dest_dir, new_folder_name)

    os.mkdir(new_folder_path)
    return new_folder_path


def copy_and_rename_file(file_path, dest_dir, new_name):
    """
    Copies a file and renames it.

    Parameters:
        file_dir (string): Path of file to be copied and renamed.
        dest_dir (string): Directory where the file will be copied to.
        new_name (string): Name of the new copied file.

    Returns:
        new_file_path (string): Path of new file.
    """
    new_file_path = os.path.join(dest_dir, new_name)
    shutil.copy(file_path, new_file_path)
    return new_file_path
