"""
Standalone Utility module
"""

from .command_interface import CommandInterface


class StandaloneUtil(CommandInterface):
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
        super().__init__(kwargs["database"])
        # Add Standalone only data
        for command, description in self.DEBUG_COMMANDS.items():
            self.VALID_COMMANDS.append(command)
            self.USAGE_MESSAGE += description
        self.DISCORD_ID = "1"

    def run(self):
        """
        Presents user with a REPL where they can continually enter commands
        to be processed by the app
        """
        while True:
            command = input("Enter a bot command : ")
            parsed_command = self.parse_command(command)
            if not parsed_command.errors:
                result = ""
                if parsed_command.action == "!quit":
                    break
                if parsed_command.action == "!help":
                    print(self.USAGE_MESSAGE)
                    continue
                if parsed_command.action == "!claim":
                    result = self.command_claim(self.DISCORD_ID, parsed_command.args[0])
                elif parsed_command.action == "!challenge":
                    result = self.command_challenge()
                elif parsed_command.action == "!rank":
                    result = self.command_rank(self.DISCORD_ID)
                elif parsed_command.action == "!status":
                    result = self.command_status(self.DISCORD_ID)
                elif parsed_command.action == "!new-challenge":
                    result = self.command_new_challenge()
                elif parsed_command.action == "!debug":
                    pass  # This is for debugging custom routines
                print(result)
            else:
                print("\n".join(parsed_command.errors))
                print("Enter `!help` for usage")
