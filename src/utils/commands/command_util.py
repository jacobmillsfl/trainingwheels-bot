"""
Command Utility module
"""
import random
from datetime import datetime

#from .command_abc import CommandAbstract
from ..database.database_util import DatabaseUtil
from ..leetcode_util import LeetcodeUtil
from ..emojis import Emojis
from ..misc.maps import QUESTION_DIFFICULTY_MAP

class CommandUtil():
    """
    An interface for classes that will support leetcode bot commands
    """

    USAGE_MESSAGE = """
Supported commands:
!help                   -   Display help information
!claim <leetcode_id>    -   Associate <leetcode_id> with the user's discord_id
!challenge              -   Display the latest weekly challenge
!rank                   -   Display user's all time Leetcode status
!status                 -   Display user's completion status of current weekly challenge
!new-challenge          -   Generate a new Weekly Challenge
!group-status           -   Display all users' completion status of current weekly challenge
"""

    def __init__(self, database: DatabaseUtil, leetcode: LeetcodeUtil, discord_mode=False):
        self.database = database
        self.discord_mode = discord_mode
        self.leetcode = leetcode
        self.reaction_complete = Emojis.check_mark if discord_mode else "Complete"
        self.reaction_incomplete = Emojis.red_x if discord_mode else "Incomplete"

    def claim(self, discord_id: str, leetcode_id: str) -> str:
        """
        Associates a leetcode_id with a discord_id in the Leetcode_User table.
        Local only, no API required.
        Database required.
        """
        message = ""
        create_user = False
        claimed_user = self.database.users.load_by_leetcode_id(leetcode_id)
        existing_user = self.database.users.load_by_discord_id(discord_id)
        if claimed_user and claimed_user["discord_id"] != discord_id:
            message += f"`{claimed_user['leetcode_id']}` is already claimed!"
        elif existing_user and existing_user["leetcode_id"] == leetcode_id:
            message += "Your account is already registered"
        elif existing_user:
            message += (
                "Your account is already registered with Leetcode username"
                f" `{existing_user['leetcode_id']}`\n"
            )
            message += "Deleting association... "
            deleted = self.database.users.delete_by_discord_id(discord_id)
            if deleted:
                message += "Deletion success!\n"
                create_user = True
            else:
                message += "An error occurred during user deletion\n"
        else:
            create_user = True
        if create_user:
            user = {"discord_id": discord_id, "leetcode_id": leetcode_id}
            success = self.database.users.insert(user)
            if success:
                message += f"Leetcode Username `{leetcode_id}` successfully claimed!\n"
            else:
                message += f"Error: {leetcode_id} already in use!\n"
        return message

    def challenge(self) -> str:
        """
        Determines the current weekly challenge.
        Local only, no API required.
        Database required.
        """
        latest = self.database.weekly_challenges.get_latest()
        if latest:
            start_date = datetime.fromtimestamp(latest["date"])
            result = f"* * * CHALLENGE {latest['id']} | {start_date.date()} * * *\n\n"
            questions = self.database.weekly_questions.load_by_challenge_id(latest["id"])
            for q in questions:
                question = self.database.leetcode_questions.load(q["id"])
                result += f"Question:\t{question['title']}\n"
                result += (
                    f"Difficulty:\t{QUESTION_DIFFICULTY_MAP[question['difficulty']]}\n"
                )
                result += f"URL:\t\t<https://leetcode.com/problems/{question['title_slug']}/>\n\n"
        else:
            result = "There are no challenges at this time"
        return result

    def rank(self, discord_id: str) -> str:
        """
        Determines a summary of leet stats for the current user.
        Calls the `rank`/`stats` leetcode API and returns results.
        No database required.
        """
        user = self.database.users.load_by_discord_id(discord_id)
        if user:
            leetcode_user_id = user["leetcode_id"]
            result = self.leetcode.get_user_rank(leetcode_user_id)
        else:
            result = (
                "Leetcode user not found. Claim your user idea with"
                " `!claim <leetcode_username>`"
            )
        return result

    def status(self, discord_id: str) -> str:
        """
        Determines the completion status of each question in the current
        weekly challenge for the given leetcode_user_id. Calls the
        `submissions` leetcode API to determine which of the weekly
        challenge problems the given user has solved. Gathers the list
        of current weekly challenges from the database.
        """
        result = ""
        user = self.database.users.load_by_discord_id(discord_id)
        if user:
            leetcode_user_id = user["leetcode_id"]
            challenge = self.database.weekly_challenges.get_latest()
            if not challenge:
                result += "No current challenges"
            else:
                questions = self.database.weekly_questions.load_by_challenge_id(challenge["id"])
                total = len(questions)
                if total == 0:
                    result += "No current weekly questions"
                else:
                    completed = 0
                    for question in questions:
                        question["complete"] = self.leetcode.check_challenge_completion(
                            leetcode_user_id, question["title_slug"]
                        )
                        if question["complete"]:
                            completed += 1
                    percentage = int(completed/total * 100)
                    result += f"User {leetcode_user_id}'s Weekly Challenge status: {percentage}%\n"
                    for question in questions:
                        complete = question["complete"]
                        result += (
                            f"\t{self.reaction_complete if complete else self.reaction_incomplete}"
                            f"\t-\t{question['title']}\n"
                        )
        else:
            result += "Leetcode user not found. Claim your user idea with"
            result += " `!claim <leetcode_username>`"
        return result

    def new_challenge(self) -> str:
        """
        Generates a new Weekly Challenge
        """
        questions = self.database.leetcode_questions.loadall()
        previous_questions = self.database.weekly_questions.loadall()
        previous_question_slugs = [q["title_slug"] for q in previous_questions]
        valid_questions = list(
            filter(lambda q: q["title_slug"]
                   not in previous_question_slugs, questions)
        )
        random.shuffle(valid_questions)
        weekly_questions = []
        current_difficulty = 0
        for question in valid_questions:
            if question["difficulty"] + current_difficulty <= 5:
                weekly_questions.append(question)
                current_difficulty += question["difficulty"]
                if current_difficulty >= 5:
                    break
        # Insert new questions into datbase
        return self.database.create_new_weekly_challenge(weekly_questions)

    def user(self, discord_id: str) -> str:
        """
        Gets the leetcode_id of the requested user
        """
        return_message = ""
        user = self.database.users.load_by_discord_id(discord_id)
        if not user:
            return_message = "User not found"
        else:
            return_message = user["leetcode_id"]
        return return_message

    def group_status(self) -> str:
        """
        Calculates and summarizes the number of users who have completed each question
        in the current challenge
        """
        result = ""
        users = self.database.users.loadall()
        challenge = self.database.weekly_challenges.get_latest()
        if not challenge:
            result += "No current challenge"
        elif len(users) == 0:
            result += "No registered users"
        else:
            date = datetime.fromtimestamp(challenge["date"])
            result += f"**Challenge {challenge['id']} | {date.strftime('%Y-%m-%d')}**\n\n"
            questions = self.database.weekly_questions.load_by_challenge_id(challenge["id"])
            user_scores = { user["leetcode_id"] : 0 for user in users }

            if len(questions) == 0:
                result += "Current challenge is empty"
            else:
                total_completions = 0
                for question in questions:
                    completions = 0
                    for user in users:
                        completed = self.leetcode.check_challenge_completion(
                                    user["leetcode_id"],
                                    question["title_slug"])
                        if completed:
                            user_scores[user["leetcode_id"]] += question["difficulty"]
                            completions += 1
                    total_completions += completions
                    result += f"{question['title']}\n" \
                        f"\t*{completions}/{len(users)} users completed*\n\n"
                group_percentage = int(
                    ((total_completions / (len(users) * len(questions)))) * 100
                )
                result += f"**Group completion:** {group_percentage}%"
        if challenge:
            result += "\n\n"
            for user in users:
                stars = Emojis.star * user_scores[user["leetcode_id"]]
                # NOTICE: In the future all database methods should return a well-defined
                #         object. That avoids having to do things like the following and
                #         allows for direct access via dot-operator
                LEETCODE_STR = "leetcode_id"
                result += f"\t{user[LEETCODE_STR]}: {stars}\n"
        return result

    def run(self) -> None:
        """
        Awaits for commands and processes them as received
        """
        pass
