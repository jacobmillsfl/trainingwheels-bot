"""
    Leetcode Utility module
"""

from typing import List
import requests

class LeetcodeUtil:
    """
        A class for interacting with Leetcode's APIs
    """

    GRAPH_URL = "https://leetcode.com/graphql/"
    PROBLEM_URL = "https://leetcode.com/problems/"
    ALL_PROBLEMS_URL = "https://leetcode.com/api/problems/all/"
    DATA_LIMIT = 100

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

    # returns a list of recently completed Leetcode challenges as a dictionary.  dict{ id : title}
    @staticmethod
    def get_recent_submissions(leetcode_username: str):
        """
            Gathers the provided user's recent submissions
        """

        recent_completions = {}
        query = LeetcodeUtil.query_builder_recent_stats(leetcode_username)
        response = requests.get(LeetcodeUtil.GRAPH_URL, json=query, timeout=10000)
        if response.ok:
            data = response.json()
            questions = data['data']['recentAcSubmissionList']
            for question in questions:
                recent_completions[question['id']] = question['title']
        else:
            print(f"Response returned status code : {response.status_code}")

        return recent_completions
