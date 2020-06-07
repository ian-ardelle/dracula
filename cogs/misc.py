from discord.ext import commands
import config
import pathlib
from lib.dbman import c, conn
import discord
import aiohttp
import aiofiles
from PIL import Image
import random
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
            await ctx.author.send(message)

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
            await ctx.send(f"Auction for {member.mention} has been cleared.")'''

    @commands.command(hidden=True)
    async def scrape(self, ctx, cid):
        chan_name = self.bot.get_guild(config.GUILD_ID).get_channel(int(cid)).name
        await ctx.send("Archiving channel...")
        working_dir = pathlib.Path.cwd() / "backups" / chan_name
        if not working_dir.exists():
            working_dir.mkdir()
        working_file = working_dir / "log.txt"
        f = open(working_file, "w")
        counter = 0
        mychan = self.bot.get_guild(config.GUILD_ID).get_channel(int(cid))
        async for message in mychan.history(limit=None):
            for file in message.attachments:
                f.write(file.url)
            f.write(
                f"{message.created_at.strftime('[%x %X]')} {message.author.display_name}: {message.clean_content}\n")
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
        await ctx.send("Archive generation complete: " + chan_name, file=discord.File(working_file))

    @commands.command(hidden=True)
    async def chan_ids(self, ctx, server_id):
        chan_str = ""
        chan_list = self.bot.get_guild(int(server_id)).channels
        for chan in chan_list:
            chan_str += chan.name + " - " + str(chan.id) + "\n"
        chan_len = len(chan_str)
        msg_num = chan_len / 2000
        x = 0
        while x < msg_num:
            await ctx.send(chan_str[2000*(x-1):2000*x])
            x += 1


    @commands.command(hidden=True)
    async def scrape_all(self, ctx):
        authorized = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
        if authorized:
            await ctx.send("Archiving server...")
            for chan in self.bot.get_guild(config.GUILD_ID).text_channels:
                if chan == ctx.channel:
                    continue
                else:
                    chan_name = chan.name
                    if chan.category:
                        category_dir = pathlib.Path.cwd() / "archive" / chan.category.name
                        if not category_dir.exists():
                            category_dir.mkdir()
                        working_dir = pathlib.Path.cwd() / "archive" / chan.category.name / chan_name
                    else:
                        working_dir = pathlib.Path.cwd() / "archive" / chan_name
                    if not working_dir.exists():
                        working_dir.mkdir()
                    working_file = working_dir / "log.txt"
                    f = open(working_file, "w")
                    counter = 0
                    async for message in chan.history(limit=None):
                        for file in message.attachments:
                            f.write(file.url)
                        f.write(f"{message.created_at.strftime('[%x %X]')} {message.author.display_name}: {message.clean_content}\n")
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
                    await ctx.send("Archive generation complete: " + chan_name, file=discord.File(working_file))
            await ctx.send("Server archive complete.")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member):
        url = str(member.avatar_url)
        filename = url.split("/")[-1]
        filename = filename.split("?")[0]  # cleans up the file name so it removes trailing ? symbols and has correct extension

        async with aiohttp.ClientSession() as image:
            async with image.get(url) as ava:
                if ava.status == 200:
                    avatar = await aiofiles.open(pathlib.Path.cwd() / filename, mode='wb')
                    await avatar.write(await ava.read())
                    await avatar.close()
        ava_img = pathlib.Path.cwd() / filename
        if member.is_avatar_animated():
            await ctx.send(file=discord.File(ava_img))
        else:
            ava_new = pathlib.Path.cwd() / (filename + ".png")
            ava_edit = Image.open(ava_img)
            ava_edit.save(ava_new)
            await ctx.send(file=discord.File(ava_new))
            ava_new.unlink()
        ava_img.unlink()

    '''@commands.command()
    async def caption(self, ctx, member: discord.Member, *words):
        url = str(member.avatar_url)
        filename = url.split("/")[-1]
        filename = filename.split("?")[
            0]  # cleans up the file name so it removes trailing ? symbols and has correct extension

        async with aiohttp.ClientSession() as image:
            async with image.get(url) as ava:
                if ava.status == 200:
                    avatar = await aiofiles.open(pathlib.Path.cwd() / filename, mode='wb')
                    await avatar.write(await ava.read())
                    await avatar.close()
        ava_img = pathlib.Path.cwd() / filename
        if member.is_avatar_animated():
            await ctx.send(file=discord.File(ava_img))
        else:
            ava_new = pathlib.Path.cwd() / (filename + ".png")
            ava_edit = Image.open(ava_img)
            ava_edit.save(ava_new)
            await ctx.send(file=discord.File(ava_new))
            ava_new.unlink()
        ava_img.unlink()'''

    @commands.command()
    async def st_gen(self, ctx):
        authorized = False
        for role in ctx.author.roles:
            if config.ST_ROLE == role.id:
                authorized = True
        if authorized:
            raw_user_list = ctx.guild.members
            user_list = []
            st_list = []
            for user in raw_user_list:
                if not user.bot:
                    user_list.append(user.id)
                for role in user.roles:
                    if role.id == config.ST_ROLE:
                        st_list.append(user.id)
                        user_list.remove(user.id)
                    elif role.name == "On Hiatus":
                        user_list.remove(user.id)
                    elif role.name == "Under construction":
                        user_list.remove(user.id)
                if not user.roles:
                    user_list.remove(user.id)

            quality_check = 0
            message = ""
            while quality_check == 0:
                message = ""
                quality_check = 1
                random_st = random.sample(range(0, len(st_list)), len(st_list))
                for st in st_list:
                    st_i = st_list.index(st)
                    user_i = random_st[st_i]
                    if st_i == user_i:
                        quality_check = 0
                    message += ctx.guild.get_member(st).mention + "'s victims:"
                    message += "\n" + ctx.guild.get_member(st_list[user_i]).mention
                    message += "~/~/~"
            msg = message.split("~/~/~")
            random_raw = random.sample(range(0, len(user_list)), len(user_list))
            user_rand = []
            for index in random_raw:
                user_rand.append(user_list[index])
            for user in user_rand:
                st_index = user_rand.index(user) % len(st_list)
                msg[st_index] += "\n" + ctx.guild.get_member(user).mention
            for mess in msg:
                if mess != "":
                    await ctx.send(mess)

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
            conn.commit()
            await ctx.send("Report submitted successfully!")

    @commands.command()
    async def feedback(self, ctx, *words):
        user = ctx.author.id
        contents = ""
        spam = 0
        for word in words:
            contents += word + " "
        contents = contents[:-1]
        lister = (int(user),)
        c.execute("SELECT * from Feedback WHERE uid = ?", lister)
        history = c.fetchall()
        if history:
            spam = 1
        if spam:
            await ctx.send("You have already submitted feedback on this poll / query.")
        else:
            lister = (int(user),)
            c.execute("INSERT INTO Feedback(uid) VALUES(?)", lister)
            conn.commit()
            await ctx.send("Report submitted successfully!")
            await self.bot.get_channel(708369926850871298).send(contents)

    '''@commands.command()
    async def view_reports(self, ctx, ):'''


def setup(bot):
    bot.add_cog(Misc(bot))
