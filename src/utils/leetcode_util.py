"""
Leetcode Utility module
"""

from typing import List
import requests

from .query_builder import QueryBuilder

class LeetcodeUtil:
    """
    A class for interacting with Leetcode's APIs
    """

    GRAPH_URL = "https://leetcode.com/graphql/"
    PROBLEM_URL = "https://leetcode.com/problems/"
    ALL_PROBLEMS_URL = "https://leetcode.com/api/problems/all/"
    DATA_LIMIT = 100
    TIMEOUT = 10000

    def __init__(self):
        pass

    @staticmethod
    def api_questions_loadall() -> List[dict]:
        """
        Loads all questions from the leetcode API
        """

        results = []
        response = requests.get(LeetcodeUtil.ALL_PROBLEMS_URL, timeout=LeetcodeUtil.TIMEOUT)

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

    @staticmethod
    def get_user_rank(leetcode_username: str) -> str:
        """
        Gathers the provided user's rank
        """

        rank = ""
        query = QueryBuilder.query_builder_user_rank(leetcode_username)
        response = requests.get(LeetcodeUtil.GRAPH_URL,
                                json=query, timeout=10000)
        if response.ok:
            data = response.json()
            if len(data) == 0:
                rank = "Unable to find rank information for Leetcode username" \
                    f" `{leetcode_username}`"
            else:
                submissions = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
                submissions_easy = list(
                    filter(lambda x: x["difficulty"] == "Easy", submissions))
                submissions_med = list(
                    filter(lambda x: x["difficulty"] == "Medium", submissions))
                submissions_hard = list(
                    filter(lambda x: x["difficulty"] == "Hard", submissions))
                easy_count = submissions_easy.pop()["count"] if len(
                    submissions_easy) > 0 else 0
                med_count = submissions_med.pop()["count"] if len(
                    submissions_med) > 0 else 0
                hard_count = submissions_hard.pop()["count"] if len(
                    submissions_hard) > 0 else 0
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
        query = QueryBuilder.query_builder_recent_stats(leetcode_username, LeetcodeUtil.DATA_LIMIT)
        response = requests.get(LeetcodeUtil.GRAPH_URL,
                                json=query, timeout=LeetcodeUtil.TIMEOUT)
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

    @staticmethod
    def get_solution_by_id(solution_id: int) -> str:
        """
        Gather's a published Leetcode question solutions, including code
        """
        query = QueryBuilder.query_builder_solution_by_id(solution_id)
        response = requests.get(LeetcodeUtil.GRAPH_URL,
                                json=query, timeout=LeetcodeUtil.TIMEOUT)
        solution = ""
        if response.ok:
            response_json = response.json()
            if "errors" in response_json.keys():
                print("\n".join(response_json["errors"]))
            else:
                tags = [tag["slug"]
                        for tag in response_json["data"]["topic"]["solutionTags"]]
                tag_str = "\t".join(tags)
                code = response_json["data"]["topic"]["post"]["content"]
                solution = f"{tag_str}\n\n{code}"
        else:
            print(f"Response returned status code : {response.status_code}")
        return solution

    @staticmethod
    def get_user_solutions(leetcode_id: str) -> str:
        """
        Returns a list of all public solutions created by a Leetcode user
        """
        solutions = []
        next_page = True
        offset = 0
        skip = LeetcodeUtil.DATA_LIMIT
        while next_page:
            query = QueryBuilder.query_builder_user_submissions(
                leetcode_id, offset, skip)
            response = requests.get(
                LeetcodeUtil.GRAPH_URL, json=query, timeout=LeetcodeUtil.TIMEOUT)
            if response.ok:
                response_json = response.json()
                if "errors" in response_json.keys():
                    print("\n".join(response_json["errors"]))
                    break
                data = response_json["data"]
                next_page = data["userSolutionTopics"]["pageInfo"]["hasNextPage"]
                edges = data["userSolutionTopics"]["edges"]
                offset += skip
                for edge in edges:
                    solution = {
                        "id": int(edge["node"]["id"]),
                        "title": edge["node"]["title"],
                        "url": edge["node"]["url"],
                        "questionTitle": edge["node"]["questionTitle"],
                        "date": edge["node"]["post"]["creationDate"] * 1000
                    }
                    solution["code"] = LeetcodeUtil.get_solution_by_id(
                        solution["id"])
                    solutions.append(solution)
            else:
                print(
                    f"Response returned status code : {response.status_code}")

        return solutions
