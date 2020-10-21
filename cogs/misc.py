from discord.ext import commands
import pathlib
import lib.dbman as db
import discord
import aiohttp
import aiofiles
from PIL import Image
from datetime import datetime, timedelta
from lib import time


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def moon_cycle(self, ctx):
        ##################################################################
        # Start by calculating number of lunar cycles that have passed   #
        # via Julian Day number conversion of the current IC date, then  #
        # evaluate the corresponding moon cycle by taking the difference #
        # from a known date for a New Moon.                              #
        ##################################################################
        ic_date = time.ic_datetime(ctx.guild.id)
        jd_a = int(ic_date.year / 100)
        jd_b = int(jd_a / 4)
        jd_c = 2 - jd_a + jd_b
        jd_e = int(365.25 * (ic_date.year + 4716))
        jd_f = int(30.6001 * (ic_date.month + 1))
        jd = jd_c + ic_date.day + jd_e + jd_f - 1524.5
        cycle_days = jd % 29.53
        if cycle_days <= 1 or cycle_days > 28.5:
            moon_cycle = "New Moon"
        elif 1 < cycle_days <= 6:
            moon_cycle = "Waxing Crescent"
        elif 6 < cycle_days <= 8:
            moon_cycle = "First Quarter"
        elif 8 < cycle_days <= 14:
            moon_cycle = "Waxing Gibbous"
        elif 14 < cycle_days <= 16:
            moon_cycle = "Full Moon"
        elif 16 < cycle_days <= 21:
            moon_cycle = "Waning Gibbous"
        elif 21 < cycle_days <= 23:
            moon_cycle = "Third Quarter"
        elif 23 < cycle_days <= 28.5:
            moon_cycle = "Waning Crescent"
        await ctx.send(f"The current moon cycle is: {moon_cycle}.")

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
        working_dir = pathlib.Path.cwd() / "backups"
        if not working_dir.exists():
            working_dir.mkdir()
        guild_dir = pathlib.Path.cwd() / "backups" / guild_name
        if not guild_dir.exists():
            guild_dir.mkdir()
        chan_name = ctx.guild.get_channel(int(cid)).name
        await ctx.send("Archiving channel...")
        working_dir = pathlib.Path.cwd() / "backups" / guild_name / chan_name
        if not working_dir.exists():
            working_dir.mkdir()
        working_file = working_dir / "log.txt"
        f = open(working_file, "w")
        mychan = ctx.guild.get_channel(int(cid))
        async for message in mychan.history(limit=None):
            for file in message.attachments:
                f.write(file.url)
            f.write(
                f"{message.created_at.strftime('[%x %X]')} {message.author.display_name}: {message.clean_content}\n"
            )
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
        await ctx.send(
            "Archive generation complete: " + chan_name, file=discord.File(working_file)
        )

    @commands.command(hidden=True)
    async def scrape_all(self, ctx):
        authorized = False
        guild = db.get_guild_info(ctx.guild.id)
        for role in ctx.author.roles:
            if guild.get("st_id") == role.id:
                authorized = True
        if authorized:
            await ctx.send("Archiving server...")
            guild_name = ctx.guild.name
            guild_dir = pathlib.Path.cwd() / "archive" / guild_name
            if not guild_dir.exists():
                guild_dir.mkdir()
            for chan in ctx.guild.text_channels:
                if chan == ctx.channel:
                    continue
                else:
                    chan_name = chan.name
                    if chan.category:
                        category_dir = (
                            pathlib.Path.cwd()
                            / "archive"
                            / ctx.guild.name
                            / chan.category.name
                        )
                        if not category_dir.exists():
                            category_dir.mkdir()
                        working_dir = (
                            pathlib.Path.cwd()
                            / "archive"
                            / ctx.guild.name
                            / chan.category.name
                            / chan_name
                        )
                    else:
                        working_dir = (
                            pathlib.Path.cwd() / "archive" / ctx.guild.name / chan_name
                        )
                    if not working_dir.exists():
                        working_dir.mkdir()
                    working_file = working_dir / "log.txt"
                    f = open(working_file, "w")
                    counter = 0
                    async for message in chan.history(limit=None):
                        for file in message.attachments:
                            f.write(file.url)
                        f.write(
                            f"{message.created_at.strftime('[%x %X]')} {message.author.display_name}: {message.clean_content}\n"
                        )
                        counter += 1
                    await ctx.send(f"Channel {chan_name} archived {counter} messages.")
                    f.close()
                    f = open(working_file, "r")
                    s = f.readlines()
                    f.close()
                    f = open(working_file, "w")
                    s.reverse()
                    for item in s:
                        f.write(item)
                    f.close()
            await ctx.send("Server archive complete.")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member):
        url = str(member.avatar_url)
        filename = url.split("/")[-1]
        filename = filename.split("?")[
            0
        ]  # cleans up the file name so it removes trailing ? symbols and has correct extension

        async with aiohttp.ClientSession() as image:
            async with image.get(url) as ava:
                if ava.status == 200:
                    avatar = await aiofiles.open(
                        pathlib.Path.cwd() / filename, mode="wb"
                    )
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
        db.execute(
            "UPDATE Config SET stakes = %s WHERE id = %s",
            (counter + 1, guild.get("id")),
        )
        await ctx.send(
            f"*Gets frozen in place.* **Dracula has been staked: {counter + 1} times!**"
        )

    """@commands.command()
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
        ava_img.unlink()"""

    @commands.command()
    async def echo(self, ctx, channel, *words):
        message = ""
        for word in words:
            message = message + word + ' '
        await self.bot.get_channel(int(channel)).send(message[:-1])

    @commands.command()
    async def chan_lookup(self, ctx, guild, series_start):
        message = ""
        chan_list = self.bot.get_guild(int(guild)).channels
        chan_list_smol = chan_list[int(series_start)-1:int(series_start)+49]
        for channel in chan_list_smol:
            message = message + channel.name + " - " + channel.id
        ctx.send(message[:-1])


def setup(bot):
    bot.add_cog(Misc(bot))
