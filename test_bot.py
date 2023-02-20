from discord import Intents
from discord.ext import commands


class MyBot(commands.Bot):
    def __init__(self, command_prefix, self_bot):
        intents = Intents.default()
        intents.message_content = True

        commands.Bot.__init__(
            self, command_prefix=command_prefix, self_bot=self_bot, intents=intents
        )
        self.READY_MESSAGE = "[INFO]: Bot now online"
        self.STATUS_MESSAGE = "Bot still online"

    async def on_ready(self):
        print(self.READY_MESSAGE)

    def add_commands(self):
        # @self.event
        # async def on_message(
        #     message,
        # ):
        #     if message.author != self.user:
        #         await message.channel.send("GOT THE MESSAGE")

        @self.command(name="status", pass_context=True)
        async def status(ctx):
            print(ctx)
            await ctx.channel.send(ctx.author.id)

    def setup(self):
        self.add_commands()


bot = MyBot(command_prefix="!", self_bot=False)
bot.setup()
bot.run("MTA3NzA1MjkzNjI0NjUzNDI2NQ.GPhL1i.iGKQdB2F1s-guXpl2NChqpI7OGp0FwZc13AUdg")
