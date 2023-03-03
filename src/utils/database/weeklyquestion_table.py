"""
Weekly Question table module
"""

from typing import List
from tinydb import TinyDB, where
from tinydb.table import Document
from .db_decorators import validate_insert

class WeeklyQuestionTable:
    """
    A class to act on the weeklyquestion_table of the database
    """
    TABLE_FIELDS = [
        "id",
        "challenge_id",
        "title",
        "title_slug",
        "difficulty",
    ]
    TABLE_NAME = "Weekly_Question"

    def __init__(self, database: TinyDB):
        self.table = database.table(self.TABLE_NAME)


    @validate_insert(required_fields=TABLE_FIELDS)
    def insert(self, item: dict) -> bool:
        """
        Inserts an item into the Weekly_Question database table
        """
        # Prevent duplicate ID's
        if len(self.table.search(where("title_slug") == item["title_slug"])) == 0:
            self.table.insert(item)
            return True
        return False

    def load_by_challenge_id(self, challenge_id) -> list:
        """
        Loads multiple items by challenge id in the Weekly_Question database table
        """
        return self.table.search(where("challenge_id") == challenge_id)

    def load_by_title_slug(self, title_slug):
        """
        Loads a single item by title slug in the Weekly_Question database table
        """
        questions = self.table.search(where("title_slug") == title_slug)
        if len(questions) == 0:
            return None
        return questions[0]

    def delete(self, title_slug) -> bool:
        """
        Deletes an item in the Weekly_Question database table
        """
        results = self.table.remove(where("title_slug") == title_slug)
        return len(results) > 0

    def delete_by_challenge_id(self, challenge_id) -> bool:
        """
        Deletes multiple items by challenge_id in the Weekly_Question database table
        called by table_weeklychallenge_delete()
        """
        results = self.table.remove(where("challenge_id") == challenge_id)
        return len(results) > 0

    def loadall(self) -> List[Document]:
        """
        Loads all items in the Weekly_Question database table
        """
        return self.table.all()
