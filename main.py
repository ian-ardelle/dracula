# main.py
# This is the main engine behind dracula
# First, the bot is object is declared by discord.ext.py specs
# Then it loads up the 'cogs', which are basically imports
# which are meant specifically to work with discord.ext.py bot objects
# Finally, under the @bot.event decorator, it produces a greeting message,
# both to Discord and to the console and initializes the bot
from discord.ext import commands
import config
import discord
from lib.dbman import c, conn

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, description="Dracula the Discord Daemon")

initial_extensions = ["cogs.dice",
                      "cogs.schedule",
                      "cogs.faq",
                      "cogs.whois",
                      "cogs.bnw",
                      "cogs.ar",
                      "cogs.misc"]

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n")
    await bot.change_presence(activity=discord.Game(name="Crossroads: A Vampire Chronicle"))
    print(f"Successfully logged in and booted!")
    c.execute("CREATE TABLE IF NOT EXISTS Faq (Listing text NOT NULL, Contents text)")
    c.execute("CREATE TABLE IF NOT EXISTS Ar (Listing text NOT NULL, Contents text)")
    c.execute("CREATE TABLE IF NOT EXISTS NHBnW (player_id int, bp int, bp_max int, wp int, wp_max int, agg_dmg int, active_toggle bit, upkeep int, upkeep_date text, alert_flag bit)")
    c.execute("CREATE TABLE IF NOT EXISTS SecretSanta (sender_id int, receiver_id int)")
    c.execute("CREATE TABLE IF NOT EXISTS Auction (auctioned int, bidder int, bid int, active bit)")
    c.execute("CREATE TABLE IF NOT EXISTS Reports (id INTEGER PRIMARY KEY, uid int, contents text, datetime text)")
    conn.commit()
    await bot.get_channel(config.BOT_ANNOUNCEMENTS_CHANNEL).send("Drac's back, baby!")

bot.run(config.DISCORD_API_KEY, bot=True, reconnect=True)
