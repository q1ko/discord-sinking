from discord.ext import commands
from decouple import config
import cogs
import discord


prefix = ""
intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} ready")


def get_modules():
    yield cogs.Verify(bot)


for i in get_modules():
    bot.add_cog(i)
    print(i.__class__.__name__, "initialised.")

bot.run(config("TOKEN"))
