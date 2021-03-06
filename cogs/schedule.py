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
            cur_date_dt = time.ic_date_dt(guild_id)
            guild = db.get_guild_info(guild_id)
            last_date = guild.get("last_date")
            player_list = db.get_all_players(guild_id)
            for player in player_list:
                if not self.bot.get_user(player.get("player_id")):
                    db.execute(
                        "DELETE FROM Characters WHERE id = %s", (player.get("id"),)
                    )
                else:
                    if player.get("bp") == 0 and player.get("alert_flag") == 0:
                        db.execute(
                            "UPDATE Characters SET alert_flag = 1 WHERE id = %s",
                            (player.get("id"),),
                        )
                        try:
                            guild_name = self.bot.get_guild(guild_id).name
                            await self.bot.get_user(player.get("player_id")).send(
                                f"Your character is at 0 BP due to "
                                f"infrequent feeding or inactivity. "
                                f"If your character remains on this "
                                f"list too long you risk being "
                                f"removed from {guild_name}. When "
                                f"you log in please fill free to "
                                f"roll as many time as are "
                                f"necessary to fill your "
                                f"character's blood pool. You may "
                                f"then jump into play without "
                                f"accounting as the feeding "
                                f"occurred while you were offline."
                            )
                        except KeyError:
                            continue
                    if player.get("alert_flag") == 1 and player.get("bp") > 0:
                        db.execute(
                            "UPDATE Characters SET alert_flag = 0 WHERE id = %s",
                            (player.get("id"),),
                        )

                    if player.get("upkeep") > 0:
                        time.ic_datetime_utc(guild_id)
                        ctime = time.ic_datetime_utc(guild_id)
                        if player.get("upkeep_date") != " ":
                            old_upkeep = utc.localize(player.get("upkeep_date"))
                        else:
                            old_upkeep = time.ic_datetime_utc(guild_id)
                            db.execute(
                                "UPDATE Characters SET upkeep_dt = %s WHERE id = %s",
                                (
                                    old_upkeep.strftime("%Y:%m:%d:%H:%M:%S"),
                                    player.get("id"),
                                ),
                            )
                        if old_upkeep < ctime:
                            new_bp = player.get("bp") - 1
                            upkeep_datetime = old_upkeep + timedelta(
                                days=30.4375 / player.get("upkeep")
                            )
                            db.execute(
                                "UPDATE Characters SET upkeep_dt = %s, bp = %s WHERE id = %s",
                                (
                                    upkeep_datetime.strftime("%Y:%m:%d:%H:%M:%S"),
                                    new_bp,
                                    player.get("id"),
                                ),
                            )

            if cur_date_dt != last_date:
                cur_date = time.ic_date(guild_id)
                channel = self.bot.get_guild(guild_id).get_channel(
                    guild.get("date_chan")
                )
                await channel.send(
                    "The date is now: " + cur_date + ". Your hunger grows."
                )
                db.execute(
                    "UPDATE Config SET last_date = %s WHERE guild_id = %s",
                    (cur_date_dt.strftime("%Y:%m:%d"), guild_id),
                )
                player_list = db.get_all_players(guild_id)
                for player in player_list:
                    current_bp = player.get("bp") - 1
                    if current_bp >= 0:
                        db.execute(
                            "UPDATE Characters SET bp = %s WHERE id = %s",
                            (current_bp, player.get("id")),
                        )
                    current_wp = player.get("wp")
                    current_wp_max = player.get("wp_max")
                    if current_wp < current_wp_max:
                        current_wp += 1
                        db.execute(
                            "UPDATE Characters SET wp = %s WHERE id = %s",
                            (current_wp, player.get("id")),
                        )

    @daily_commands.before_loop
    async def before_alert(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Time(bot))
