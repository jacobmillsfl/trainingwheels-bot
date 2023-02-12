"""
    Datebase Utility module
"""

from typing import List
from tinydb import TinyDB, where

class DatabaseUtil:
    """
        A class for managing all database interactions
    """

    TABLE_LEETCODE_QUESTION = "Leetcode_Question"

    def __init__(self, database_path):
        self.database_path = database_path
        # Once we migrate to Docker,
        #  put this in a Docker volume such as '/leetcode_data/db.json'
        self.db = TinyDB(self.database_path)

    def table_leetcodequestion_insert_many(self, items : List[dict]) -> int:
        """
            Inserts a collection of items into the Leetcode_Question database
            table
        """
        table = self.db.table(self.TABLE_LEETCODE_QUESTION)
        inserts = 0
        for item in items:
            matches = table.search(where('id') == item['id'])
            if len(matches) == 0:
                table.insert(item)
                inserts += 1
        return inserts

    def table_leetcodequestion_loadall(self):
        """
            Loads all items in the Leetcode_Question database table
        """
        table = self.db.table(self.TABLE_LEETCODE_QUESTION)
        return table.all()

    def table_leetcodequestion_delete(self, question_id : int):
        """
            Deletes an item in the Leetcode_Question database table
        """

        table = self.db.table(self.TABLE_LEETCODE_QUESTION)
        return table.remove(where("id") == question_id)
