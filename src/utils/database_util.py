"""
    Datebase Utility module
"""

from typing import List
from tinydb import TinyDB, where
# from src.utils.database_util import DatabaseUtil
# For running/testing locally
# source bot-env/bin/activate

class DatabaseUtil:
    """
    A class for managing all database interactions
    """

    TABLE_LEETCODE_QUESTION = "Leetcode_Question"
    TABLE_LEETCODE_USER = "Leetcode_User"

    def __init__(self, database_path):
        self.database_path = database_path
        # Once we migrate to Docker,
        #  put this in a Docker volume such as '/leetcode_data/db.json'
        self.db = TinyDB(self.database_path)

    def table_leetcodequestion_insert_many(self, items: List[dict]) -> int:
        """
        Inserts a collection of items into the Leetcode_Question database
        table
        """

        table = self.db.table(self.TABLE_LEETCODE_QUESTION)
        inserts = 0
        for item in items:
            matches = table.search(where("id") == item["id"])
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

    def table_leetcodequestion_delete(self, question_id: int):
        """
        Deletes an item in the Leetcode_Question database table
        """

        table = self.db.table(self.TABLE_LEETCODE_QUESTION)
        return table.remove(where("id") == question_id)

    def table_leetcodeuser_insert(self, item: dict) -> bool:
        """
        Inserts a collection of items in the LeetcodeUser database table
        """
        table = self.db.table(self.TABLE_LEETCODE_USER)
        matches = table.search(where("discord_id") == item["discord_id"] \
        or where("leetcode_id") == item["leetcode_id"])
        if len(matches) == 0:
            table.insert(item)
            return True
        return False

    def table_leetcodeuser_load_by_discord_id(self, discord_id):
        """
            Loads a single item by discord id in the "Leetcode_User" database table
        """
        table = self.db.table(self.TABLE_LEETCODE_USER)
        users = table.search(where("discord_id") == discord_id)
        if len(users) == 0:
            return None
        return users[0]

    def table_leetcodeuser_load_by_leetcode_id(self, leetcode_id):
        """
            Loads a single item by leetcode id in the "Leetcode_User" database table
        """
        table = self.db.table(self.TABLE_LEETCODE_USER)
        users = table.search(where("leetcode_id") == leetcode_id)
        if len(users) == 0:
            return None
        return users[0]

    def table_leetcodeuser_loadall(self):
        """
            Loads all items in the Leetcode_User database table
        """
        table = self.db.table(self.TABLE_LEETCODE_USER)
        return table.all()
