# main.py
# This is the main engine behind dracula
# First, the bot is object is declared by discord.ext.py specs
# Then it loads up the 'cogs', which are basically imports
# which are meant specifically to work with discord.ext.py bot objects
# Finally, under the @bot.event decorator, it produces a greeting message,
# both to Discord and to the console and initializes the bot
from discord.ext import commands
import lib.dbman as db
import discord
import config

############################################################
# Removed config file, implemented constants in its place. #
############################################################

DISCORD_BOT_TOKEN = config.DISCORD_BOT_TOKEN


bot = commands.Bot(command_prefix="$", description="Dracula the Discord Daemon")


initial_extensions = ["cogs.dice", "cogs.schedule", "cogs.bnw", "cogs.misc", "cogs.fun"]

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(
        f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n"
    )
    await bot.change_presence(activity=discord.Game(name="Vampire: The Masquerade"))
    print(f"Successfully logged in and booted!")


bot.run(DISCORD_BOT_TOKEN, bot=True, reconnect=True)
