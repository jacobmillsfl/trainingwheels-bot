"""
    Discord Utility module
"""
from discord import Intents, Message, channel
from discord.ext import commands
from .command_interface import CommandInterface

intents = Intents.default()
intents.message_content = True


class DiscordUtil(commands.Bot, CommandInterface):
    """
    A class for performing all logic to interact with Discord as a bot
    """

    def __init__(self, discord_auth_token, channel_id):
        commands.Bot.__init__(self, command_prefix="!", self_bot=False, intents=intents)
        self.token = discord_auth_token
        self.channel_id = channel_id
        self.add_commands()

    def add_commands(self):
        @self.command(name="claim", pass_context=True)
        async def command_claim(ctx):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            return_message = ""
            discord_id = ctx.author.id
            parsed_command = self.validate_command(ctx.message.content, "!claim")
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                leetcode_id = parsed_command.args[0]
                self.command_claim(leetcode_id)

            await ctx.channel.send(f"{discord_id}: {ctx.message.content}")

        # async def on_ready(self):
        # """
        # Send a notification when the bot is connected and ready to recieve events
        # """
        # print(f"Logged in as {client.user}")

    # @client.event
    # async def on_message(self, message: Message):
    #     """
    #     Handle incoming events
    #     """
    #     if message.author == client.user or message.channel.id != 1072303681501941791:
    #         return
    #     channel = message.channel
    #     command = self.parse_command(message.content)
    #     if len(command.errors) > 0:
    #         error_message = "\n".join(command.errors)
    #         await channel.send(error_message)
    #     else:
    #         result_message = command.show_result()
    #         await channel.send(result_message)

    def run(self):
        super(commands.Bot, self).run(self.token)
