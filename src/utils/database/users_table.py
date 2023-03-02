"""
User Table module
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

class UsersTable():
    """
    Table to hold all registered users
    """
    TABLE_LEETCODE_USER_FIELDS = ["discord_id", "leetcode_id"]
    TABLE_LEETCODE_USER = "Leetcode_User"

    def __init__(self, database: TinyDB):
        self.table = database.table(self.TABLE_LEETCODE_USER)

    def loadall(self) -> List[Document]:
        """
        Loads all items in the Leetcode_User database table
        """
        return self.table.all()

    @validate_insert(required_fields=TABLE_LEETCODE_USER_FIELDS)
    def insert(self, item: dict) -> bool:
        """
        Inserts a collection of items in the LeetcodeUser database table
        """
        matches = self.table.search(
            where("discord_id") == item["discord_id"]
            or where("leetcode_id") == item["leetcode_id"]
        )
        if len(matches) == 0:
            self.table.insert(item)
            return True
        return False

    def load_by_discord_id(self, discord_id):
        """
        Loads a single item by discord id in the "Leetcode_User" database table
        """
        users = self.table.search(where("discord_id") == discord_id)
        if len(users) == 0:
            return None
        return users[0]

    def load_by_leetcode_id(self, leetcode_id):
        """
        Loads a single item by leetcode id in the "Leetcode_User" database table
        """
        users = self.table.search(where("leetcode_id") == leetcode_id)
        if len(users) == 0:
            return None
        return users[0]

    def delete_by_leetcode_id(self, leetcode_id) -> bool:
        """
        Deletes an item by leetcode_id in the Leetcode_User database table
        """
        results = self.table.remove(where("leetcode_id") == leetcode_id)

        # Will return True if an item was successfully deleted
        return len(results) > 0

    def delete_by_discord_id(self, discord_id) -> bool:
        """
        Deletes an item by discord_id in the Leetcode_User database table
        """
        results = self.table.remove(where("discord_id") == discord_id)

        # Will return True if an item was successfully deleted
        return len(results) > 0
