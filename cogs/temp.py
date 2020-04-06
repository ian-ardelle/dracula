from discord.ext import commands
import config


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def chancount(self,ctx):
        chanlist = self.bot.get_guild(config.GUILD_ID).channels
        await ctx.send(f"The number of channels in the server is: {str(chanlist)}")


def setup(bot):
    bot.add_cog(Misc(bot))
