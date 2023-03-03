"""
Command Parser module
"""
from typing import List
from .bot_command import BotCommand

class CommandParser:
    """
    Parses bot commands
    """
    def __init__(self, debug_commands: List[str]):
        self.debug_commands = debug_commands

    def validate_cmd_claim(self, issuer: str, action: str, args: str, errors: List[str]):
        """
        Validates the claim command
        """
        arg_split = args.split(" ")
        if len(arg_split) != 1:
            errors.append("Invalid argument count for command claim")
        else:
            kwargs = {
                "discord_id": issuer,
                "leetcode_id": arg_split[0]
            }

        return BotCommand(issuer, action, kwargs, errors)

    def validate_cmd_challenge(self, issuer: str, action: str, args: str, errors: List[str]):
        """
        Validates the challenge command
        """
        kwargs = {}
        if args:
            errors.append("Invalid argument count for command challenge")

        return BotCommand(issuer, action, kwargs, errors)

    def validate_cmd_rank(self, issuer: str, action: str, args: str, errors: List[str]):
        """
        Validates the rank command
        """
        kwargs = {
            "discord_id": issuer
        }
        if args:
            errors.append("Invalid argument count for command rank")

        return BotCommand(issuer, action, kwargs, errors)

    def validate_cmd_status(self, issuer: str, action: str, args: str, errors: List[str]):
        """
        Validates the status command
        """
        kwargs = {
            "discord_id": issuer
        }
        if args:
            errors.append("Invalid argument count for command status")

        return BotCommand(issuer, action, kwargs, errors)

    def validate_cmd_new_challenge(self, issuer: str, action: str, args: str, errors: List[str]):
        """
        Validates the new_challenge command
        """
        kwargs = {}
        if args:
            errors.append("Invalid argument count for command new_challenge")

        return BotCommand(issuer, action, kwargs, errors)

    def validate_cmd_user(self, issuer: str, action: str, args: str, errors: List[str]):
        """
        Validates the user command
        """
        kwargs = {
            "discord_id": issuer
        }
        if args:
            errors.append("Invalid argument count for command user")

        return BotCommand(issuer, action, kwargs, errors)

    def validate_cmd_group_status(self, issuer: str, action: str, args: str, errors: List[str]):
        """
        Validates the group_status command
        """
        kwargs = {}
        if args:
            errors.append("Invalid argument count for command group_status")

        return BotCommand(issuer, action, kwargs, errors)

    def parse(self, command: str, issuer: str) -> BotCommand:
        """
        Parses and validates a given command
        """
        action = ""
        args = ""
        errors = []

        parts = command.split(" ")
        if len(parts) == 0:
            errors.append("Invalid command, no input given")
        elif parts[0] not in BotCommand.VALID_COMMANDS:
            errors.append(
                f"`{parts[0]}` is not a currently supported command.")
        else:
            # Remove `!` character and replace `-` with `_`
            action = parts[0][1:].strip().replace("-","_")
            # Remove whitespace around arguments
            args = " ".join(parts[1:]).strip()

        if len(errors) > 0 \
            or parts[0] in self.debug_commands \
            or action == "help":
            return BotCommand(issuer, action, args, errors)

        validator_name = f"validate_cmd_{action}"
        validate = getattr(self, validator_name)
        return validate(issuer, action, args, errors)
