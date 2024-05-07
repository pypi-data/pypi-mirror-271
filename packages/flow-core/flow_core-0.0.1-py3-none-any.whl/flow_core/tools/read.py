from promptflow.core import tool


@tool
def read(filename: str):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
