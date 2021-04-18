# bnw.py
# Controls manipulation of blood / willpower levels
from discord.ext import tasks, commands
import lib.dbman as db
import discord
import lib.utility as utility


class BnW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blood_bag.start()

    @tasks.loop(seconds=15)
    async def blood_bag(self):
        for guild in db.get_guild_list():
            guild = db.get_guild_info(guild[0])
            bb_role = self.bot.get_guild(guild.get("guild_id")).get_role(
                guild.get("bb_id")
            )
            bb_members = bb_role.members
            if bb_members is not None:
                for member in bb_members:
                    try:
                        player = db.get_player_info(guild.get("guild_id"), member.id)
                        if player.get("bp") + 1 <= player.get("bp_max"):
                            await self.bot.get_guild(guild.get("guild_id")).get_member(
                                member.id
                            ).remove_roles(bb_role)
                            new_bp = player.get("bp") + 1
                            db.execute(
                                "UPDATE Characters SET bp = %s WHERE id = %s",
                                (new_bp, player.get("id")),
                            )
                    except TypeError:
                        continue

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
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st(guild, ctx.author.roles):
            for member in ctx.guild.members:
                if guild.get("player_role") in member.roles:
                    try:
                        exist_check = db.get_player_info(ctx.guild.id, member.id)
                    except TypeError:
                        db.execute(
                            "INSERT INTO Characters (player_id, bp_max, bp, wp_max, wp, upkeep,"
                            "agg_dmg, alert_flag, guild_id) VALUES (%s,5,5,5,5,0,' ', 0,0,%s, 0, 0)",
                            (member.id, guild.get("id")),
                        )
            await ctx.send("Table populated.")

    @commands.command()
    async def add_player(self, ctx, member: discord.Member):
        """
        Adds a blank entry for the mentioned Discord user.
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st_nar(guild, ctx.author.roles):
            try:
                exist_check = db.get_player_info(ctx.guild.id, member.id)
            except TypeError:
                db.execute(
                    "INSERT INTO Characters (player_id, bp_max, bp, wp_max, wp, upkeep, upkeep_dt, agg_dmg, "
                    "alert_flag, guild_id, active_toggle, Experience) VALUES (%s,5,5,5,5,0,' ', 0,0,%s, 0, 0)",
                    (member.id, guild.get("id")),
                )
                await ctx.send("Player Added")
            else:
                await ctx.send(
                    "Player is already in the database for this server. Please remove them first."
                )

    @commands.command()
    async def set_bp(self, ctx, member: discord.Member, value):
        """
        Sets bp value of the specified member to the specified value (ST / Narrator only command).\n\
        Syntax: $set_bp [member] [value]\n\
        NOTE: This does not check BP max values, so through this command one may exceed BP limits.
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st_nar(guild, ctx.author.roles):
            if value:
                db.execute(
                    "UPDATE Characters SET bp = %s WHERE player_id = %s AND guild_id = %s",
                    (int(value), member.id, guild.get("id")),
                )
                await ctx.send("Value updated.")

    @commands.command()
    async def set_bp_max(self, ctx, member: discord.Member, value):
        """
        Sets bp max value of the specified member to the specified value (ST only command).\n\
        Syntax: $set_bp_max [member] [value]
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st_nar(guild, ctx.author.roles):
            db.execute(
                "UPDATE Characters SET bp_max = %s WHERE player_id = %s AND guild_id = %s",
                (value, member.id, guild.get("id")),
            )
            await ctx.send("Value updated.")

    @commands.command()
    async def set_wp(self, ctx, member: discord.Member, value):
        """
        Sets WP value of the specified member to the specified value (ST / Narrator only command).\n\
        Syntax: $set_wp [member] [value]\n\
        NOTE: This does not check WP max values, so through this command one may exceed WP limits.
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st_nar(guild, ctx.author.roles):
            db.execute(
                "UPDATE Characters SET wp = %s WHERE player_id = %s AND guild_id = %s",
                (value, member.id, guild.get("id")),
            )
            await ctx.send("Value updated.")

    @commands.command()
    async def set_wp_max(self, ctx, member: discord.Member, value):
        """
        Sets WP value of the specified member to the specified value (ST only command).\n\
        Syntax: $set_wp_max [member] [value]
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st_nar(guild, ctx.author.roles):
            db.execute(
                "UPDATE Characters SET wp_max = %s WHERE player_id = %s AND guild_id = %s",
                (value, member.id, guild.get("id")),
            )
            await ctx.send("Value updated.")

    @commands.command()
    async def set_agg_dmg(self, ctx, member: discord.Member, value):
        """
        Sets aggravated damage value of the specified member to the specified value (ST / Narrator only command).\n\
        Syntax: $set_agg_dmg [member] [value]
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st_nar(guild, ctx.author.roles):
            db.execute(
                "UPDATE Characters SET agg_dmg = %s WHERE player_id = %s AND guild_id = %s",
                (value, member.id, guild.get("id")),
            )
            await ctx.send("Value updated.")

    @commands.command()
    async def set_bp_upkeep(self, ctx, member: discord.Member, value):
        """
        Sets bp upkeep value of the specified member to the specified value (ST / Narrator only command).\n\
        Syntax: $set_bp_upkeep [member] [value]
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st_nar(guild, ctx.author.roles):
            db.execute(
                "UPDATE Characters SET upkeep = %s WHERE player_id = %s AND guild_id = %s",
                (value, member.id, guild.get("id")),
            )
            await ctx.send("Value updated.")

    @commands.command()
    async def check_stats(self, ctx, *, member: discord.Member = 0):
        """
        Checks the stats of the command's invoker, or if executed by an ST or narrator,\n\
        the command of a given member.\n\n\
        Syntax: $check_stats / $check_stats [member]
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st_nar(guild, ctx.author.roles):
            if member == 0:
                stats_member = ctx.author
            else:
                stats_member = member
        else:
            stats_member = ctx.author
        player = db.get_player_info(ctx.guild.id, stats_member.id)
        await ctx.author.send(
            f"--Stats for {stats_member.mention} on \"{ctx.guild.name}\"--\n\nBlood Points: {player.get('bp')}\nBlood "
            f"Point Cap: {player.get('bp_max')}\nWillpower: {player.get('wp')}\nWillpower Cap: {player.get('wp_max')}\n"
            f"Aggravated Damage: {player.get('agg_dmg')}\nMonthly Upkeep: {player.get('upkeep')}\nExperience: "
            f"{player.get('experience')}"
        )

    @commands.command()
    async def purge_bp_leavers(self, ctx):
        """
        Another ST only command. Goes through list of users and flags\n\
        ones to keep in the database from those still in server, purging the leavers.
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st(guild, ctx.author.roles):
            player_list = db.get_all_players(ctx.guild.id)
            for player in player_list:
                d_player = ctx.guild.get_member(player.get("player_id"))
                if d_player:
                    if d_player in ctx.guild.get_role(guild.get("player_role")).members:
                        db.execute(
                            "UPDATE Characters SET active_toggle = 1 WHERE id = %s",
                            player.get("id"),
                        )
            db.execute(
                "DELETE FROM Characters WHERE active_toggle = 0 AND guild_id = %s",
                guild.get("id"),
            )
            db.execute("UPDATE Characters SET active_toggle = 0")
            await ctx.send("Table updated.")

    @commands.command()
    async def rm_player(self, ctx, member):
        """
        Removes specified user from Blood and Willpower database.\n\
        Syntax: $rm_player [member]
        """
        guild = db.get_guild_info(ctx.guild.id)
        for role in ctx.author.roles:
            if guild.get("st_id") == role.id or guild.get("narrator_id") == role.id:
                authorized = True
        if authorized:
            db.execute(
                "DELETE FROM Characters WHERE player_id = %s AND guild_id = %s",
                (int(member), guild.get("id")),
            )
            await ctx.send("Value updated.")

    @commands.command()
    async def check_empty_bp(self, ctx):
        """
        Yet another ST only command. Returns a DM with a list of players\n\
        who have 0 blood points.
        """
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st(guild, ctx.author.roles):
            db.execute(
                "SELECT player_id from Characters WHERE bp = 0 AND guild_id = %s",
                guild.get("id"),
            )
            player_list = db.c.fetchall()
            i = 0
            zeros_message = ""
            while i < len(player_list):
                zeros_message += (
                    ctx.guild.get_member(int(player_list[i][0])).display_name + "\n"
                )
                i += 1
            await ctx.author.send(f"Players with 0 Blood Points:\n{zeros_message}")
        else:
            await ctx.send("Error: Insufficient permissions.")

    @commands.command()
    async def bp(self, ctx, arg1="none", arg2="none"):
        """
        BP checking and expenditure for all!\n\n\
        There's two versions of this command:\n\
        [+] All players - $bp checks BP level and DMs you, $bp [value] spends [value] BP\n\
        [+] STs and Narrators - $bp [user] checks their BP and DMs you, $bp [user] [value] works similarly.
        """
        if arg1 == "none":
            player = db.get_player_info(ctx.guild.id, ctx.author.id)
            await ctx.author.send(
                f"{ctx.author.mention}'s Blood Points: {player.get('bp')}"
            )
        else:
            user_id = None
            try:
                arg1 = int(arg1)
                if arg1 < 0:
                    await ctx.send("Error: Cannot spend negative BP.")
                elif arg1 < 100:
                    mod = arg1
                    player = db.get_player_info(ctx.guild.id, ctx.author.id)
                    if mod > player.get("bp"):
                        await ctx.send("Error: Cannot spend BP in excess of pool.")
                    else:
                        mod = player.get("bp") - mod
                        db.execute(
                            "UPDATE Characters SET bp = %s WHERE id = %s",
                            (mod, player.get("id")),
                        )
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
                guild = db.get_guild_info(ctx.guild.id)
                if utility.auth_check_st_nar(guild, ctx.author.roles):
                    if arg2 == "none":
                        player = db.get_player_info(ctx.guild.id, user_id)
                        await ctx.author.send(
                            f"{self.bot.get_user(user_id).mention}'s Blood Points: {player.get('bp')}"
                        )
                    else:
                        try:
                            mod = int(arg2)
                            if mod < 0:
                                await ctx.send("Error: Cannot spend negative BP.")
                            else:
                                player = db.get_player_info(ctx.guild.id, user_id)
                                if mod > player.get("bp"):
                                    await ctx.send(
                                        "Error: Cannot spend BP in excess of pool."
                                    )
                                else:
                                    mod = player.get("bp") - mod
                                    db.execute(
                                        "UPDATE Characters SET bp = %s WHERE id = %s",
                                        (mod, player.get("id")),
                                    )
                                    await ctx.send("Values updated.")
                        except ValueError:
                            await ctx.send("Error: Invalid syntax.")

    @commands.command()
    async def wp(self, ctx, arg1="none", arg2="none"):
        """
        WP checking and expenditure for all!\n\n\
        There's two versions of this command:\n\
        [+] All players - $wp checks WP level and DMs you, $wp [value] spends [value] BP\n\
        [+] STs and Narrators - $wp [user] checks their WP and DMs you, $wp [user] [value] works similarly.
        """
        if arg1 == "none":
            player = db.get_player_info(ctx.guild.id, ctx.author.id)
            await ctx.author.send(
                f"{ctx.author.mention}'s Willpower: {player.get('wp')}"
            )
        else:
            user_id = None
            try:
                arg1 = int(arg1)
                if arg1 < 0:
                    await ctx.send("Error: Cannot spend negative WP.")
                elif arg1 < 100:
                    mod = arg1
                    player = db.get_player_info(ctx.guild.id, ctx.author.id)
                    if mod > player.get("wp"):
                        await ctx.send("Error: Cannot spend WP in excess of pool.")
                    else:
                        mod = player.get("wp") - mod
                        db.execute(
                            "UPDATE Characters SET wp = %s WHERE id = %s",
                            (mod, player.get("id")),
                        )
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
                guild = db.get_guild_info(ctx.guild.id)
                if utility.auth_check_st_nar(guild, ctx.author.roles):
                    if arg2 == "none":
                        player = db.get_player_info(ctx.guild.id, user_id)
                        await ctx.author.send(
                            f"{self.bot.get_user(user_id).mention}'s Willpower: {player.get('wp')}"
                        )
                    else:
                        try:
                            mod = int(arg2)
                            if mod < 0:
                                await ctx.send("Error: Cannot spend negative WP.")
                            else:
                                player = db.get_player_info(ctx.guild.id, user_id)
                                if mod > player.get("wp"):
                                    await ctx.send(
                                        "Error: Cannot spend WP in excess of pool."
                                    )
                                else:
                                    mod = player.get("wp") - mod
                                    db.execute(
                                        "UPDATE Characters SET wp = %s WHERE id = %s",
                                        (mod, player.get("id")),
                                    )
                                    await ctx.send("Values updated.")
                        except ValueError:
                            await ctx.send("Error: Invalid syntax.")

    @commands.command()
    async def set_exp(self, ctx, member, value):
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st(guild, ctx.author.roles):
            db.execute("UPDATE Characters SET Experience = %s WHERE player_id = %s",
                       (int(value), int(member)))
            await ctx.send("Experience set successfully.")

    @commands.command()
    async def add_exp(self, ctx, member, value):
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st(guild, ctx.author.roles):
            player = db.get_player_info(ctx.guild.id, int(member))
            new_exp = player.get('experience') + int(value)
            db.execute("UPDATE Characters SET Experience = %s WHERE player_id = %s",
                       (new_exp, player.get('player_id')))
            await ctx.send("Experience added successfully.")

    @commands.command()
    async def add_exp_role(self, ctx, role_added: discord.Role, value):
        guild = db.get_guild_info(ctx.guild.id)
        if utility.auth_check_st(guild, ctx.author.roles):
            r_list = role_added.members
            print(r_list)
            for member in r_list:
                player = db.get_player_info(ctx.guild.id, member.id)
                new_exp = player.get('experience') + int(value)
                db.execute("UPDATE Characters SET Experience = %s WHERE player_id = %s AND guild_id = %s",
                           (new_exp, player.get('player_id'), player.get('guild_id')))
            await ctx.send("Experience added successfully.")


def setup(bot):
    bot.add_cog(BnW(bot))
