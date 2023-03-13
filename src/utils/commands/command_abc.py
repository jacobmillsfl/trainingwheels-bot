"""
Command Abstract Base Class module
"""
from abc import ABC, abstractmethod

class CommandAbstract(ABC):
    """
    Abstract Base Class for Bot Commands
    """

    @abstractmethod
    def _claim(self, **kwargs) -> str:
        """
        Associates a leetcode_id with a discord_id in the Leetcode_User table.
        Local only, no API required.
        Database required.

        Keyword Args:
        - leetcode_id       Leetcode ID being claimed
        """
        pass

    @abstractmethod
    def _challenge(self) -> str:
        """
        Determines the current weekly challenge.
        Local only, no API required.
        Database required.
        """
        pass

    @abstractmethod
    def _rank(self, **kwargs) -> str:
        """
        Determines a summary of leet stats for the current user.
        Calls the `rank`/`stats` leetcode API and returns results.
        No database required.

        Keyword Args:
         - discord_id       The discord user ID
        """
        pass

    @abstractmethod
    def _status(self, **kwargs) -> str:
        """
        Determines the completion status of each question in the current
        weekly challenge. Calls the `submissions` leetcode API to 
        determine which of the weekly challenge problems the given user 
        has solved. Gathers the list of current weekly challenges from 
        the database.

        Keyword Args:
         - discord_id       The discord user ID
        """
        pass

    @abstractmethod
    def _new_challenge(self) -> str:
        """
        Generates a new Weekly Challenge
        """
        pass

    @abstractmethod
    def _user(self, **kwargs) -> str:
        """
        Gets the leetcode_id of the requested user

        Keyword Args:
         - discord_id       The discord user ID
        """
        pass

    @abstractmethod
    def _group_status(self) -> str:
        """
        Calculates and summarizes the number of users who have completed each question
        in the current challenge
        """
        pass
