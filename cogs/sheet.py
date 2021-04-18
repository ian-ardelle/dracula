from discord.ext import commands
import lib.dbman as db
import discord
import lib.utility as utility


def set_attribute(guild, member: discord.Member, name, value):
    setatt = True


class Sheet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_str(self, ctx, member: discord.Member, value):
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st(guild, ctx.author.roles):
            set_attribute(self, guild, member, "strength", value)

    @commands.command()
    async def set_dex(self, ctx, member: discord.Member, value):
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st(guild, ctx.author.roles):
            set_attribute(self, guild, member, "dexterity", value)

    @commands.command()
    async def set_sta(self, ctx, member: discord.Member, value):
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st(guild, ctx.author.roles):
            set_attribute(self, guild, member, "stamina", value)
