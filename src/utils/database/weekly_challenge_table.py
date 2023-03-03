"""
Weekly Challenge table module
"""

from tinydb import TinyDB, where
from .db_decorators import validate_insert

class WeeklyChallengeTable():
    """
    Table to hold all Weekly Challenges after being generated
    """
    TABLE_FIELDS = ["id", "date"]
    TABLE_NAME = "Weekly_Challenge"

    def __init__(self, database: TinyDB):
        self.table = database.table(self.TABLE_NAME)

    @validate_insert(required_fields=TABLE_FIELDS)
    def insert(self, item: dict) -> bool:
        """
        "Inserts an item to the Weekly_Challenge table"
        """

        # Prevent duplicate ID's
        if len(self.table.search(where("id") == item["id"])) == 0:
            self.table.insert(item)
            return True
        return False

    def load(self, challenge_id):
        """
        Loads an item by id from the Weekly_Challenge table
        """
        results = self.table.search(where("id") == challenge_id)
        if len(results) == 0:
            return None
        return results[0]

    def get_latest(self):
        """
        Loads the item with the most recent date property
        """
        results = self.table.all()
        if len(results) == 0:
            return None
        sorted_results = sorted(results, key=lambda challenge: challenge["date"])
        return sorted_results[-1]
