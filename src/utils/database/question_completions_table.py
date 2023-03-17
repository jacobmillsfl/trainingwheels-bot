"""
Question Completions module
"""

from typing import List
from tinydb import TinyDB, where
from .db_decorators import validate_insert

class QuestionCompletionsTable():
    """
    Table to store all completed questions by leetcode user ID & title slug
    """
    TABLE_FIELDS = ["leetcode_id", "title_slug"]
    TABLE_NAME = "Question_Completions"

    def __init__(self, database: TinyDB):
        self.table = database.table(self.TABLE_NAME)

    @validate_insert(required_fields=TABLE_FIELDS)
    def insert(self, item: dict) -> bool:
        """
        Inserts a single item of leetcode_id and title_slug to QuestionCompletions database table
        """
        matches = self.table.search(
            where("leetcode_id") == item["leetcode_id"]
            and where("title_slug") == item["title_slug"]

        )
        if len(matches) == 0:
            self.table.insert(item)
            return True
        return False

    def insert_many(self, leetcode_id: str, items: List[dict]) -> int:
        """
        Inserts a collection of items into the Question Completions database table
        """
        inserts = 0
        for item in items:
            completion_insert = {"leetcode_id": leetcode_id, "title_slug": item["title_slug"]}
            if self.insert(completion_insert):
                inserts += 1
        return inserts

    def load(self, leetcode_id: str, title_slug: str):
        """
        Load a single item by leetcode_id and title_slug in the Question Completions database table
        """
        completion = self.table.search(
            where("leetcode_id") == leetcode_id
            and where("title_slug") == title_slug
        )
        if len(completion) == 0:
            return None
        return completion[0]

    def load_all_title_slugs_by_user(self, leetcode_id):
        """
        Loads a list of all title slugs in the Question Completions database table
        """
        results = self.table.search(where("leetcode_id") == leetcode_id)
        title_slugs = []
        for item in results:
            title_slugs.append(item["title_slug"])
        return title_slugs

    def check_completion(self, leetcode_id: str, title_slug: str) -> bool:
        """
        Checks if a user has completed a question per the Question Completions database table
        """
        completed = self.load(leetcode_id, title_slug)
        if completed:
            return True
        return False
