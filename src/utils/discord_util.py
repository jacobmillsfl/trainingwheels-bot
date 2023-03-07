"""
    Discord Utility module
"""
from discord import Intents
from discord.ext import commands
from .commands.command_abc import CommandAbstract
from .commands.command_util import CommandUtil
from .commands.command_parser import CommandParser

intents = Intents.default()
intents.message_content = True


class DiscordUtil(commands.Bot, CommandAbstract):
    """
    A class for performing all logic to interact with Discord as a bot
    """

    def __init__(self, **kwargs):
        """
        Initializes the Discord Utility
        """
        commands.Bot.__init__(self, command_prefix="!", self_bot=False, intents=intents)
        self.token = kwargs["token"]
        self.channel_id = kwargs["channel_id"]
        database = kwargs["database"]
        leetcode = kwargs["leetcode"]

        self.command_util = CommandUtil(database, leetcode, discord_mode=True)
        self.parser = CommandParser(debug_commands=[])
        self.add_commands()

    def _claim(self, **kwargs):
        """
        Associates a leetcode_id with a discord_id in the Leetcode_User table.

        Keyword Args:
        - discord_id        Discord ID doing the claiming
        - leetcode_id       Leetcode ID being claimed
        """
        return self.command_util.claim(kwargs["discord_id"], kwargs["leetcode_id"])

    def _challenge(self):
        """
        Determines the current weekly challenge.
        """
        return self.command_util.challenge()

    def _rank(self, **kwargs):
        """
        Determines a summary of leet stats for the current user.
        """
        return self.command_util.rank(kwargs["discord_id"])

    def _status(self, **kwargs):
        """
        Determines the weekly challenge completion status for a user
        """
        return self.command_util.status(kwargs["discord_id"])

    def _new_challenge(self):
        """
        Generates a new Weekly Challenge
        """
        return self.command_util.new_challenge()

    def _user(self, **kwargs):
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

    # Dynamically register Discord async commands
    def add_commands(self):
        """
        Registers commands with the bot
        """

        @self.command(name="claim", pass_context=True)
        async def claim(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            return_message = ""
            discord_id = str(ctx.author.id)
            parsed_command = self.parser.parse(ctx.message.content, discord_id)
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                leetcode_id = parsed_command.args[0]
                kwargs = {
                    "discord_id": discord_id,
                    "leetcode_id": leetcode_id
                }
                result = self._claim(**kwargs)
                return_message = result

            await ctx.channel.send(return_message)

        @self.command(name="challenge", pass_context=True)
        async def challenge(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            return_message = ""
            discord_id = str(ctx.author.id)
            parsed_command = self.parser.parse(ctx.message.content, discord_id)
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                result = self._challenge()
                return_message = result

            await ctx.channel.send(return_message)

        @self.command(name="rank", pass_context=True)
        async def rank(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            discord_id = str(ctx.author.id)
            return_message = ""
            parsed_command = self.parser.parse(ctx.message.content, discord_id)
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                kwargs = {"discord_id": discord_id}
                result = self._rank(**kwargs)
                return_message = f"```\n{result}\n```"

            await ctx.channel.send(return_message)

        @self.command(name="status", pass_context=True)
        async def status(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            discord_id = str(ctx.author.id)
            return_message = ""
            parsed_command = self.parser.parse(ctx.message.content, discord_id)
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                kwargs = {"discord_id": discord_id}
                result = self._status(**kwargs)
                return_message = result

            await ctx.channel.send(return_message)

        @self.command(name="new-challenge", parse_context=True)
        async def new_challenge(ctx: commands.Context):
            return_message = ""
            discord_id = str(ctx.author.id)
            parsed_command = self.parser.parse(ctx.message.content, discord_id)
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                result = self._new_challenge()
                return_message = result

            await ctx.channel.send(return_message)

        @self.command(name="user", pass_context=True)
        async def user(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            return_message = ""
            discord_id = str(ctx.author.id)
            parsed_command = self.parser.parse(ctx.message.content, discord_id)
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                kwargs = {"discord_id": discord_id}
                result = self._user(**kwargs)
                return_message = result

            await ctx.channel.send(return_message)

        @self.command("group-status", pass_context=True)
        async def group_status(ctx: commands.Context):
            message = await ctx.channel.send("Checking group status...")
            return_message = ""
            discord_id = str(ctx.author.id)
            parsed_command = self.parser.parse(ctx.message.content, discord_id)
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                result = self._group_status()
                return_message = result

            await message.edit(content=return_message)

    def run(self):
        commands.Bot.run(self, self.token)
