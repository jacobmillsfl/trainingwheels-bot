"""
Leetcode Utility module
"""

from typing import List
from random import randint
from datetime import datetime

from dotenv import dotenv_values
import requests
from .database_util import DatabaseUtil


class LeetcodeUtil:
    """
    A class for interacting with Leetcode's APIs
    """

    GRAPH_URL = "https://leetcode.com/graphql/"
    PROBLEM_URL = "https://leetcode.com/problems/"
    ALL_PROBLEMS_URL = "https://leetcode.com/api/problems/all/"
    DATA_LIMIT = 100

    config = dotenv_values(".process.env")
    database = DatabaseUtil(config.get("DATABASE_NAME"))


    def __init__(self):
        pass

    @staticmethod
    def api_questions_loadall() -> List[dict]:
        """
        Loads all questions from the leetcode API
        """

        results = []
        response = requests.get(LeetcodeUtil.ALL_PROBLEMS_URL, timeout=10000)

        if response.ok:
            data = response.json()
            questions = data['stat_status_pairs']
            for question in questions:
                if question['paid_only']:
                    # Skip paid questions
                    continue

                # Format question into our database schema format for `Leetcode_Question`
                formatted_question = {
                    "id": question['stat']['question_id'],
                    "title": question['stat']['question__title'],
                    "titleSlug": question['stat']['question__title_slug'],
                    "difficulty": question['difficulty']['level'],
                }

                results.append(formatted_question)
        else:
            print(f"Response returned status code : {response.status_code}")

        return results


    # helper function to build the query specific to the user calling the command
    @staticmethod
    def query_builder_recent_stats(leetcode_username: str):
        """
        Gathers the provided user's recent stats
        """

        query_recent_stats = {
        "query": """
            query recentAcSubmissions($username: String!, $limit: Int!) {
                recentAcSubmissionList(username: $username, limit: $limit) {
                    id
                    title
                    titleSlug
                    timestamp
                }
            }
        """,
        "variables": {
            "username": leetcode_username,
            "limit": LeetcodeUtil.DATA_LIMIT
        }
        }
        return query_recent_stats

    @staticmethod
    def get_recent_submissions(leetcode_username: str) -> list:
        """
        Gathers the provided user's recent submissions
        """

        recent_completions = []
        query = LeetcodeUtil.query_builder_recent_stats(leetcode_username)
        response = requests.get(LeetcodeUtil.GRAPH_URL, json=query, timeout=10000)
        if response.ok:
            data = response.json()
            questions = data['data']['recentAcSubmissionList']
            for question in questions:
                completion = {
                    "title": question["title"],
                    "titleSlug": question["titleSlug"]
                }
                recent_completions.append(completion)
        else:
            print(f"Response returned status code : {response.status_code}")

        return recent_completions

    @staticmethod
    def check_challenge_completion(leetcode_id: str, title_slug: str) -> bool:
        """
        Determines if a user has completed a given challenge
        """
        submissions = LeetcodeUtil.get_recent_submissions(leetcode_id)
        for submission in submissions:
            if submission["titleSlug"] == title_slug:
                return True
        return False

    def weeklychallenge_generate(self) -> bool:
        """
        Generates a new weekly challenge with 3 questions that have not been used before.
        """

        previous_challenge = self.database.table_weeklychallenge_getlatest()
        if previous_challenge is None:
            challenge_id = 1
        else:
            challenge_id = previous_challenge["id"] + 1

        weight = 0
        max_weight = 5
        easy_weight = 1
        medium_weight = 2
        hard_weight = 3

        questions = []

        while weight < max_weight and len(questions) < 3:
            #Adjust randint() range to adjust probabilities of each difficulty
            difficulty_selector = randint(0,3)
            if difficulty_selector == 3 and max_weight - weight >= hard_weight:
                question = self.database.table_leetcodequestion_getrandom_newby_difficulty("hard")
                formatted_question = {challenge_id, question["title_slug"]}
                questions.append(formatted_question)
                weight += hard_weight
            elif difficulty_selector > 1 and max_weight - weight >= medium_weight:
                question = self.database.table_leetcodequestion_getrandom_newby_difficulty("medium")
                formatted_question = {challenge_id, question["title_slug"]}
                questions.append(formatted_question)
                weight += medium_weight
            else:
                question = self.database.table_leetcodequestion_getrandom_newby_difficulty("easy")
                formatted_question = {challenge_id, question["title_slug"]}
                questions.append(formatted_question)
                weight += easy_weight

        timestamp = int(datetime.utcnow().timestamp())
        date = datetime.fromtimestamp(timestamp)
        self.database.table_weeklychallenge_insert(challenge_id, date)

        for question in questions:
            self.database.table_weeklyquestion_insert(question)

        return len(questions) > 0
