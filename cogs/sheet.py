from discord.ext import commands
import lib.dbman as db
import discord

class Sheet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_strength(self, ctx, member: discord.Member, value):
        authorized = False
        guild = db.get_guild_info(ctx.guild.id)
        for role in ctx.author.roles:
            if guild.get("st_id") == role.id or guild.get("narrator_id") == role.id:
                authorized = True