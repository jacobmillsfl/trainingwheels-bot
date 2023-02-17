"""
    Datebase Utility module
"""

from typing import List
from tinydb import TinyDB, where

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
            if isinstance(args[0], dict) \
                and all(field in args[0].keys() for field in required_fields) \
                and len(args[0].keys()) == len(required_fields):
                return func(self, *args)
            return False # Indicates validation failure
        return wrapper
    return decorator

# Database Utility Class Definition
class DatabaseUtil:
    """
    A class for managing all database interactions
    """

    # Table Names
    TABLE_LEETCODE_QUESTION = "Leetcode_Question"
    TABLE_LEETCODE_USER = "Leetcode_User"
    TABLE_WEEKLY_CHALLENGE = "Weekly_Challenge"
    TABLE_WEEKLY_QUESTION = "Weekly_Question"

    # Table Fields
    TABLE_LEETCODE_QUESTION_FIELDS = ["id", "title", "titleSlug", "difficulty"]
    TABLE_LEETCODE_USER_FIELDS = ["discord_id", "leetcode_id"]
    TABLE_WEEKLY_CHALLENGE_FIELDS = ["id", "date"]
    TABLE_WEEKLY_QUESTION_FIELDS = ["challenge_id", "title_slug"]

    def __init__(self, database_path):
        self.database_path = database_path
        # Once we migrate to Docker,
        #  put this in a Docker volume such as '/leetcode_data/db.json'
        self.db = TinyDB(self.database_path)

    @validate_insert(required_fields=TABLE_LEETCODE_QUESTION_FIELDS)
    def table_leetcodequestion_insert(self, item: dict) -> bool:
        """
        Inserts an item into the Leetcode_Question database table
        """
        table = self.db.table(self.TABLE_LEETCODE_QUESTION)

        # Prevent duplicate ID's
        if len(table.search(where("id") == item["id"])) == 0:
            table.insert(item)
            return True
        return False

    def table_leetcodequestion_insert_many(self, items: List[dict]) -> int:
        """
        Inserts a collection of items into the Leetcode_Question database
        table
        """
        inserts = 0
        for item in items:
            if self.table_leetcodequestion_insert(item):
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

    @validate_insert(required_fields=TABLE_LEETCODE_USER_FIELDS)
    def table_leetcodeuser_insert(self, item: dict) -> bool:
        """
        Inserts a collection of items in the LeetcodeUser database table
        """
        table = self.db.table(self.TABLE_LEETCODE_USER)
        matches = table.search(
            where("discord_id") == item["discord_id"]
            or where("leetcode_id") == item["leetcode_id"]
        )
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

    def table_leetcodeuser_delete_by_leetcode_id(self, leetcode_id) -> bool:
        """
        Deletes an item by leetcode_id in the Leetcode_User database table
        """

        table = self.db.table(self.TABLE_LEETCODE_USER)
        results = table.remove(where("leetcode_id") == leetcode_id)

        # Will return True if an item was successfully deleted
        return len(results) > 0

    def table_leetcodeuser_delete_by_discord_id(self, discord_id) -> bool:
        """
        Deletes an item by discord_id in the Leetcode_User database table
        """

        table = self.db.table(self.TABLE_LEETCODE_USER)
        results = table.remove(where("discord_id") == discord_id)

        # Will return True if an item was successfully deleted
        return len(results) > 0

    @validate_insert(required_fields=TABLE_WEEKLY_CHALLENGE_FIELDS)
    def table_weeklychallenge_insert(self, item: dict) -> bool:
        """
        Inserts an item from the Weekly_Challenge table
        """
        table = self.db.table(self.TABLE_WEEKLY_CHALLENGE)

        # Prevent duplicate ID's
        if len(table.search(where("id") == item["id"])) == 0:
            table.insert(item)
            return True
        return False

    def table_weeklychallenge_load(self, challenge_id):
        """
        Loads an item by id from the Weekly_Challenge table
        """

        table = self.db.table(self.TABLE_WEEKLY_CHALLENGE)
        results = table.search(where("id") == challenge_id)
        if len(results) == 0:
            return None
        return results[0]

    def table_weeklychallenge_getlatest(self):
        """
        Loads the item with the most recent date property
        """

        table = self.db.table(self.TABLE_WEEKLY_CHALLENGE)
        results = table.all()
        if len(results) == 0:
            return None
        sorted_results = sorted(results, key=lambda challenge: challenge["date"])
        return sorted_results[-1]

    def table_weeklychallenge_delete(self, challenge_id: int) -> bool:
        """
        Deletes an item in the Weekly_Challenge database table and 
        calls weeklyquestion_delete_by_challenge_id() to delete associated questions from
        Weekly_Question database table
        """
        self.table_weeklyquestion_delete_by_challenge_id(challenge_id)
        table = self.db.table(self.TABLE_WEEKLY_CHALLENGE)
        results = table.remove(where("id") == challenge_id)
        return len(results) > 0

    @validate_insert(required_fields=TABLE_WEEKLY_QUESTION_FIELDS)
    def table_weeklyquestion_insert(self, item: dict) -> bool:
        """
        Inserts an item into the Weekly_Question database table
        """
        table = self.db.table(self.TABLE_WEEKLY_QUESTION)

        # Prevent duplicate ID's
        if len(table.search(where("title_slug") == item["title_slug"])) == 0:
            table.insert(item)
            return True
        return False

    def table_weeklyquestion_load_by_challenge_id(self, challenge_id) -> list:
        """
        Loads multiple items by challenge id in the Weekly_Question database table
        """
        table = self.db.table(self.TABLE_WEEKLY_QUESTION)
        return table.search(where("challenge_id") == challenge_id)

    def table_weeklyquestion_load_by_title_slug(self, title_slug):
        """
        Loads a single item by title slug in the Weekly_Question database table
        """
        table = self.db.table(self.TABLE_WEEKLY_QUESTION)
        questions = table.search(where("title_slug") == title_slug)
        if len(questions) == 0:
            return None
        return questions[0]

    def table_weeklyquestion_delete(self, title_slug) -> bool:
        """
        Deletes an item in the Weekly_Question database table
        """
        table = self.db.table(self.TABLE_WEEKLY_QUESTION)
        results = table.remove(where("title_slug") == title_slug)
        return len(results) > 0

    def table_weeklyquestion_delete_by_challenge_id(self, challenge_id) -> bool:
        """
        Deletes multiple items by challenge_id in the Weekly_Question database table
        called by table_weeklychallenge_delete()
        """
        table = self.db.table(self.TABLE_WEEKLY_QUESTION)
        results = table.remove(where("challenge_id") == challenge_id)
        return len(results) > 0
