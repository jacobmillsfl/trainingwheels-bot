"""
    Discord Utility module
"""
from discord import Intents
from discord.ext import commands
from .command_interface import CommandInterface

intents = Intents.default()
intents.message_content = True


class DiscordUtil(commands.Bot, CommandInterface):
    """
    A class for performing all logic to interact with Discord as a bot
    """

    def __init__(self, **kwargs):
        commands.Bot.__init__(self, command_prefix="!", self_bot=False, intents=intents)
        self.token = kwargs["token"]
        self.channel_id = kwargs["channel_id"]

        database = kwargs["database"]
        CommandInterface.__init__(self, database, discord_mode=True)

        self.add_commands()

    def add_commands(self):
        """
        Registers commands with the bot
        """

        @self.command(name="claim", pass_context=True)
        async def command_claim(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            return_message = ""
            discord_id = str(ctx.author.id)
            parsed_command = self.validate_command(ctx.message.content, "!claim")
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                leetcode_id = parsed_command.args[0]
                result = self.command_claim(discord_id, leetcode_id)
                return_message = result

            await ctx.channel.send(return_message)

        @self.command(name="user", pass_context=True)
        async def command_user(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            return_message = ""
            discord_id = str(ctx.author.id)
            parsed_command = self.validate_command(ctx.message.content, "!user")
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                result = self.command_user(discord_id)
                return_message = result

            await ctx.channel.send(return_message)

        @self.command(name="challenge", pass_context=True)
        async def command_challenge(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            return_message = ""
            parsed_command = self.validate_command(ctx.message.content, "!challenge")
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                result = self.command_challenge()
                return_message = result

            await ctx.channel.send(return_message)

        @self.command(name="rank", pass_context=True)
        async def command_rank(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            discord_id = str(ctx.author.id)
            return_message = ""
            parsed_command = self.validate_command(ctx.message.content, "!rank")
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                result = self.command_rank(discord_id)
                return_message = result

            await ctx.channel.send(return_message)

        @self.command(name="status", pass_context=True)
        async def command_status(ctx: commands.Context):
            if str(ctx.channel.id) != str(self.channel_id):
                return
            discord_id = str(ctx.author.id)
            return_message = ""
            parsed_command = self.validate_command(ctx.message.content, "!status")
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                result = self.command_status(discord_id)
                return_message = result

            await ctx.channel.send(return_message)

        @self.command(name="new-challenge", parse_context=True)
        async def command_new_challenge(ctx: commands.Context):
            return_message = ""
            parsed_command = self.validate_command(
                ctx.message.content, "!new-challenge"
            )
            if len(parsed_command.errors) > 0:
                return_message = "\n".join(parsed_command.errors)
            else:
                result = self.command_new_challenge()
                return_message = result

            await ctx.channel.send(return_message)

    def run(self):
        super(commands.Bot, self).run(self.token)
