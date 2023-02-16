"""
Standalone Utility module
"""

from .command_interface import CommandInterface

class StandaloneUtil(CommandInterface):
    """
    A class for providing features similar to a Discord bot without
    actually connecting to Discord
    """

    def __init__(self):
        # Add Standalone only commands
        self.VALID_COMMANDS.append("!quit")
        self.USAGE_MESSAGE += "!quit                   -   Exits the application"

    def run(self):
        """
        Presents user with a REPL where they can continually enter commands
        to be processed by the app
        """
        while True:
            command = input("Enter a bot command : ")
            parsed_command = self.parse_command(command)
            if not parsed_command.errors:
                print(f"Running command: {parsed_command.action}")

                if parsed_command.action == "!quit":
                    # Exit run() routine
                    break
                if parsed_command.action == "!help":
                    print(self.USAGE_MESSAGE)
                # Add support for additional commands

            else:
                print("\n".join(parsed_command.errors))
                print("Enter `!help` for usage")
