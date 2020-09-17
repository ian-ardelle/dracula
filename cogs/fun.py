from discord.ext import commands
import lib.dbman as db
import discord
import chess
import random
import json


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ####################################
    # Chess - A multiplayer experience #
    ####################################
    @commands.command()
    async def chess_new(self, ctx):
        player = db.get_player_info(ctx.guild.id, ctx.author.id)
        players = db.get_all_players(ctx.guild.id)
        exist_check = 0
        for person in players:
            if person.get('chess') == ctx.channel.id:
                exist_check = 1
        if player.get('chess') == 0 and exist_check == 0:
            db.execute("UPDATE Characters SET chess = %s WHERE id = %s", (ctx.channel.id, player.get('id')),)
            await ctx.send("Game lobby created successfully.")

    @commands.command()
    async def chess_join(self, ctx):
        players = db.get_all_players(ctx.guild.id)
        for player in players:
            if player.get('chess') == ctx.channel.id:
                p1 = ctx.guild.get_member(player.get('player_id')).display_name
                p2 = ctx.author.display_name
                user = db.get_player_info(ctx.guild.id, ctx.author.id)
                await ctx.send(f"Game prepared in this channel for players: {p1} and {p2}.")
                db.execute("UPDATE Characters SET chess = %s WHERE id = %s", (ctx.channel.id, user.get('id')),)

    @commands.command()
    async def chess_leave(self, ctx):
        player = db.get_player_info(ctx.guild.id, ctx.author.id)
        db.execute("UPDATE Characters SET chess = 0 WHERE id = %s", (player.get('id'),))
        await ctx.send(f"{ctx.author.display_name} has been removed from the chess queue.")

    @commands.command()
    async def chess_start(self, ctx, white = 0):
        player = db.get_player_info(ctx.guild.id, ctx.author.id)
        p_list = db.get_all_players(ctx.guild.id)
        p1 = ctx.author.display_name
        if player.get('chess') == ctx.channel.id:
            for person in p_list:
                p2 = ctx.guild.get_member(player.get('player_id')).display_name
                if person.get('chess') == ctx.channel.id:
                    if white == 0:
                        white = random.randrange(1, 2, 1)
                    if white == 1:
                        await ctx.send(f"Starting game for {p1} and {p2}, {p1} to start as white.")
                    elif white == 2:
                        await ctx.send(f"Starting game for {p1} and {p2}, {p2} to start as white.")

    ##############
    # Moderation #
    ##############
    @commands.command()
    async def jail(self, ctx, member_id: discord.Member):
        member = ctx.guild.get_member(member_id)
        jail_log = open(f"jail_log_{ctx.guild.id}.json", "w+")
        old_log = json.load(jail_log)
        old_log[f"{member.id}"] = member.roles
        await member.edit(roles=[ctx.guild.default_role, ctx.guild.get_role(756212060441804811)])
        json.dump(old_log, jail_log)

    async def pardon(self, ctx, member_id: discord.Member):
        member = ctx.guild.get_member(member_id)
        jail_log = open(f"jail_log_{ctx.guild.id}.json", "w+")
        try:
            old_log = json.load(jail_log)
            old_roles = old_log[f"{member.id}"]
            await member.edit(roles=old_roles)
            old_log.pop(f"{member.id}")
        except KeyError:
            await ctx.send("Member is not jailed.")


def setup(bot):
    bot.add_cog(Fun(bot))
