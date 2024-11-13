import json
import os


class DBManager:
    """
    Class to manage interactions with db
    """

    def save(file_path: str, data: dict | list):
        """
        save data to file storage
        """
        with open(file_path, "w") as file:
            if isinstance(data, (dict, list)):
                json.dump(data, file)
            else:
                raise TypeError("Data must be of type dict or list")

    def load(file_path: str):
        """
        load data from the file storage
        """
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return None

    def count(file_path: str):
        """
        count number of entries in the file storage
        """
        data = DBManager.load(file_path)
        if not data:
            return 0

        return len(data)

    def initialize():
        """
        Creates a temp folder
        """
        folder_path = "src/db/temp"
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
