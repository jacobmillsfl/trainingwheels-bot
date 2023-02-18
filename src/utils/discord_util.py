"""
    Discord Utility module
"""
from discord import Intents, Client
from .command_interface import CommandInterface

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)


class DiscordUtil(CommandInterface):
    """
    A class for performing all logic to interact with Discord as a bot
    """

    def __init__(self, discord_auth_token):
        self.token = discord_auth_token

        self.run()
        pass

    @client.event
    async def on_ready(self):
        """
        Send a notification when the bot is connected and ready to recieve events
        """
        print(f"Logged in as {client.user}")

    @client.event
    async def on_message(self, message):
        """
        Handle incoming events
        """
        if message.author == client.user:
            return
        channel = message.channel
        command = self.parse_command(message.content)
        if len(command.errors) > 0:
            error_message = ", ".join(command.errors)
            await channel.send(error_message)
        else:
            result_message = command.show_result()
            await channel.send(result_message)

    def run(self):
        client.run(self.token)
