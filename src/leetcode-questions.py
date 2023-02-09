"""
Notice: This is a proof of concept for interacting with leetcode's API in Python.
        The logic here should be formalized into Python classes elsewhere in the solution.
"""

import requests
import json

graph_url = "https://leetcode.com/graphql/"
problem_url = "https://leetcode.com/problems/"
headers = {
    "authority": "leetcode.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://leetcode.com"
}

data_categorySlug = ""
data_skip = 0
data_limit = 50
data_filters = {}

COMMA_DELIM = ', '

query_all_problems = {"query": """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
    problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
    ) {
        total: totalNum
        questions: data {
        acRate
        difficulty
        freqBar
        frontendQuestionId: questionFrontendId
        isFavor
        paidOnly: isPaidOnly
        status
        title
        titleSlug
        topicTags {
            name
            id
            slug
        }
        hasSolution
        hasVideoSolution
        }
      }
    }""",
    "variables": {
        "categorySlug":data_categorySlug,
        "skip":data_skip,
        "limit":data_limit,
        "filters":data_filters
    }
}

query_stats = {"query":"""query getUserProfile($username: String!) { 
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
}""",
"variables": {
    "username":"link787"
    }
}

response = requests.get(graph_url, headers=headers, json=query_all_problems)

if (response.ok):
    parsed_response = json.loads(response.text)
    print(f"Total questions: {parsed_response['data']['problemsetQuestionList']['total']}")
    questions = parsed_response['data']['problemsetQuestionList']['questions']
    for question in questions:
        print(f"Title: {question['title']}")
        print(f"Difficulty: {question['difficulty']}")
        print(f"Tags: {COMMA_DELIM.join(tag['name'] for tag in question['topicTags'])}")
        print(f"URL: {problem_url}{question['titleSlug']}\n")

