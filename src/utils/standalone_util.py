"""
Standalone Utility module
"""

from .commands.command_abc import CommandAbstract
from .commands.command_util import CommandUtil
from .commands.command_parser import CommandParser
from .commands.bot_command import BotCommand

class StandaloneUtil(CommandAbstract):
    """
    A class for providing features similar to a Discord bot without
    actually connecting to Discord
    """

    DEBUG_COMMANDS = {
        "!quit": "!quit                   -   Exits the application\n",
        "!debug": "!debug                  -   Runs a debug routine\n",
    }

    def __init__(self, **kwargs):
        if "database" not in kwargs:
            raise ValueError("Database required to construct a StandaloneUtil object")
        self.command_util = CommandUtil(kwargs["database"], kwargs["leetcode"])
        self.parser = CommandParser(debug_commands=self.DEBUG_COMMANDS.keys())
        # Add Standalone only data
        for command, description in self.DEBUG_COMMANDS.items():
            BotCommand.VALID_COMMANDS.append(command)
            CommandUtil.USAGE_MESSAGE += description
        self.DISCORD_ID = "1"

    def run(self):
        """
        Presents user with a REPL where they can continually enter commands
        to be processed by the app
        """
        while True:
            command = input("Enter a bot command : ")
            parsed_command = self.parser.parse(command, self.DISCORD_ID)
            if not parsed_command.errors:
                # Standalone only commands
                if parsed_command.action == "quit":
                    break
                if parsed_command.action == "help":
                    print(self.command_util.USAGE_MESSAGE)
                    continue

                # Dispatch bot commands
                cmd = getattr(self, f"_{parsed_command.action}")
                if parsed_command.kwargs:
                    result = cmd(**parsed_command.kwargs)
                else:
                    result = cmd()
                print(result)
            else:
                print("\n".join(parsed_command.errors))
                print("Enter `!help` for usage")

    def _claim(self, **kwargs) -> str:
        """
        Associates a leetcode_id with a discord_id in the Leetcode_User table.

        Keyword args:
        - leetcode_id       The Leetcode ID being claimed
        """
        return self.command_util.claim(kwargs["discord_id"], kwargs["leetcode_id"])

    def _challenge(self) -> str:
        """
        Determines the current weekly challenge.
        """
        return self.command_util.challenge()

    def _rank(self, **kwargs) -> str:
        """
        Determines a summary of leet stats for the current user.
        """
        return self.command_util.rank(kwargs["discord_id"])

    def _status(self, **kwargs) -> str:
        """
        Determines the completion status of each question in the current
        weekly challenge
        """
        return self.command_util.status(kwargs["discord_id"])

    def _new_challenge(self) -> str:
        """
        Generates a new Weekly Challenge
        """
        return self.command_util.new_challenge()

    def _user(self, **kwargs) -> str:
        """
        Gets the leetcode_id of the requested user
        """
        return self.command_util.user(kwargs["discord_id"])

    def _group_status(self) -> str:
        """
        Calculates and summarizes the number of users who have completed each question
        in the current challenge
        """
        return self.command_util.group_status()

    def _debug(self) -> str:
        """
        Runs a debug routine
        """
        return "DEBUG"
