import os
import shutil

from promptflow.core import tool


@tool
def delete(file_or_folder_name: str):
    if os.path.exists(file_or_folder_name):
        if os.path.isfile(file_or_folder_name):
            os.remove(file_or_folder_name)
            print(f"{file_or_folder_name} deleted successfully.")
        elif os.path.isdir(file_or_folder_name):
            shutil.rmtree(file_or_folder_name)
            print(f"{file_or_folder_name} deleted successfully.")
    else:
        print(f"File or folder {file_or_folder_name} not found.")
