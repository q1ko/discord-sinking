from decouple import config
import discord

intents = discord.Intents.default()
intents.guilds = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} ready")

bot.load_extension("cogs.verify")

bot.run(config("TOKEN"))
