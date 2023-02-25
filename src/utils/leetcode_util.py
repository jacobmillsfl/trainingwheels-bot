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
    def query_builder_user_submissions(leetcode_username: str, offset: int, skip: int):
        """
        Builds a leetcode query to gather the provided user's submissions
        """
        query_user_submissions = {
            "query": """
                query userSolutionTopics($username: String!, $orderBy: TopicSortingOption, $skip: Int, $first: Int) {
                    userSolutionTopics(
                        username: $username
                        orderBy: $orderBy
                        skip: $skip
                        first: $first
                    ) {
                        pageInfo {
                            hasNextPage
                        }
                        edges {
                            node {
                                id
                                title
                                url
                                viewCount
                                questionTitle
                                post {
                                    creationDate
                                    voteCount
                                }
                            }
                        }
                    }
                }
            """,
            "variables": {
                "username": leetcode_username,
                "orderBy": "newest_to_oldest",
                "skip": skip,
                "first": offset
            }
        }
        return query_user_submissions

    @staticmethod
    def query_builder_solution_by_id(solution_id: int):
        """
        Builds a leetcode query to gather a specific submission
        """
        query_submission = {
            "query": """
                query communitySolution($topicId: Int!) {
                    isSolutionTopic(id: $topicId)
                    topic(id: $topicId) {
                        id
                        viewCount
                        topLevelCommentCount
                        favoriteCount
                        subscribed
                        title
                        pinned
                        solutionTags {
                            name
                            slug
                        }
                        hideFromTrending
                        commentCount
                        isFavorite
                        post {
                            id
                            voteCount
                            voteStatus
                            content
                            updationDate
                            creationDate
                            status
                            isHidden
                        author {
                            isDiscussAdmin
                            isDiscussStaff
                            username
                            nameColor
                            activeBadge {
                                displayName
                                icon
                            }
                            profile {
                                userAvatar
                                reputation
                            }
                            isActive
                        }
                        authorIsModerator
                        isOwnPost
                    }
                }
            }
            """,
            "variables": {
                "topicId": solution_id
            }
        }
        return query_submission

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

    @staticmethod
    def get_solution_by_id(solution_id: int) -> str:
        """
        Gather's a published Leetcode question solutions, including code
        """
        query = LeetcodeUtil.query_builder_solution_by_id(solution_id)
        response = requests.get(LeetcodeUtil.GRAPH_URL, json=query, timeout=10000)
        solution = ""
        if response.ok:
            response_json = response.json()
            if "errors" in response_json.keys():
                print("\n".join(response_json["errors"]))
            else:
                tags = [tag["slug"] for tag in response_json["data"]["topic"]["solutionTags"]]
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
        nextPage = True
        offset = 0
        skip = LeetcodeUtil.DATA_LIMIT
        while nextPage:
            query = LeetcodeUtil.query_builder_user_submissions(leetcode_id, offset, skip)
            response = requests.get(LeetcodeUtil.GRAPH_URL, json=query, timeout=10000)
            if response.ok:
                response_json = response.json()
                if "errors" in response_json.keys():
                    print("\n".join(response_json["errors"]))
                    break
                data = response_json["data"]
                nextPage = data["userSolutionTopics"]["pageInfo"]["hasNextPage"]
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
                    solution["code"] = LeetcodeUtil.get_solution_by_id(solution["id"])
                    solutions.append(solution)
            else:
                print(f"Response returned status code : {response.status_code}")

        return solutions
