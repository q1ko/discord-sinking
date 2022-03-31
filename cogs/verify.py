from datetime import datetime
from discord.ext import commands
from discord import slash_command, message_command, ApplicationContext, Option
import discord

gid = ["959045964054806570", "959058837564960819"]
vchnl = {}
vrole = {}


class Verify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @message_command(name="Set as verify channel", guild_ids=gid)
    async def _verify_assign(self, ctx: ApplicationContext, msg: discord.Message):
        # check for role
        try:
            channel = ctx.channel
            vchnl[ctx.guild_id] = channel
            await ctx.respond(
                f"{channel.mention} is now the verify channel.", delete_after=8
            )
        except ValueError:
            await ctx.respond("Invalid channel.", delete_after=8)

    @message_command(name="View verify channel", guild_ids=gid)
    async def _verify_show(self, ctx: ApplicationContext, msg: discord.Message):
        # check for role
        try:
            await ctx.respond(
                f"{vchnl[ctx.guild_id].mention} is the verify channel.", delete_after=8
            )
        except KeyError:
            await ctx.respond(
                "Verify channel has not been assigned yet.", delete_after=8
            )

    @slash_command(description="Verify your birthday.", guild_ids=gid)
    async def verify(
        self,
        ctx: ApplicationContext,
        month: Option(int, min_value=1, max_value=12),
        day: Option(int, min_value=1, max_value=31),
        year: Option(int, "Type the year as four digits. 2004 instead of 04."),
    ):
        current = datetime.now().date()
        try:
            if ctx.channel != vchnl[ctx.guild_id]:
                return await ctx.respond(
                    "Wrong channel to use /verify!", delete_after=5
                )
        except KeyError:
            return await ctx.respond(
                "Verify channel has not been assigned yet.", delete_after=5
            )

        user = datetime(year, month, day).date()
        age = int((current - user).days / 365)

        if age < 16 or age > 40:
            # consequent action
            return await ctx.respond("Inappropriate age.", delete_after=5)

        await ctx.respond("Valid.", delete_after=5)
        # verified action
