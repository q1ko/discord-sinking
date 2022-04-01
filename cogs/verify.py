from datetime import datetime
from discord.ext import commands
from discord import (
    Forbidden,
    slash_command,
    message_command,
    ApplicationContext,
    Option,
)
import discord

gid = ["959045964054806570", "959058837564960819", "859217307321499678"]
vchnl = {}
vrole = {}
banmsg = {
    859217307321499678: "You are banned due to your inability to reach the age requirement of the server.\nAppeal here: https://discord.gg/bje2bxYw"
}


class Verify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @message_command(name="Set as verify channel")  # bot requires: manage channels
    async def _verify_assign(self, ctx: ApplicationContext, msg: discord.Message):
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.respond(
                "Not enough permission. (Manage Channels required)", delete_after=8
            )

        try:
            channel = ctx.channel
            vchnl[ctx.guild_id] = channel
            await ctx.respond(
                f"{channel.mention} is now the verify channel.", delete_after=8
            )
        except ValueError:
            await ctx.respond("Invalid channel.", delete_after=8)

    @message_command(name="View verify assignments")  # bot requires: manage channels
    async def _verify_show(self, ctx: ApplicationContext, msg: discord.Message):
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.respond(
                "Not enough permission. (Manage Channels required)", delete_after=8
            )

        try:
            vcout = f"{vchnl[ctx.guild_id].mention} is the verify channel."
        except KeyError:
            vcout = "Verify channel has not been assigned yet."

        try:
            vrout = f"{vrole[ctx.guild_id].mention} is the verifed role."
        except KeyError:
            vrout = "Verifed role has not been assigned yet."

        try:
            bmout = f"Ban message: {banmsg[ctx.guild_id]}"
        except KeyError:
            bmout = "Ban message has not been assigned yet."

        await ctx.respond(f"{vcout}\n{vrout}\n{bmout}", delete_after=8)

    @message_command(name="Set ban message")  # bot requires: manage channels
    async def _verify_ban_msg(self, ctx: ApplicationContext, msg: discord.Message):
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.respond(
                "Not enough permission. (Manage Channels required)", delete_after=8
            )

        banmsg[ctx.guild_id] = msg.content
        await ctx.respond(f"Ban message is now set to: {banmsg[ctx.guild_id]}")

    @slash_command(
        description="Verify your birthday."
    )  # bot requires: manage roles, ban members
    async def verify(
        self,
        ctx: ApplicationContext,
        month: Option(int, min_value=1, max_value=12),
        day: Option(int, min_value=1, max_value=31),
        year: Option(int, "Type the year as four digits. 2004 instead of 04."),
    ):
        try:
            if ctx.channel != vchnl[ctx.guild_id]:
                return await ctx.respond(
                    "Wrong channel to use /verify!", delete_after=5
                )
        except KeyError:
            return await ctx.respond(
                "Verify channel has not been assigned yet.", delete_after=5
            )

        try:
            if ctx.author.get_role(vrole[ctx.guild_id].id):
                return await ctx.respond("Already verified!", delete_after=8)
        except KeyError:
            await ctx.respond("Verified role has not been assigned yet.")

        current = datetime.now().date()
        user = datetime(year, month, day).date()
        age = int((current - user).days / 365)

        try:
            msg = banmsg[ctx.guild_id]
        except KeyError:
            msg = "You have not reached the age requirement for this server!"
            await ctx.respond(f"A custom ban message has not been set. Using: {msg}")

        if age < 16 or age > 35:
            try:
                await ctx.respond("Inappropriate age.", delete_after=5)
                await ctx.author.send(msg)
                return await ctx.author.ban(msg)
            except Forbidden:
                return await ctx.respond(
                    "Bot does not have Ban Members permission or bot is below bannable role.",
                    delete_after=8,
                )
        try:
            await ctx.author.add_roles(vrole[ctx.guild_id])
            await ctx.respond("Verified.", delete_after=5)
        except KeyError:
            return await ctx.respond(
                "Verified role has not been assigned yet.", delete_after=8
            )
        except Forbidden:
            return await ctx.respond(
                "Bot does not have Manage Roles permission.", delete_after=8
            )

    @slash_command(
        description="Set role given when verified."
    )  # bot requires: manage roles
    async def setverifyrole(
        self,
        ctx: ApplicationContext,
        role: Option(discord.Role, "Role given when verified."),
    ):
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.respond(
                "Not enough permission. (Manage Roles required)", delete_after=8
            )

        vrole[ctx.guild_id] = role
        await ctx.respond(f"{role.mention} is now the verified role.", delete_after=8)
    