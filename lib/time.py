from pytz import timezone
import pytz
from datetime import datetime
import lib.dbman as db

est = timezone('America/New_York')
cst = timezone('America/Chicago')
utc = pytz.utc


def ic_date(guild_id):
    time_info = db.get_guild_info(guild_id)
    utc_now = utc.localize(datetime.utcnow())
    utcICCurrent = utc.localize(time_info.get("ic_start")) + (utc_now - utc.localize(time_info.get("irl_start"))) * time_info.get("date_coefficient")
    return utcICCurrent.astimezone(time_info.get("tz")).strftime("%A, %B %d, %Y")


def ic_time(guild_id):
    time_info = db.get_guild_info(guild_id)
    utc_now = utc.localize(datetime.utcnow())
    utcICCurrent = utc.localize(time_info.get("ic_start")) + (utc_now - utc.localize(time_info.get("irl_start"))) * time_info.get("date_coefficient")
    if utcICCurrent >= utc_now:
        minutes_ic = utc_now.astimezone(time_info.get("tz")).hour*60 + utc_now.astimezone(time_info.get("tz")).minute
    else:
        minutes_ic = utcICCurrent.astimezone(time_info.get("tz")).hour*60 + utcICCurrent.astimezone(time_info.get("tz")).minute
    minutes_ic = minutes_ic / 2  # we're only operating on 12 hours of time now, so we divide the time by 2

    if minutes_ic > 420:  # if the time is past 7am...
        minutes_ic += 720  # add 12 hours

    hours_ic = int(minutes_ic / 60)
    minutes_ic = int(minutes_ic % 60)

    if hours_ic == 0:
        hours_ic += 12
        return f"{hours_ic:02d}:{minutes_ic:02d} AM"
    elif hours_ic > 12:
        return f"{hours_ic - 12:02d}:{minutes_ic:02d} PM"
    else:
        return f"{hours_ic:02d}:{minutes_ic:02d} AM"


def ic_datetime(guild_id):
    time_info = db.get_guild_info(guild_id)
    utc_now = utc.localize(datetime.utcnow())
    utcICCurrent = utc.localize(time_info.get("ic_start")) + (utc_now - utc.localize(time_info.get("irl_start"))) * time_info.get("tz")
    datetime_ic = datetime(utcICCurrent.year, utcICCurrent.month, utcICCurrent.day, int(ic_time()[0:2]), int(ic_time()[3:5]))
    return datetime_ic


def ic_datetime_utc(guild_id):
    time_info = db.get_guild_info(guild_id)
    utc_now = utc.localize(datetime.utcnow())
    utcICCurrent = utc.localize(time_info.get("ic_start")) + (utc_now - utc.localize(time_info.get("irl_start"))) * time_info.get("tz")
    return utcICCurrent
