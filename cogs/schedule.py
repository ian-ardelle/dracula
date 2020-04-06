from discord.ext import tasks, commands
from lib import time
import config
from lib.dbman import c, conn
from datetime import datetime, timedelta
import pytz

cur_date = time.ic_date()
cur_time = time.ic_time()
utc = pytz.utc


class Time(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.daily_commands.start()
        self.cycle_commands.start()
        self.empty_bp_alert.start()
        self.clear_empty_bp_alert.start()

    @commands.command()
    async def time(self, ctx):
        """
        Returns a timestamp of the current IC time.
        """
        await ctx.send(time.ic_date() + " @ " + time.ic_time())

    @tasks.loop(seconds=5)
    async def daily_commands(self):
        global cur_date
        if cur_date != time.ic_date():
            channel = self.bot.get_channel(config.DATE_CHANNEL)
            cur_date = time.ic_date()
            await channel.send("The date is now: " + cur_date + ". Your hunger grows.") #End of date stuff
            c.execute("SELECT player_id FROM BnW")
            pid_list = c.fetchall()
            for member in pid_list:
                lister = (member[0],)
                c.execute("SELECT bp FROM BnW WHERE player_id = ?", lister)
                current_bp = int(list(c.fetchone())[0]) - 1
                if current_bp >= 0:
                    listers = (current_bp, member[0],)
                    c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                    conn.commit()
                c.execute("SELECT wp, wp_max FROM BnW WHERE player_id = ?", lister)
                wp_data = list(c.fetchone())
                current_wp = int(wp_data[0])
                current_wp_max = int(wp_data[1])
                if current_wp < current_wp_max:
                    current_wp += 1
                    listers = (current_wp, member[0],)
                    c.execute("UPDATE BnW SET wp = ? WHERE player_id = ?", listers)
                    conn.commit()

    @tasks.loop(seconds=10)
    async def cycle_commands(self):
        c.execute("SELECT player_id, upkeep_date, upkeep, bp FROM BnW")
        upkeep_list = c.fetchall()
        ctime = time.ic_datetime_utc().replace(tzinfo=None)
        for member in upkeep_list:
            if member[1] != '0':
                old_upkeep = datetime(int(member[1][0:4]), int(member[1][5:7]), int(member[1][8:10]), int(member[1][11:13]), int(member[1][14:16]))
            else:
                old_upkeep = ''
            if not old_upkeep:
                old_upkeep = ctime
            if old_upkeep < ctime and member[2] > 0:
                if member[3] > 0:
                    new_bp = member[3] - 1
                    upkeep_datetime = old_upkeep + timedelta(days=30.42/member[2])
                    listers = (upkeep_datetime.strftime("%Y:%m:%d:%H:%M:%S"), new_bp, member[0],)
                    c.execute("UPDATE BnW SET upkeep_date = ?, bp = ? WHERE player_id = ?", listers)
                    conn.commit()

    @tasks.loop(seconds=10)
    async def empty_bp_alert(self):
        c.execute("SELECT player_id FROM BnW WHERE bp = 0 AND alert_flag = 0")
        pid_list = c.fetchall()
        pid_list = [x[0] for x in pid_list]
        if pid_list:
            for pid in pid_list:
                await self.bot.get_guild(config.GUILD_ID).get_member(int(pid)).send("Your character is at 0 BP due to infrequent feeding or inactivity. If your character remains on this list too long you risk being removed from Crossroads. When you log in please fill free to roll as many time as are necessary to fill your character's blood pool. You may then jump into play without accounting as the feeding occurred while you were offline.")
                lister = (pid,)
                c.execute("UPDATE BnW SET alert_flag = 1 WHERE player_id = ?", lister)
                conn.commit()

    @empty_bp_alert.before_loop
    async def before_alert(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=10)
    async def clear_empty_bp_alert(self):
        c.execute("SELECT player_id FROM BnW WHERE alert_flag = 1 AND bp != 0")
        pid_list = c.fetchall()
        pid_list = [x[0] for x in pid_list]
        for pid in pid_list:
            lister = (pid,)
            c.execute("UPDATE BnW SET alert_flag = 0 WHERE player_id = ?", lister)
            conn.commit()

    @commands.command()
    async def countdown(self, ctx):
        cd_delta = datetime(2017, 6, 10, 5).astimezone(pytz.utc) - time.ic_datetime_utc()
        cd_delta = cd_delta * (1 / config.DATE_COEFFICIENT)
        d_day = datetime.utcnow() + cd_delta
        await ctx.send(f"The effects of Critias's speech wears off at: {d_day.strftime('%m/%d/%Y, %H:%M')} UTC, which is in: {cd_delta.days} days, {cd_delta.seconds // 3600} hours, and {(cd_delta.seconds - ((cd_delta.seconds // 3600) * 3600)) // 60} minutes.")


def setup(bot):
    bot.add_cog(Time(bot))
