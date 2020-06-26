from discord.ext import tasks, commands
from lib import time
import lib.dbman as db
from datetime import datetime, timedelta
import pytz

utc = pytz.utc


class Time(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.daily_commands.start()

    @commands.command()
    async def time(self, ctx):
        """
        Returns a timestamp of the current IC time.
        """
        await ctx.send(time.ic_date(ctx.guild.id) + " @ " + time.ic_time(ctx.guild.id))

    @tasks.loop(seconds=15)
    async def daily_commands(self):
        for guild_id in db.get_guild_list():
            guild_id = guild_id[0]
            cur_date = time.ic_date(guild_id)
            guild = db.get_guild_info(guild_id)
            last_date = guild.get("last_date")
            g_id = guild.get("id")
            if cur_date != last_date:
                channel = self.bot.get_channel(guild.get("date_chan"))
                await channel.send("The date is now: " + cur_date + ". Your hunger grows.")
                player_list = db.get_all_players(g_id)
                for player in player_list:
                    current_bp = player.get("bp") - 1
                    if current_bp >= 0:
                        db.execute("UPDATE Characters SET bp = %s WHERE id = %s", (current_bp, player.get("id")))
                    current_wp = player.get("wp")
                    current_wp_max = player.get("wp_max")
                    if current_wp < current_wp_max:
                        current_wp += 1
                        db.execute("UPDATE BnW SET wp = %s WHERE player_id = %s", (current_wp, player.get("id")))
                    if player.get("upkeep_date") != '':
                        old_upkeep = player.get("upkeep_date")
                    else:
                        old_upkeep = ''
                    if not old_upkeep:
                        ctime = time.ic_datetime_utc(guild_id)
                        old_upkeep = ctime
                    if old_upkeep < ctime and player.get("upkeep") > 0 and player.get("bp") > 0:
                        new_bp = player.get("bp") - 1
                        upkeep_datetime = old_upkeep + timedelta(
                            days=db.get_guild_info(guild_id).get("time_coefficient") / player.get("upkeep"))
                        db.execute("UPDATE Characters SET upkeep_date = %s, bp = %s WHERE id = %s",
                                   (upkeep_datetime.strftime("%Y:%m:%d:%H:%M:%S"), new_bp, player.get("id")))
                    if player.get("bp") == 0 and player.get("alert_flag") == 0:
                        db.execute("UPDATE Characters SET alert_flag = 1 WHERE id = %s", player.get("id"))
                        try:
                            guild_name = self.bot.get_guild(guild_id).name
                            await self.bot.get_guild(guild_id).get_member(player.get("player_id")).send(
                                f"Your character is at 0 BP due to infrequent feeding or inactivity. If your \
                                character remains on this list too long you risk being removed from {guild_name}. \
                                When you log in please fill free to roll as many time as are necessary to fill \
                                your character's blood pool. You may then jump into play without accounting as the \
                                feeding occurred while you were offline.")
                        except KeyError:
                            continue
                    if player.get("alert_flag") == 1 and player.get("bp") > 0:
                        db.execute("UPDATE Characters SET alert_flag = 0 WHERE id = %s", player.get("id"))

    @daily_commands.before_loop
    async def before_alert(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Time(bot))
