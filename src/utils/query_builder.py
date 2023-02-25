"""
Query Builder helper class
"""
class QueryBuilder:
    """
    Query Builder to help build Leetcode queries within leetcode_util.py
    """

    # helper function to build the query specific to the user calling the command
    @staticmethod
    def query_builder_recent_stats(leetcode_username: str, data_limit: int):
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
            "limit": data_limit
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
