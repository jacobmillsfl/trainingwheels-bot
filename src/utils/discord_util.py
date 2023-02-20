"""
    Discord Utility module
"""
from discord import Intents, Client, Message
from .command_interface import CommandInterface

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)


class DiscordUtil(CommandInterface):
    """
    A class for performing all logic to interact with Discord as a bot
    """

    def __init__(self, **kwargs):
        if "database" not in kwargs or "token" not in kwargs:
            raise ValueError("Token and database required to construct a DiscordUtil object")
        self.token = kwargs["token"]
        super().__init__(kwargs["database"])

    @client.event
    async def on_ready(self):
        """
        Send a notification when the bot is connected and ready to recieve events
        """
        print(f"Logged in as {client.user}")

    @client.event
    async def on_message(self, message: Message):
        """
        Handle incoming events
        """
        if message.author == client.user or message.channel.id != 1072303681501941791:
            return
        channel = message.channel
        command = self.parse_command(message.content)
        if len(command.errors) > 0:
            error_message = "\n".join(command.errors)
            await channel.send(error_message)
        else:
            result_message = command.get_result()
            await channel.send(result_message)

    def run(self):
        client.run(self.token)
