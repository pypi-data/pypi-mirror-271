import os
from typing import Optional

from promptflow.core import tool


@tool
def create(
    value: str,
    folder: Optional[str] = None,
    file_name: Optional[str] = None,
):
    try:
        if folder:
            # Create the folder if it doesn't exist
            os.makedirs(folder, exist_ok=True)
            if file_name:
                file_path = os.path.join(folder, file_name)
            else:
                file_path = os.path.join(folder, "new_file.txt")
        elif folder:
            # Create the folder if it doesn't exist
            os.makedirs(folder, exist_ok=True)
            if file_name:
                file_path = os.path.join(folder, file_name)
            else:
                file_path = os.path.join(folder, "new_file.txt")
        else:
            if file_name:
                file_path = file_name
            else:
                file_path = "new_file.txt"

        # Open the file in write mode
        with open(file_path, "w") as file:
            # Write the data to the file
            file.write(value)
    except Exception as e:
        print("An error occurred:", str(e))
