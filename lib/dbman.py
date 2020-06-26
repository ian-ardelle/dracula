# dbman.py
# I decided to just make this an alias file as keeping SQL secure while defining custom commands is poopy
# Originally was meant to be a file which had commands and almost a microlanguage for adjusting values
# but that's way too complicated so it's just a way of now preventing us from reassigning c and conn
# in every function which uses sqlite3.

import mysql.connector as mysql
from datetime import datetime
from pytz import timezone

db = mysql.connect(
    host="localhost",
    user="drac",
    passwd="F1v3B0r0ugh$",
    database="Dracula"
)

c = db.cursor()


def tuple_to_dict(tup):
    dictionary = {}
    for a, b in tup:
        dictionary.setdefault(a,).append(b)
    return dictionary


def get_prefix(bot, message):
    default_prefix = "!"
    guild_id = message.guild.id
    c.execute("SELECT guild_id, prefix FROM Config")
    prefix_tuple = c.fetchall()
    return tuple_to_dict(prefix_tuple).get(guild_id, default_prefix)


def get_guild_list():
    db.c.execute("SELECT guild_id FROM Config")
    return db.c.fetchall()


def get_guild_info(guild_id):
    db.c.execute("SELECT * FROM Config WHERE guild_id = %d", guild_id)
    guild_info = db.c.fetchone()
    ic_start = datetime(int(guild_info[4][0:4]), int(guild_info[4][5:7]), int(guild_info[4][8:10]), int(guild_info[4][11:13]), int(guild_info[4][14:16]))
    irl_start = datetime(int(guild_info[5][0:4]), int(guild_info[5][5:7]), int(guild_info[5][8:10]), int(guild_info[5][11:13]), int(guild_info[5][14:16]))
    return {"id": guild_info[0], "date_coefficient": guild_info[3], "ic_start": ic_start,
            "irl_start": irl_start, "tz": timezone(guild_info[6]), "date_chan": guild_info[7], "feeding_chan": guild_info[8],
            "st_alerts_chan": guild_info[9], "announcements_chan": guild_info[10], "st_id": guild_info[11],
            "narrator_id": guild_info[12], "bloodbag_id": guild_info[13], "player_role": guild_info[14],
            "stakes": guild_info[15], "empty_bp_message": guild_info[16], "exploding_toggle": guild_info[17],
            "last_date": datetime.strptime(guild_info[18], "%Y:%m:%d:%H:%M:%S")}


def get_player_info(guild_id, player_id):
    g_id = get_guild_info(guild_id).get("id")
    db.c.execute("SELECT * FROM Characters WHERE guild_id = %d AND player_id = %d", g_id, player_id)
    player = db.c.fetchone()
    formatted_player = {"id": player[0], "player_id": player[1], "bp_max": player[2], "bp": player[3],
                        "wp_max": player[4], "wp": player[5], "upkeep": player[6], "upkeep_date": player[7],
                        "guild_id": player[8]}
    return formatted_player


def get_all_players(guild_id):
    db.c.execute("SELECT * FROM Characters")
    player_list = db.c.fetchall()
    formatted_player_list = []
    for player in player_list:
        formatted_player = {"id": player[0], "player_id": player[1], "bp_max": player[2], "bp": player[3],
                            "wp_max": player[4], "wp": player[5], "upkeep": player[6], "upkeep_date": player[7],
                            "guild_id": player[8]}
        formatted_player_list.append(formatted_player)
    return formatted_player_list
