# bnw.py
# Controls manipulation of blood / willpower levels
from discord.ext import tasks, commands
from lib.dbman import c, conn
import config
import discord


class BnW(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.blood_bag.start()

    @tasks.loop(seconds=15)
    async def blood_bag(self):
        c.execute("SELECT player_id, bp, bp_max FROM BnW")
        global member_list
        member_list = c.fetchall()
        for member in member_list:
            member_id = member[0]
            bp = member[1]
            bp_max = member[2]
            bb_members = self.bot.get_guild(config.GUILD_ID).get_role(config.BB_ROLE).members
            if bb_members is not None:
                if bp + 1 <= bp_max:
                    if self.bot.get_guild(config.GUILD_ID).get_member(member_id) in bb_members:
                        await self.bot.get_guild(config.GUILD_ID).get_member(member_id).remove_roles(self.bot.get_guild(config.GUILD_ID).get_role(config.BB_ROLE))
                        new_bp = bp + 1
                        listers = (new_bp, member_id,)
                        c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                        conn.commit()

    @blood_bag.before_loop
    async def loop_starts(self):
        await self.bot.wait_until_ready()

    # bp_wp_pop()
    # Again uses authentication loop for STs
    # Populates any new users into the BnW database
    # Skips over any users with a Bot role and those who already exist in the database
    @commands.command()
    async def bp_wp_pop(self, ctx):
        """
        Populates BP/WP database with users in-server. (ST only command)\n\
        Does not affect those who already have entries in the table.\n\
        Will set all values other than their player_id to 0.
        """
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            for member in self.bot.get_guild(config.GUILD_ID).members:
                if config.PLAYER_ROLE in member.roles:
                    lister = (member.id,)
                    c.execute("SELECT * FROM BnW WHERE player_id = ?", lister)
                    exist_check = c.fetchone()
                    if not exist_check:
                        c.execute("INSERT INTO BnW VALUES (?,0,0,0,0,0,0,0,'0',0)", lister)
                        conn.commit()
        elif auth_nh:
            for member in self.bot.get_guild(config.GUILD_NH).members:
                if config.PLAYER_NH in member.roles:
                    lister = (member.id,)
                    c.execute("SELECT * FROM NHBnW WHERE player_id = ?", lister)
                    exist_check = c.fetchone()
                    if not exist_check:
                        c.execute("INSERT INTO NHBnW VALUES (?,0,0,0,0,0,0,0,'0',0)", lister)
                        conn.commit()
            await ctx.send("Table populated.")

    @commands.command()
    async def add_player(self, ctx, member: discord.Member):
        '''
        Adds a blank entry for the mentioned Discord user.
        '''
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.NARRATOR_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            c.execute("INSERT INTO BnW VALUES(?,0,0,0,0,0,0,0,'0',0);",(member.id,))
            conn.commit()
            await ctx.send("Player Added")
        elif auth_nh:
            c.execute("INSERT INTO NHBnW VALUES(?,0,0,0,0,0,0,0,'0',0);", (member.id,))
            conn.commit()
            await ctx.send("Player Added")

    @commands.command()
    async def set_bp(self, ctx, member: discord.Member, value):
        '''
        Sets bp value of the specified member to the specified value (ST / Narrator only command).\n\
        Syntax: $set_bp [member] [value]\n\
        NOTE: This does not check BP max values, so through this command one may exceed BP limits.
        '''
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.NARRATOR_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            lister = (value, member.id,)
            c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")
        elif auth_nh:
            lister = (value, member.id,)
            c.execute("UPDATE NHBnW SET bp = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")

    @commands.command()
    async def set_bp_max(self, ctx, member: discord.Member, value):
        '''
        Sets bp max value of the specified member to the specified value (ST only command).\n\
        Syntax: $set_bp_max [member] [value]
        '''
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.NARRATOR_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            lister = (value, member.id,)
            c.execute("UPDATE BnW SET bp_max = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")
        elif auth_nh:
            lister = (value, member.id,)
            c.execute("UPDATE NHBnW SET bp_max = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")

    @commands.command()
    async def set_wp(self, ctx, member: discord.Member, value):
        '''
        Sets WP value of the specified member to the specified value (ST / Narrator only command).\n\
        Syntax: $set_wp [member] [value]\n\
        NOTE: This does not check WP max values, so through this command one may exceed WP limits.
        '''
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.NARRATOR_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            lister = (value, member.id,)
            c.execute("UPDATE BnW SET wp = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")
        elif auth_nh:
            lister = (value, member.id,)
            c.execute("UPDATE NHBnW SET wp = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")

    @commands.command()
    async def set_wp_max(self, ctx, member: discord.Member, value):
        '''
        Sets WP value of the specified member to the specified value (ST only command).\n\
        Syntax: $set_wp_max [member] [value]
        '''
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.NARRATOR_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            lister = (value, member.id,)
            c.execute("UPDATE BnW SET wp_max = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")
        elif auth_nh:
            lister = (value, member.id,)
            c.execute("UPDATE NHBnW SET wp_max = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")

    @commands.command()
    async def set_agg_dmg(self, ctx, member: discord.Member, value):
        '''
        Sets aggravated damage value of the specified member to the specified value (ST / Narrator only command).\n\
        Syntax: $set_agg_dmg [member] [value]
        '''
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.NARRATOR_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            lister = (value, member.id,)
            c.execute("UPDATE BnW SET agg_dmg = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")
        elif auth_nh:
            lister = (value, member.id,)
            c.execute("UPDATE NHBnW SET agg_dmg = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")

    @commands.command()
    async def set_bp_upkeep(self, ctx, member: discord.Member, value):
        '''
        Sets bp upkeep value of the specified member to the specified value (ST / Narrator only command).\n\
        Syntax: $set_bp_upkeep [member] [value]
        '''
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.NARRATOR_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            lister = (value, member.id,)
            c.execute("UPDATE BnW SET upkeep = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")
        elif auth_nh:
            lister = (value, member.id,)
            c.execute("UPDATE NHBnW SET upkeep = ? WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")


    @commands.command()
    async def check_stats(self, ctx, *, member: discord.Member = 0):
        '''
        Checks the stats of the command's invoker, or if executed by an ST or narrator,\n\
        the command of a given member.\n\n\
        Syntax: $check_stats / $check_stats [member]
        '''
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.NARRATOR_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            if member == 0:
                global stats_member
                stats_member = ctx.author
            else:
                stats_member = member
        elif auth_nh:
            if member == 0:
                stats_member = ctx.author
            else:
                stats_member = member
        else:
            stats_member = ctx.author
        lister = (stats_member.id,)
        if ctx.guild.id == config.GUILD_ID:
            c.execute("SELECT * FROM BnW WHERE player_id = ?", lister)
        elif ctx.guild.id == config.GUILD_NH:
            c.execute("SELECT * FROM NHBnW WHERE player_id = ?", lister)
        data = c.fetchone()
        await ctx.author.send(f"--Stats for {stats_member.mention}--\n\nBlood Points: {data[1]}\nBlood Point Cap: {data[2]}\nWillpower: {data[3]}\nWillpower Cap: {data[4]}\nAggravated Damage: {data[5]}\nMonthly Upkeep: {data[7]}")

    @commands.command()
    async def purge_bp_leavers(self, ctx):
        '''
        Another ST only command. Goes through list of users and flags\n\
        ones to keep in the database from those still in server, purging the leavers.
        '''
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
        if authorized:
            c.execute("SELECT player_id FROM BnW")
            db_list = list(c.fetchall())
            for member in self.bot.get_guild(config.GUILD_ID).members:
                if str(member.id) in str(db_list):
                    if member in self.bot.get_guild(config.GUILD_ID).get_role(config.PLAYER_ROLE).members:
                        lister = (member.id,)
                        c.execute("UPDATE BnW SET active_toggle = 1 WHERE player_id = ?", lister)
                        conn.commit()
            c.execute("DELETE FROM BnW WHERE active_toggle = 0")
            conn.commit()
            c.execute("UPDATE BnW SET active_toggle = 0")
            conn.commit()
            await ctx.send("Table updated.")

    @commands.command()
    async def feed_bp(self, ctx, member: discord.Member, amount=0):
        '''
        Takes a specified amount of BP from the user of the command, and gives it to a specified user.
        Syntax: $feed_bp [member] [amount]
        '''
        amount = int(amount)
        if amount < 1:
            await ctx.send("Error: You must feed at least 1 bp to feed someone.")
        else:
            lister = (ctx.author.id,)
            c.execute("SELECT bp FROM BnW WHERE player_id = ?", lister)
            user_pool = c.fetchone()
            if int(user_pool[0]) < amount:
                await ctx.send("Error: Cannot feed in excess of invoker's pool.")
            else:
                lister = (member.id,)
                c.execute("SELECT bp, bp_max FROM BnW WHERE player_id = ?", lister)
                data = c.fetchone()
                target_bp = int(data[0])
                target_max = int(data[1])
                if target_bp == target_max:
                    await ctx.send("Error: Cannot feed target with full BP.")
                else:
                    hunger = target_max - target_bp
                    if hunger < amount:
                        listers = (target_max,member.id,)
                        c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                        conn.commit()
                        new_user_pool = int(user_pool[0]) - hunger
                        listers = (new_user_pool,ctx.author.id,)
                        c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                        conn.commit()
                        await ctx.send(f"Successfully fed {member.mention} {hunger} blood points.")
                    else:
                        new_target_bp = target_bp - amount
                        listers = (new_target_bp, member.id,)
                        c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                        conn.commit()
                        new_user_pool = int(user_pool[0]) - amount
                        listers = (new_user_pool, ctx.author.id,)
                        c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                        conn.commit()
                        await ctx.send(f"Successfully fed <@{member.id}> {amount} blood points.")

    @commands.command()
    async def rm_player(self, ctx, member: discord.Member):
        '''
        Removes specified user from Blood and Willpower database.\n\
        Syntax: $rm_player [member]
        '''
        authorized = False
        auth_nh = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
            elif config.NARRATOR_ROLE == role.id:
                authorized = True
            elif config.ST_NH == role.id:
                auth_nh = True
        if authorized:
            lister = (member.id,)
            c.execute("DELETE FROM BnW WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")
        if auth_nh:
            lister = (member.id,)
            c.execute("DELETE FROM NHBnW WHERE player_id = ?", lister)
            conn.commit()
            await ctx.send("Value updated.")

    @commands.command()
    async def check_empty_bp(self, ctx):
        '''
        Yet another ST only command. Returns a DM with a list of players\n\
        who have 0 blood points.
        '''
        authorized = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
        if authorized:
            c.execute("SELECT player_id from BnW WHERE bp = 0")
            player_list = c.fetchall()
            i = 0
            global zeros_message
            zeros_message = ""
            while i < len(player_list):
                zeros_message += self.bot.get_guild(config.GUILD_ID).get_member(int(player_list[i][0])).display_name + "\n"
                i += 1
            await ctx.author.send(f"Players with 0 Blood Points:\n{zeros_message}")
        else:
            await ctx.send("Error: Insufficient permissions.")

    @commands.command()
    async def bp(self, ctx, arg1="none", arg2="none"):
        '''
        BP checking and expenditure for all!\n\n\
        There's two versions of this command:\n\
        [+] All players - $bp checks BP level and DMs you, $bp [value] spends [value] BP\n\
        [+] STs and Narrators - $bp [user] checks their BP and DMs you, $bp [user] [value] works similarly.
        '''
        if arg1 == "none":
            lister = (ctx.author.id,)
            if ctx.guild.id == config.GUILD_ID:
                c.execute("SELECT bp FROM BnW WHERE player_id = ?", lister)
            elif ctx.guild.id == config.GUILD_NH:
                c.execute("SELECT bp FROM NHBnW WHERE player_id = ?", lister)
            data = c.fetchone()
            await ctx.author.send(f"{ctx.author.mention}'s Blood Points: {data[0]}")
        else:
            global user_id
            user_id = None
            try:
                arg1 = int(arg1)
                if arg1 < 0:
                    await ctx.send("Error: Cannot spend negative BP.")
                elif arg1 < 100:
                    mod = arg1
                    lister = (ctx.author.id,)
                    c.execute("SELECT bp FROM BnW WHERE player_id = ?", lister)
                    data = c.fetchone()
                    if mod > int(data[0]):
                        await ctx.send("Error: Cannot spend BP in excess of pool.")
                    else:
                        mod = int(data[0]) - mod
                        listers = (mod, ctx.author.id,)
                        c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                        conn.commit()
                        await ctx.send("Values updated.")
                else:
                    user_id = arg1
            except ValueError:
                try:
                    uid = self.bot.get_user(int(arg1[2:-1])).id
                    if uid is None:
                        await ctx.send("Error: Invalid syntax.")
                    else:
                        user_id = uid
                except ValueError:
                    await ctx.send("Error: Invalid syntax.")
            if user_id is not None:
                authorized = False
                for role in ctx.author.roles:
                    if config.ST_ROLE == role.id:
                        authorized = True
                    elif config.NARRATOR_ROLE == role.id and ctx.channel == self.bot.get_channel(config.COMMANDS_CHAN):
                        authorized = True
                if authorized:
                    if arg2 == "none":
                        lister = (user_id,)
                        c.execute("SELECT bp FROM BnW WHERE player_id = ?", lister)
                        data = c.fetchone()
                        await ctx.author.send(f"{self.bot.get_user(user_id).mention}'s Blood Points: {data[0]}")
                    else:
                        try:
                            mod = int(arg2)
                            if mod < 0:
                                await ctx.send("Error: Cannot spend negative BP.")
                            else:
                                lister = (user_id,)
                                c.execute("SELECT bp FROM BnW WHERE player_id = ?", lister)
                                data = c.fetchone()
                                if mod > int(data[0]):
                                    await ctx.send("Error: Cannot spend BP in excess of pool.")
                                else:
                                    mod = int(data[0]) - mod
                                    listers = (mod, user_id,)
                                    c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                                    conn.commit()
                                    await ctx.send("Values updated.")
                        except ValueError:
                            await ctx.send("Error: Invalid syntax.")

    @commands.command()
    async def wp(self, ctx, arg1="none", arg2="none"):
        '''
        WP checking and expenditure for all!\n\n\
        There's two versions of this command:\n\
        [+] All players - $wp checks WP level and DMs you, $wp [value] spends [value] BP\n\
        [+] STs and Narrators - $wp [user] checks their WP and DMs you, $wp [user] [value] works similarly.
        '''
        if arg1 == "none":
            lister = (ctx.author.id,)
            c.execute("SELECT wp FROM BnW WHERE player_id = ?", lister)
            data = c.fetchone()
            await ctx.author.send(f"{ctx.author.mention}'s Willpower: {data[0]}")
        else:
            global user_id
            user_id = None
            try:
                arg1 = int(arg1)
                if arg1 < 0:
                    await ctx.send("Error: Cannot spend negative WP.")
                elif arg1 < 100:
                    mod = arg1
                    lister = (ctx.author.id,)
                    c.execute("SELECT wp FROM BnW WHERE player_id = ?", lister)
                    data = c.fetchone()
                    if mod > int(data[0]):
                        await ctx.send("Error: Cannot spend WP in excess of pool.")
                    else:
                        mod = int(data[0]) - mod
                        listers = (mod, ctx.author.id,)
                        c.execute("UPDATE BnW SET wp = ? WHERE player_id = ?", listers)
                        conn.commit()
                        await ctx.send("Values updated.")
                else:
                    user_id = arg1
            except ValueError:
                try:
                    uid = self.bot.get_user(int(arg1[2:-1])).id
                    if uid is None:
                        await ctx.send("Error: Invalid syntax.")
                    else:
                        user_id = uid
                except ValueError:
                    await ctx.send("Error: Invalid syntax.")
            if user_id is not None:
                authorized = False
                for role in ctx.author.roles:
                    if config.ST_ROLE == role.id:
                        authorized = True
                    elif config.NARRATOR_ROLE == role.id and ctx.channel == self.bot.get_channel(config.COMMANDS_CHAN):
                        authorized = True
                if authorized:
                    if arg2 == "none":
                        lister = (user_id,)
                        c.execute("SELECT wp FROM BnW WHERE player_id = ?", lister)
                        data = c.fetchone()
                        await ctx.author.send(f"{self.bot.get_user(user_id).mention}'s Willpower: {data[0]}")
                    else:
                        try:
                            mod = int(arg2)
                            if mod < 0:
                                await ctx.send("Error: Cannot spend negative WP.")
                            else:
                                lister = (user_id,)
                                c.execute("SELECT wp FROM BnW WHERE player_id = ?", lister)
                                data = c.fetchone()
                                if mod > int(data[0]):
                                    await ctx.send("Error: Cannot spend WP in excess of pool.")
                                else:
                                    mod = int(data[0]) - mod
                                    listers = (mod, user_id,)
                                    c.execute("UPDATE BnW SET wp = ? WHERE player_id = ?", listers)
                                    conn.commit()
                                    await ctx.send("Values updated.")
                        except ValueError:
                            await ctx.send("Error: Invalid syntax.")


def setup(bot):
    bot.add_cog(BnW(bot))