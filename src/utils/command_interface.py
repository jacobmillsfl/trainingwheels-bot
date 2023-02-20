"""
Command Interface module
"""
import random
from datetime import datetime
from .leetcode_util import LeetcodeUtil

QUESTION_DIFFICULTY_MAP = {1: "Easy", 2: "Medium", 3: "Hard"}


class BotCommand:
    """
    A class for storing the data that make up a bot command
    """

    def __init__(self, action, args, errors):
        self.action = action
        self.args = args
        self.errors = errors
        self.result = ""

    def get_result(self):
        """
        Shows the current results of a BotCommand instance
        """
        return self.result

    def add_error(self, error_message) -> None:
        """
        Adds an error string to the error message list
        """
        self.errors.append(error_message)


class CommandInterface:
    """
    An interface for classes that will support leetcode bot commands
    """

    VALID_COMMANDS = [
        "!user",
        "!help",
        "!claim",
        "!challenge",
        "!rank",
        "!status",
        "!new-challenge",
    ]
    USAGE_MESSAGE = """
Supported commands:

!help                   -   Display help information
!claim <leetcode_id>    -   Associate <leetcode_id> with the user's discord_id
!challenge              -   Display the latest weekly challenge
!rank                   -   Display user's all time Leetcode status
!status                 -   Display user's completion status of current weekly challenge
!new-challenge          -   Generate a new Weekly Challenge
"""

    def __init__(self, database):
        self.database = database

    def command_claim(self, discord_id: str, leetcode_id: str) -> str:
        """
        Associates a leetcode_id with a discord_id in the Leetcode_User table.
        Local only, no API required.
        Database required.
        """
        message = ""
        create_user = False
        claimed_user = self.database.table_leetcodeuser_load_by_leetcode_id(leetcode_id)
        existing_user = self.database.table_leetcodeuser_load_by_discord_id(discord_id)
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
            deleted = self.database.table_leetcodeuser_delete_by_discord_id(discord_id)
            if deleted:
                message += "Deletion success!\n"
                create_user = True
            else:
                message += "An error occurred during user deletion\n"
        else:
            create_user = True
        if create_user:
            user = {"discord_id": discord_id, "leetcode_id": leetcode_id}
            success = self.database.table_leetcodeuser_insert(user)
            if success:
                message += f"Leetcode Username `{leetcode_id}` successfully claimed!\n"
            else:
                message += f"Error: {leetcode_id} already in use!\n"
        return message

    def command_challenge(self) -> str:
        """
        Determines the current weekly challenge.
        Local only, no API required.
        Database required.
        """
        latest = self.database.table_weeklychallenge_getlatest()
        if latest:
            start_date = datetime.fromtimestamp(latest["date"])
            result = f"* * * CHALLENGE {latest['id']} | {start_date.date()} * * *\n\n"

            questions = self.database.table_weeklyquestion_load_by_challenge_id(
                latest["id"]
            )
            for q in questions:
                question = self.database.table_leetcodequestion_load(q["id"])
                result += f"Question:\t{question['title']}\n"
                result += (
                    f"Difficulty:\t{QUESTION_DIFFICULTY_MAP[question['difficulty']]}\n"
                )
                result += f"URL:\t\thttps://leetcode.com/problems/{question['title_slug']}/\n\n"
        else:
            result = "There are no challenges at this time"
        return result

    def command_rank(self, discord_id: str) -> str:
        """
        Determines a summary of leet stats for the current user.
        Calls the `rank`/`stats` leetcode API and returns results.
        No database required.
        """
        user = self.database.table_leetcodeuser_load_by_discord_id(discord_id)
        if user:
            leetcode_user_id = user["leetcode_id"]
            result = LeetcodeUtil.get_user_rank(leetcode_user_id)
        else:
            result = (
                "Leetcode user not found. Claim your user idea with"
                " `!claim <leetcode_username>`"
            )
        return result

    def command_status(self, discord_id: str) -> str:
        """
        Determines the completion status of each question in the current
        weekly challenge for the given leetcode_user_id. Calls the
        `submissions` leetcode API to determine which of the weekly
        challenge problems the given user has solved. Gathers the list
        of current weekly challenges from the database.
        """
        result = ""
        user = self.database.table_leetcodeuser_load_by_discord_id(discord_id)
        if user:
            leetcode_user_id = user["leetcode_id"]
            challenge = self.database.table_weeklychallenge_getlatest()
            if not challenge:
                result += "No current challenges"
            else:
                result += f"User {leetcode_user_id}'s Weekly Challenge status:\n"
                questions = self.database.table_weeklyquestion_load_by_challenge_id(
                    challenge["id"]
                )
                for question in questions:
                    complete = LeetcodeUtil.check_challenge_completion(
                        leetcode_user_id, question["title_slug"]
                    )
                    result += (
                        f"\t{'Complete' if complete else 'Incomplete'}"
                        f"\t-\t{question['title']}\n"
                    )
        else:
            result += "Leetcode user not found. Claim your user idea with"
            result += " `!claim <leetcode_username>`"
        return result

    def command_new_challenge(self) -> str:
        """
        Generates a new Weekly Challenge
        """
        questions = self.database.table_leetcodequestion_loadall()
        previous_questions = self.database.table_weeklyquestion_loadall()
        previous_question_slugs = [q["title_slug"] for q in previous_questions]
        valid_questions = list(
            filter(lambda q: q["title_slug"] not in previous_question_slugs, questions)
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

    def command_user(self, discord_id: str) -> str:
        """
        Gets the leetcode_id of the requested user
        """
        return_message = ""
        user = self.database.table_leetcodeuser_load_by_discord_id(discord_id)
        if not user:
            return_message = "User not found"
        else:
            return_message = user["leetcode_id"]
        return return_message

    def run(self) -> None:
        """
        Awaits for commands and processes them as received
        """
        pass

    def validate_command(self, command: str, expected_command: str):
        """
        Ensures that the action matches the intended command
        """
        parsed_command = self.parse_command(command)
        if parsed_command.action and parsed_command.action != expected_command:
            parsed_command.errors.append(
                f"Unexpected command {parsed_command.action}, expected: {expected_command}"
            )
        return parsed_command

    def parse_command(self, command: str) -> BotCommand:
        """
        Parses and validates a given command
        """
        action = ""
        args = ""
        errors = []

        parts = command.split(" ")
        if len(parts) == 0:
            errors.append("Invalid command, no input given")
        elif parts[0] not in self.VALID_COMMANDS:
            errors.append(f"`{parts[0]}` is not a currently supported command.")
        else:
            action = parts[0]
            args = parts[1:]

        if action == "!claim" and len(args) == 0:
            errors.append("Invalid syntax for command `!claim`")

        return BotCommand(action, args, errors)
