"""
    Datebase Utility module
"""
from datetime import datetime
from typing import List
from tinydb import TinyDB, where

from .users_table import UsersTable
from .weeklyquestion_table import WeeklyQuestionTable
from .leetcode_question_table import LeetcodeQuestionsTable
from .weekly_challenge_table import WeeklyChallengeTable
from .question_completions_table import QuestionCompletionsTable

# Database Utility Class Definition
class DatabaseUtil:
    """
    A class for managing all database interactions, with member classes for each table.
    """

    def __init__(self, database_path: str):
        self.database_path = database_path
        self.db = TinyDB(self.database_path)
        self.users = UsersTable(self.db)
        self.weekly_questions = WeeklyQuestionTable(self.db)
        self.leetcode_questions = LeetcodeQuestionsTable(self.db)
        self.weekly_challenges = WeeklyChallengeTable(self.db)
        self.question_completions = QuestionCompletionsTable(self.db)



    def create_new_weekly_challenge(self, question_list: List[dict]) -> str:
        """
        Creates a new weekly challenge and weekly questions
        """
        message = ""
        success = True
        last_chal = self.weekly_challenges.get_latest()
        if last_chal:
            new_chal_id = last_chal["id"] + 1
        else:
            new_chal_id = 1
        timestamp = datetime.timestamp(datetime.now())
        challenge = {"id": new_chal_id, "date": timestamp}
        chal_success = self.weekly_challenges.insert(challenge)
        if chal_success:
            for question in question_list:
                weekly_question = {**question, "challenge_id": new_chal_id}
                question_success = self.weekly_questions.insert(weekly_question)
                if not question_success:
                    message += (
                        f"Error creating weekly question `{question['title_slug']}`\n"
                    )
                    success = False
        else:
            message += "Error creating weekly challenge"
            success = False
        if success:
            message = "Challenge created successfully!"
        return message

    def delete_weekly_challenge(self, challenge_id: int) -> bool:
        """
        Deletes an item in the Weekly_Challenge database table and
        calls weeklyquestion_delete_by_challenge_id() to delete associated questions from
        Weekly_Question database table
        """

        self.weekly_questions.delete_by_challenge_id(challenge_id)
        results = self.weekly_challenges.table.remove(where("id") == challenge_id)
        return len(results) > 0
