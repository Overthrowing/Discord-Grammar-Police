import os
import discord
from discord.ext import commands
import language_tool_python
from dotenv import load_dotenv

load_dotenv()
tool = language_tool_python.LanguageTool('en-US')


class GrammarPolice(commands.Bot):
    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        message_content = message.content
        user_id = message.author.id

        errors = tool.check(message_content)
        if len(errors) > 0:
            corrected = tool.correct(message_content)
            await message.channel.send("*" + corrected + f" <@!{user_id}>")

        await self.process_commands(message)


bot = GrammarPolice(
    command_prefix=commands.when_mentioned_or(','),
    help_command=None,
    intents=discord.Intents.all()
)

bot.run(os.getenv("DISCORD_TOKEN"))
