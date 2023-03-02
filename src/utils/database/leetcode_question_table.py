"""
Leetcode Question table module
"""

from typing import List
from tinydb import TinyDB, where
from tinydb.table import Document

# Decorator for validating database insert methods
def validate_insert(required_fields):
    """
    Python decorator function to validate objects before they are inserted
    into the database.

    Usage:
        Before any method that inserts data into the database, you should
        decorate the method as such:

        @validate_insert(required_fields = TABLE_XXXX_FIELDS)

        In the above, `TABLE_XXXX_FIELDS` should be the class constant variable
        containing a list of the required fields for the table to be inserted
        into.

    Note:
        This method does not prevent inserting duplicate values for unique
        fields. The insert method body should still enforce uniqueness
        where appropriate.
    """

    def decorator(func):
        def wrapper(self, *args):
            if (
                isinstance(args[0], dict)
                and all(field in args[0].keys() for field in required_fields)
                and len(args[0].keys()) == len(required_fields)
            ):
                return func(self, *args)
            return False  # Indicates validation failure

        return wrapper

    return decorator

class LeetcodeQuestionsTable():
    """
    Table to hold all questions pulled from Leetcode
    """
    TABLE_LEETCODE_QUESTION_FIELDS = ["id", "title", "title_slug", "difficulty"]
    TABLE_LEETCODE_QUESTION = "Leetcode_Question"

    def __init__(self, database: TinyDB):
        self.table = database.table(self.TABLE_LEETCODE_QUESTION)

    @validate_insert(required_fields=TABLE_LEETCODE_QUESTION_FIELDS)
    def insert(self, item: dict) -> bool:
        """
        Inserts an item into the Leetcode_Question database table
        """
        # Prevent duplicate ID's
        if len(self.table.search(where("id") == item["id"])) == 0:
            self.table.insert(item)
            return True
        return False

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
