from discord.ext import commands
from lib import rand_org_gen
import config
from lib.dbman import c, conn


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def r(self, ctx, pool: int = 1, diff: int = 6, wp: int = 0):
        """
        Rolls and checks successes.\n\
        Syntax: $r [Dice Pool] [Difficulty] [modifier]\n\
        \n\
        Example: $r 5 7 => [5, 2, 8, 4, 3] Results: 1 Successes!
        """
        global alert_st
        alert_st = 0
        if pool < 1:
            pass

        elif diff < 1:
            pass

        else:
            ss = 0
            fail = 0
            random_raw = rand_org_gen.gen(pool, 10)
            await ctx.send(random_raw)
            for roll in random_raw:
                if roll >= diff:
                    ss += 1

                if roll == 1:
                    fail += 1

            if ss <= 0 and wp <= 0:
                if fail > 0:
                    result = "Botch!"
                    alert_st = 2

                else:
                    result = "Failure!"
                    alert_st = 1

            elif ss - fail <= 0 < ss and wp <= 0:
                result = "Failure!"
                alert_st = 1

            else:
                ss += wp
                if ss - fail > 0:
                    result = str(ss - fail) + " successes!"
                else:
                    result = "{} successes!".format(str(wp))
            await ctx.send("{} - Results: ".format(ctx.author.mention) + result)
            if ctx.channel == self.bot.get_channel(config.FEEDING_CHANNEL):
                global ss_net
                ss_net = ss - fail
                if ss_net < 0:
                    ss_net = wp
                lister = (ctx.author.id,)
                c.execute("SELECT bp, bp_max FROM BnW WHERE player_id = ?", lister)
                global new_bp
                bp_data = list(c.fetchone())
                current_bp = int(bp_data[0])
                bp_max = int(bp_data[1])
                if current_bp + ss > bp_max:
                    new_bp = bp_max
                else:
                    new_bp = current_bp + ss_net
                listers = (new_bp, ctx.author.id,)
                c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                conn.commit()
                if alert_st == 1:
                    await self.bot.get_channel(config.ST_ALERTS_CHANNEL).send("{} failed a feeding roll!".format(ctx.author.mention))
                elif alert_st == 2:
                    await self.bot.get_channel(config.ST_ALERTS_CHANNEL).send("{} botched a feeding roll!".format(ctx.author.mention))

    @commands.command()
    async def re(self, ctx, pool: int = 1, diff: int = 6, wp: int = 0):
        '''
        Same as $r except this also applies explosions to the dice.\n\
        Syntax: $re [Dice Pool] [Difficulty] [wpifier]\n\
        \n\
        Example: $re 5 7 => [10, 2, 8, 4, 3] [9] Results: 3 Successes!
        '''
        global st_alert
        st_alert = 0
        if pool < 1:
            pass

        elif diff < 1:
            pass

        else:
            ss = 0
            fail = 0
            tens = 0
            random_raw = rand_org_gen.gen(pool, 10)
            await ctx.send(random_raw)
            for roll in random_raw:
                if roll >= diff:
                    ss += 1

                elif roll == 1:
                    fail += 1

                if roll == 10:
                    tens += 1

            if ss <= 0 and wp <= 0:
                if fail > 0:
                    result = "Botch!"
                    st_alert = 2

                else:
                    result = "Failure!"
                    st_alert = 1

            else:
                ss -= fail
                tens -= fail
                while tens > 0:
                    explosion = rand_org_gen.gen(tens, 10)
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
                    result = "Failure!"
                    st_alert = 1
                else:
                    result = str(ss) + " Successes!"
            await ctx.send("{} - Results: ".format(ctx.author.mention) + result)
            if ctx.channel == self.bot.get_channel(config.FEEDING_CHANNEL):
                global ss_net
                ss_net = ss - fail
                if ss_net < 0:
                    ss_net = wp
                lister = (ctx.author.id,)
                c.execute("SELECT bp, bp_max FROM BnW WHERE player_id = ?", lister)
                global new_bp
                bp_data = list(c.fetchone())
                current_bp = int(bp_data[0])
                bp_max = int(bp_data[1])
                if current_bp + ss > bp_max:
                    new_bp = bp_max
                else:
                    new_bp = current_bp + ss_net
                listers = (new_bp, ctx.author.id,)
                c.execute("UPDATE BnW SET bp = ? WHERE player_id = ?", listers)
                conn.commit()
                if st_alert == 1:
                    await self.bot.get_channel(config.ST_ALERTS_CHANNEL).send("{} failed a feeding roll!".format(ctx.author.mention))
                elif st_alert == 2:
                    await self.bot.get_channel(config.ST_ALERTS_CHANNEL).send("{} botched a feeding roll!".format(ctx.author.mention))


def setup(bot):
    bot.add_cog(Dice(bot))
