"""
Leetcode Question table module
"""

from typing import List
from tinydb import TinyDB, where
from tinydb.table import Document
from .db_decorators import validate_insert

class LeetcodeQuestionsTable():
    """
    Table to hold all questions pulled from Leetcode
    """
    TABLE_FIELDS = ["id", "title", "title_slug", "difficulty"]
    TABLE_NAME = "Leetcode_Question"

    def __init__(self, database: TinyDB):
        self.table = database.table(self.TABLE_NAME)

    def insert_many(self, items: List[dict]) -> int:
        """
        Inserts a collection of items into the Leetcode_Question database
        table
        """
        inserts = 0
        for item in items:
            if self.insert(item):
                inserts += 1
        return inserts

    @validate_insert(required_fields=TABLE_FIELDS)
    def insert(self, item: dict) -> bool:
        """
        Inserts an item into the Leetcode_Question database table
        """
        # Prevent duplicate ID's
        if len(self.table.search(where("id") == item["id"])) == 0:
            self.table.insert(item)
            return True
        return False

    def load(self, question_id):
        """
        Loads a single item by question_id in the Leetcode_Question database table
        """
        questions = self.table.search(where("id") == question_id)
        if len(questions) == 0:
            return None
        return questions[0]

    def loadall(self) -> List[Document]:
        """
        Loads all items in the Leetcode_Question database table
        """
        return self.table.all()

    def delete(self, question_id: int):
        """
        Deletes an item in the Leetcode_Question database table
        """
        return self.table.remove(where("id") == question_id)
