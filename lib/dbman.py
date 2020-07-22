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

c = db.cursor(buffered=True)


def execute(query, params=''):
    if params:
        c.execute(query, params)
    else:
        c.execute(query)
    db.commit()


# def get_prefix(bot, message):
#    default_prefix = "!"
#    guild_id = message.guild.id
#    guild = get_guild_info(guild_id)
#    return guild.get('prefix', default_prefix)


def get_guild_list():
    c.execute("SELECT guild_id FROM Config")
    return c.fetchall()


def get_guild_info(guild_id):
    c.execute("SELECT * FROM Config WHERE guild_id = %s", (guild_id,))
    guild_info = c.fetchone()
    irl_raw = guild_info[4].decode('utf-8')
    ic_raw = guild_info[5].decode('utf-8')
    irl_start = datetime(int(irl_raw[0:4]), int(irl_raw[5:7]), int(irl_raw[8:10]), int(irl_raw[11:13]), int(irl_raw[14:16]))
    ic_start = datetime(int(ic_raw[0:4]), int(ic_raw[5:7]), int(ic_raw[8:10]), int(ic_raw[11:13]), int(ic_raw[14:16]))
    return dict(id=guild_info[0], guild_id=guild_info[1], prefix=guild_info[2], date_coefficient=guild_info[3], ic_start=ic_start, irl_start=irl_start,
                tz=timezone(guild_info[6]), date_chan=guild_info[7], feeding_chan=guild_info[8],
                st_alerts_chan=guild_info[9], announcements_chan=guild_info[10], st_id=guild_info[11],
                narrator_id=guild_info[12], bb_id=guild_info[13], player_role=guild_info[14],
                stakes=guild_info[15], exploding_toggle=guild_info[16],
                last_date=datetime.strptime(guild_info[17].decode('utf-8'), "%Y:%m:%d").date())


def get_player_info(guild_id, player_id):
    g_id = get_guild_info(guild_id).get("id")
    c.execute("SELECT * FROM Characters WHERE guild_id = %s AND player_id = %s", (g_id, player_id))
    player = c.fetchone()
    if player[7] != ' ':
        raw = player[7].decode('utf-8')
        upkeep_dt = datetime(int(raw[0:4]), int(raw[5:7]), int(raw[8:10]), int(raw[11:13]), int(raw[14:16]), int(raw[17:19]))
    else:
        upkeep_dt = ' '
    formatted_player = dict(id=player[0], player_id=player[1], bp_max=player[2], bp=player[3], wp_max=player[4], wp=player[5], upkeep=player[6], upkeep_date=upkeep_dt, agg_dmg=player[8], alert_flag=player[9], guild_id=player[10])
    return formatted_player


def get_all_players(guild_id):
    guild = get_guild_info(guild_id)
    c.execute("SELECT * FROM Characters WHERE guild_id = %s", (guild.get('id'),))
    player_list = c.fetchall()
    formatted_player_list = []
    for player in player_list:
        if player[7] != ' ':
            raw = player[7].decode('utf-8')
            upkeep_dt = datetime(int(raw[0:4]), int(raw[5:7]), int(raw[8:10]), int(raw[11:13]),
                                 int(raw[14:16]), int(raw[17:19]))
        else:
            upkeep_dt = ' '
        formatted_player = dict(id=player[0], player_id=player[1], bp_max=player[2], bp=player[3], wp_max=player[4], wp=player[5], upkeep=player[6], upkeep_date=upkeep_dt, agg_dmg=player[8], alert_flag=player[9], guild_id=player[10])
        formatted_player_list.append(formatted_player)
    return formatted_player_list
