from discord.ext import commands
import config
import os
from lib.dbman import c, conn
from lib import rand_org_gen
import discord
from datetime import datetime, timedelta


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def numchan(self, ctx):
        chanlist = ctx.guild.channels
        await ctx.send(f"The number of channels in the server is: {len(chanlist)}")

    @commands.command(hidden=True)
    async def testicles(self, ctx):
        await ctx.send("Testicles confirmed.")

    '''@commands.command()
    async def optin(self, ctx):
        member = ctx.author.id
        lister = (member,)
        c.execute("SELECT * FROM SecretSanta WHERE sender_id = ?", lister)
        exist_check = c.fetchone()
        if not exist_check:
            c.execute("INSERT INTO SecretSanta VALUES (?,0)", lister)
            conn.commit()
            await ctx.send("User added into Secret Santa randomizer!")
        else:
            await ctx.send("Error: User already opted into Secret Santa")

    @commands.command()
    async def ss_gen(self, ctx):
        authorized = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
        if authorized:
            c.execute("SELECT * FROM SecretSanta")
            raw_sender_list = c.fetchall()
            sender_list = []
            for sender in raw_sender_list:
                sender_list.append(int(sender[0]))
            quality_check = 0
            while quality_check == 0:
                quality_check = 1
                random_raw = rand_org_gen.gen(len(sender_list), len(sender_list), False)
                for x in random_raw:
                    if x == random_raw[x-1]:
                        quality_check = 0
            receiver_list = []
            for x in random_raw:
                receiver_list.append(sender_list[int(x-1)])
            user_num = len(sender_list)
            y = 0
            while y < user_num:
                listers = (receiver_list[y], sender_list[y])
                c.execute("UPDATE SecretSanta SET receiver_id = ? WHERE sender_id = ?", listers)
                y += 1
            conn.commit()
            await ctx.send("List generated successfully!")

    @commands.command()
    async def my_ss(self, ctx):
        lister = (ctx.author.id,)
        c.execute("SELECT * FROM SecretSanta WHERE sender_id = ?", lister)
        output = c.fetchone()
        await ctx.author.send("Your secret santa gift recipient is: " + self.bot.get_guild(config.GUILD_ID).get_member(output[1]).display_name)

    @commands.command(hidden=True)
    async def ss_dumb(self, ctx):
        authorized = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
        if authorized:
            message = "Sender, Receiver\n"
            c.execute("SELECT * FROM SecretSanta")
            outputs = c.fetchall()
            for entry in outputs:
                message += str(self.bot.get_guild(config.GUILD_ID).get_member(entry[0]).display_name) + ", " + str(self.bot.get_guild(config.GUILD_ID).get_member(entry[1]).display_name) + "\n"
            await ctx.author.send(message)'''

    @commands.command()
    async def start_auction(self, ctx, member: discord.Member):
        authorized = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
        if authorized:
            lister = (member.id,)
            c.execute("INSERT INTO Auction VALUES(?,0,500,1)", lister)
            conn.commit()
            await ctx.send("A new auction has been started for having a date with " + str(member.mention) + "! Get your bids in now by typing $bid [amount]!")

    @commands.command()
    async def bid(self, ctx, bid):
        c.execute("SELECT * FROM Auction WHERE active = 1")
        entry = c.fetchone()
        if int(bid) % 50 == 0:
            if int(bid) > entry[2]:
                listers = (ctx.author.id, bid,)
                c.execute("UPDATE Auction SET bidder = ?, bid = ? WHERE active = 1", listers)
                conn.commit()
                await ctx.send("New Highest Bidder! " + ctx.author.mention + " has bid $" + str(bid) + " on " + self.bot.get_guild(config.GUILD_ID).get_member(entry[0]).mention + "!")
        else:
            await ctx.send("Bid must be an in an increment of $50!")

    @commands.command()
    async def end_auction(self, ctx):
        c.execute("SELECT * FROM Auction WHERE active = 1")
        active_auctions = c.fetchall()
        c.execute("UPDATE Auction SET active = 0 WHERE active = 1")
        conn.commit()
        if active_auctions:
            message = "The auction on the following person has ended:"
            for auction in active_auctions:
                message += "\n" + str(self.bot.get_guild(config.GUILD_ID).get_member(auction[0]).mention) + " with a bid of $" + str(auction[2]) + " by " + str(self.bot.get_guild(config.GUILD_ID).get_member(auction[1]).mention) + "."
        else:
            message = "There are no active auctions at this time."
        await ctx.send(message)

    @commands.command()
    async def auction_results(self, ctx):
        c.execute("SELECT * FROM Auction WHERE active = 0")
        auction_dump = c.fetchall()
        message = "The auction results are as follows:"
        for auction in auction_dump:
            message += f"\nDate with {self.bot.get_guild(config.GUILD_ID).get_member(auction[0]).mention} - sold to {self.bot.get_guild(config.GUILD_ID).get_member(auction[1]).mention} for ${str(auction[2])}"
        await ctx.send(message)

    @commands.command()
    async def clear_auction(self, ctx, member: discord.Member):
        authorized = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
        if authorized:
            lister = (member.id,)
            c.execute("DELETE FROM Auction WHERE auctioned = ?", lister)
            conn.commit()
            await ctx.send(f"Auction for {member.mention} has been cleared.")

    @commands.command(hidden=True)
    async def scrape(self, ctx, cid):
        authorized = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
        if authorized:
            chan_name = self.bot.get_guild(config.GUILD_ID).get_channel(int(cid)).name
            await ctx.send("Archiving channel...")
            script_dir = os.path.dirname(__file__)
            working_dir = os.path.join(script_dir, os.pardir, "backups", chan_name)
            if not os.path.exists(working_dir):
                os.makedirs(working_dir)
            working_file = os.path.join(working_dir, "log.txt")
            f = open(working_file, "w")
            counter = 0
            mychan = self.bot.get_guild(config.GUILD_ID).get_channel(int(cid))
            async for message in mychan.history(limit=None):
                for file in message.attachments:
                    f.write(file.url)
                f.write(f"{message.created_at.strftime('[%x %X]')} {message.author.display_name}: {message.content}\n")
                counter += 1
            await ctx.send(f"Channel archived {counter} messages.")
            f.close()
            f = open(working_file, "r")
            s = f.readlines()
            f.close()
            f = open(working_file, "w")
            s.reverse()
            for item in s:
                f.write(item)
            f.close()
            await ctx.send("Archive generation complete.")

    @commands.command()
    async def report(self, ctx, *words):
        user = ctx.author.id
        contents = ""
        spam = 0
        for word in words:
            contents += word + " "
        contents = contents[:-1]
        now = datetime.utcnow()
        lister = (int(user),)
        c.execute("SELECT datetime from Reports WHERE uid = ?", lister)
        history = c.fetchall()
        if history:
            last_report = history[-1][0]
            print(last_report)
            last_report = datetime.strptime(last_report, '%m/%d/%y %H:%M:%S')
            diff = now - last_report
            if diff < timedelta(hours=2):
                await ctx.send("It's been less than two hours since your last report was submitted. Please slow down your submissions, or consider combining multiple reports into a single submission.")
                spam = 1
        if spam:
            pass
        else:
            listers = (int(user), contents, now.strftime("%m/%d/%y %H:%M:%S"))
            c.execute("INSERT INTO Reports(uid, contents, datetime) VALUES(?, ?, ?)", listers)
            await ctx.send("Report submitted successfully!")


def setup(bot):
    bot.add_cog(Misc(bot))
