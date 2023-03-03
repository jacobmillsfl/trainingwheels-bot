"""
Bot Command module
"""
from typing import List

class BotCommand:
    """
    A class for storing the data that make up a bot command
    """

    VALID_COMMANDS = [
        "!user",
        "!help",
        "!claim",
        "!challenge",
        "!rank",
        "!status",
        "!new-challenge",
        "!group-status",
    ]

    def __init__(self, issuer: str, action: str, kwargs: dict, errors: List[str]):
        self.issuer = issuer
        self.action = action
        self.kwargs = kwargs
        self.errors = errors
