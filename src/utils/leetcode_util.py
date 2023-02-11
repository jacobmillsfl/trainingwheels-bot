import requests
from typing import List

class LeetcodeUtil:
    GRAPH_URL = "https://leetcode.com/graphql/"
    PROBLEM_URL = "https://leetcode.com/problems/"
    ALL_PROBLEMS_URL = "https://leetcode.com/api/problems/all/"
    data_limit = 100

    def __init__(self):
        pass

    @staticmethod
    def api_questions_loadall() -> List[dict]:
        results = []
        response = requests.get(LeetcodeUtil.ALL_PROBLEMS_URL)

        if (response.ok):
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
            "limit": LeetcodeUtil.data_limit
        }
        }
        return query_recent_stats

    # returns a list of recently completed Leetcode challenges as a dictionary.  dict{ id : title}
    @staticmethod
    def get_recent_submissions(leetcode_username: str):
        recent_completions = {}
        query = LeetcodeUtil.query_builder_recent_stats(leetcode_username)
        response = requests.get(LeetcodeUtil.GRAPH_URL, json=query)
        if(response.ok):
            data = response.json()
            questions = data['data']['recentAcSubmissionList']
            for question in questions:
                recent_completions[question['id']] = question['title']
        else:
            print(f"Response returned status code : {response.status_code}")

        return recent_completions


