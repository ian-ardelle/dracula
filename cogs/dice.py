from discord.ext import commands
import lib.dbman as db
import random


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def r(self, ctx, pool: int = 1, diff: int = 6, wp: str = "0", *reason):
        """
        Rolls and checks successes.\n\
        Syntax: $r [Dice Pool] [Difficulty] [modifier]\n\
        \n\
        Example: $r 5 7 => [5, 2, 8, 4, 3] Results: 1 Successes!
        """
        alert_st = 0
        reason_string = ""
        if pool < 1:
            pass

        elif diff < 1:
            pass

        else:
            reason = list(reason)
            try:
                wp = int(wp)
            except ValueError:
                reason.insert(0, wp)
                wp = 0
            if not reason:
                reason = ["No reason provided."]
            for word in reason:
                reason_string += word + " "
            reason_string = reason_string[:-1]
            ss = 0
            fail = 0
            random_raw = []
            for i in range(pool):
                random_raw.append(random.randint(1, 10))
            await ctx.send(random_raw)
            for roll in random_raw:
                if roll >= diff:
                    ss += 1

                if roll == 1:
                    fail += 1

            if ss <= 0 and wp <= 0:
                if fail > 0:
                    result = "Botch! | Reason: " + str(reason_string)
                    alert_st = 2

                else:
                    result = "Failure! | Reason: " + str(reason_string)
                    alert_st = 1

            elif ss - fail <= 0 < ss and wp <= 0:
                result = "Failure! | Reason: " + str(reason_string)
                alert_st = 1

            else:
                ss += wp
                if ss - fail > 0:
                    result = (
                        str(ss - fail) + " successes! | Reason: " + str(reason_string)
                    )
                else:
                    result = (
                        "{} successes!".format(str(wp))
                        + " | Reason: "
                        + str(reason_string)
                    )
            await ctx.send("{} - Results: ".format(ctx.author.mention) + result)
            guild = db.get_guild_info(ctx.guild.id)
            if ctx.channel.id == guild.get("feeding_chan"):
                net_ss = ss - fail
                if net_ss < 0:
                    net_ss = wp
                player = db.get_player_info(ctx.guild.id, ctx.author.id)
                current_bp = player.get("bp")
                bp_max = player.get("bp_max")
                new_bp = current_bp + net_ss
                if new_bp > bp_max:
                    new_bp = bp_max
                db.execute(
                    "UPDATE Characters SET bp = %s WHERE id = %s",
                    (new_bp, player.get("id")),
                )
                if alert_st == 1:
                    await self.bot.get_channel(guild.get("st_alerts_chan")).send(
                        "{} failed a feeding roll!".format(ctx.author.mention)
                    )
                elif alert_st == 2:
                    await self.bot.get_channel(guild.get("st_alerts_chan")).send(
                        "{} botched a feeding roll!".format(ctx.author.mention)
                    )

    @commands.command()
    async def rs(self, ctx, pool: int = 1, diff: int = 6, wp: str = "0", *reason):
        """
        Same as $r except this also applies explosions to the dice.\n\
        Syntax: $rs [Dice Pool] [Difficulty] [wpifier]\n\
        \n\
        Example: $rs 5 7 => [10, 2, 8, 4, 3] [9] Results: 3 Successes!
        """
        st_alert = 0
        reason_string = ""

        if pool < 1:
            pass

        elif diff < 1:
            pass

        else:
            reason = list(reason)
            try:
                wp = int(wp)
            except ValueError:
                reason.insert(0, wp)
                wp = 0
            if not reason:
                reason = ["No reason provided."]
            for word in reason:
                reason_string += word + " "
            reason_string = reason_string[:-1]
            ss = 0
            fail = 0
            tens = 0
            random_raw = []
            for i in range(pool):
                random_raw.append(random.randint(1, 10))
            await ctx.send(random_raw)
            for roll in random_raw:
                if roll >= diff:
                    ss += 1

                elif roll == 1:
                    fail += 1

                if roll == 10:
                    tens += 1
            guild = db.get_guild_info(ctx.guild.id)
            if guild.get("exploding_toggle") == 1:
                if ss <= 0 and wp <= 0:
                    if fail > 0:
                        result = "Botch! | Reason: " + str(reason_string)
                        st_alert = 2

                    else:
                        result = "Failure! | Reason: " + str(reason_string)
                        st_alert = 1

                else:
                    ss -= fail
                    tens -= fail
                    while tens > 0:
                        explosion = []
                        for i in range(tens):
                            explosion.append(random.randint(1, 10))
                        await ctx.send(explosion)
                        ten = 0
                        for roll in explosion:
                            if roll == 10:
                                ten += 1
                                ss += 1
                            elif roll >= diff:
                                ss += 1
                        tens = ten
                    if ss <= 0:
                        ss = wp
                    else:
                        ss += wp

                    if ss <= 0:
                        result = "Failure! | Reason: " + str(reason_string)
                        st_alert = 1
                    else:
                        result = str(ss) + " Successes! | Reason: " + str(reason_string)
            elif guild.get("exploding_toggle") == 0:
                ss += tens
                ss -= fail
                if ss <= 0:
                    ss = wp
                else:
                    ss += wp

                if ss <= 0:
                    result = "Failure! | Reason: " + str(reason_string)
                    st_alert = 1
                else:
                    result = str(ss) + " Successes! | Reason: " + str(reason_string)

            await ctx.send("{} - Results: ".format(ctx.author.mention) + result)
            if ctx.channel.id == guild.get("feeding_chan"):
                net_ss = ss - fail
                if net_ss < 0:
                    net_ss = wp
                player = db.get_player_info(ctx.guild.id, ctx.author.id)
                current_bp = player.get("bp")
                bp_max = player.get("bp_max")
                new_bp = current_bp + net_ss
                if new_bp > bp_max:
                    new_bp = bp_max
                db.execute(
                    "UPDATE Characters SET bp = %s WHERE id = %s",
                    (new_bp, player.get("id")),
                )
                if st_alert == 1:
                    await self.bot.get_channel(guild.get("st_alerts_chan")).send(
                        "{} failed a feeding roll!".format(ctx.author.mention)
                    )
                elif st_alert == 2:
                    await self.bot.get_channel(guild.get("st_alerts_chan")).send(
                        "{} botched a feeding roll!".format(ctx.author.mention)
                    )


def setup(bot):
    bot.add_cog(Dice(bot))
