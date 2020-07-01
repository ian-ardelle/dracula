from discord.ext import commands
import pathlib
import lib.dbman as db
import discord
import aiohttp
import aiofiles
from PIL import Image
from datetime import datetime, timedelta


def mkdir(directory):
    print("Check 1")
    if not directory.exists:
        directory.mkdir()
        print("Check 2")


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

    @commands.command(hidden=True)
    async def scrape(self, ctx, cid):
        counter = 0
        guild_name = ctx.guild.name
        chan_name = ctx.guild.get_channel(int(cid)).name
        await ctx.send("Archiving channel...")
        working_dir = pathlib.Path.cwd() / "backups" / guild_name
        mkdir(working_dir)
        working_dir = pathlib.Path.cwd() / "backups" / guild_name / chan_name
        mkdir(working_dir)
        print("ChecK 3")
        working_file = working_dir / "log.txt"
        f = open(working_file, "w")
        mychan = ctx.guild.get_channel(int(cid))
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
    async def scrape_all(self, ctx):
        authorized = False
        guild = db.get_guild_info(ctx.guild.id)
        for role in ctx.author.roles:
            if guild.get("st_id") == role.id:
                authorized = True
        if authorized:
            await ctx.send("Archiving server...")
            for chan in ctx.guild.text_channels:
                if chan == ctx.channel:
                    continue
                else:
                    guild_dir = pathlib.Path.cwd() / "archive" / ctx.guild.name
                    mkdir(guild_dir)
                    chan_name = chan.name
                    if chan.category:
                        category_dir = pathlib.Path.cwd() / "archive" / ctx.guild.name / chan.category.name
                        mkdir(category_dir)
                        working_dir = pathlib.Path.cwd() / "archive" / ctx.guild.name / chan.category.name / chan_name
                    else:
                        working_dir = pathlib.Path.cwd() / "archive" / ctx.guild.name / chan_name
                    mkdir(working_dir)
                    working_file = working_dir / "log.txt"
                    f = open(working_file, "w")
                    counter = 0
                    async for message in chan.history(limit=None):
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
            await ctx.send("Server archive complete.")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member):
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
        ava_img.unlink()

    @commands.command(hidden=True)
    async def stake(self, ctx):
        guild = db.get_guild_info(ctx.guild.id)
        counter = guild.get("stakes")
        db.execute("UPDATE Config SET stakes = %s WHERE id = %s", (counter + 1, guild.get("id")))
        await ctx.send(f"*Gets frozen in place.* **Dracula has been staked: {counter + 1} times!**")

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


def setup(bot):
    bot.add_cog(Misc(bot))
