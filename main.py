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

############################################################
# Removed config file, implemented constants in its place. #
############################################################

print(db.get_guild_info(db.get_guild_list()[0][0]).get('announcements_channel'))

DISCORD_API_KEY = "NTc1MDk0NjEyMzEwMzYwMDg2.XPyMmg.bBhJKtQ9-PrsDTuS1hyoBvnJHxM"

bot = commands.Bot(command_prefix=db.get_prefix, description="Dracula the Discord Daemon")

initial_extensions = ["cogs.dice",
                      "cogs.schedule",
                      "cogs.bnw",
                      "cogs.misc"]

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n")
    await bot.change_presence(activity=discord.Game(name="Vampire: The Masquerade"))
    print(f"Successfully logged in and booted!")
    for guild in db.get_guild_list():
        await bot.get_channel(db.get_guild_info(guild[0]).get("announcements_channel")).send("Drac's back, baby!")

bot.run(DISCORD_API_KEY, bot=True, reconnect=True)
