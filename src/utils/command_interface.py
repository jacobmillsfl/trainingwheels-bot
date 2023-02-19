"""
Command Inteface module
"""


class BotCommand:
    """
    A class for storing the data that make up a bot command
    """

    def __init__(self, action, args, errors):
        self.action = action
        self.args = args
        self.errors = errors
        self.result = ""

    def show_result(self):
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

    VALID_COMMANDS = ["!help", "!claim", "!challenge", "!rank", "!status", "!quit"]
    USAGE_MESSAGE = """
Supported commands:

!help                   -   Display help information
!claim <leetcode_id>    -   Associate <leetcode_id> with the user's discord_id
!challenge              -   Display the latest weekly challenge
!rank                   -   Display user's all time Leetcode status
!status                 -   Display user's completion status of current weekly challenge
"""

    def command_claim(self, leetcode_id: str) -> str:
        """
        Associates a leetcode_id with a discord_id in the Leetcode_User table.
        Local only, no API required.
        Database required.
        """
        pass

    def command_challenge(self) -> str:
        """
        Determines the current weekly challenge.
        Local only, no API required.
        Database required.
        """
        pass

    def command_rank(self, leetcode_user_id: str) -> str:
        """
        Determines a summary of leet stats for the current user.
        Calls the `rank`/`stats` leetcode API and returns results.
        No database required.
        """
        pass

    def command_status(self, leetcode_user_id: str) -> str:
        """
        Determines the completion status of each question in the current
        weekly challenge for the given leetcode_user_id. Calls the
        `submissions` leetcode API to determine which of the weekly
        challenge problems the given user has solved. Gathers the list
        of current weekly challenges from the database.
        """
        pass

    def run(self) -> None:
        """
        Awaits for commands and processes them as received
        """
        pass

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

        return BotCommand(action, args, errors)
