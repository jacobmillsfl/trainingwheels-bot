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
                    "title_slug": question['stat']['question__title_slug'],
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
    def query_builder_user_rank(leetcode_username: str):
        """
        Builds a leetcode query to gather the provided user's rank
        """
        query_user_rank = {
            "query": """
                query getUserProfile($username: String!) { 
                    allQuestionsCount { 
                        difficulty count 
                    } matchedUser(username: $username) { 
                        contributions { 
                            points 
                        } profile { 
                            reputation ranking 
                        } submissionCalendar submitStats { 
                            acSubmissionNum { 
                                difficulty count submissions 
                            } totalSubmissionNum { 
                                difficulty count submissions 
                            } 
                        } 
                    } 
                }
            """,
            "variables": {
                "username": leetcode_username
            }
        }
        return query_user_rank

    @staticmethod
    def get_user_rank(leetcode_username: str) -> str:
        """
        Gathers the provided user's rank
        """

        rank = ""
        query = LeetcodeUtil.query_builder_user_rank(leetcode_username)
        response = requests.get(LeetcodeUtil.GRAPH_URL, json=query, timeout=10000)
        if response.ok:
            data = response.json()
            if len(data) == 0:
                rank = "Unable to find rank information for Leetcode username" \
                    f" `{leetcode_username}`"
            else:
                submissions = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
                submissions_easy = list(filter(lambda x: x["difficulty"] == "Easy" , submissions))
                submissions_med = list(filter(lambda x: x["difficulty"] == "Medium" , submissions))
                submissions_hard = list(filter(lambda x: x["difficulty"] == "Hard" , submissions))
                easy_count = submissions_easy.pop()["count"] if len(submissions_easy) > 0 else 0
                med_count = submissions_med.pop()["count"] if len(submissions_med) > 0 else 0
                hard_count = submissions_hard.pop()["count"] if len(submissions_hard) > 0 else 0
                rank = f"""
Name:                {leetcode_username}
Ranking:             {data['data']['matchedUser']['profile']['ranking']}
Contribution Points: {data['data']['matchedUser']['contributions']['points']}
Easy Challenges:     {easy_count}
Medium Challenges:   {med_count}
Hard Challenges:     {hard_count}
"""

        else:
            rank = f"Leetcode API Error {response.status_code}"

        return rank

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
                    "title_slug": question["titleSlug"]
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
            if submission["title_slug"] == title_slug:
                return True
        return False
