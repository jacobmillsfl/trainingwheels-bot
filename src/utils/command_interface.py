"""
    Command Inteface module
"""

class CommandInterface:
    """
        An interface for classes that will support leetcode bot commands
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

    def command_status(self, leetcode_user_id) -> str:
        """
            Determines the completion status of each question in the current 
            weekly challenge for the given leetcode_user_id. Calls the 
            `submissions` leetcode API to determine which of the weekly
            challenge problems the given user has solved. Gathers the list 
            of current weekly challenges from the database.
        """
        pass
