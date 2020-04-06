from pytz import timezone
import pytz
from datetime import datetime
import config

cst = timezone('Pacific/Easter')
utc = pytz.utc


def ic_date():
    global utc_now
    utc_now = utc.localize(datetime.utcnow())
    global utcICCurrent
    utcICCurrent = utc.localize(config.IC_START_DATETIME) + (utc_now - utc.localize(config.IRL_START_DATETIME)) * config.DATE_COEFFICIENT
    if utcICCurrent >= utc_now:
        return utc_now.astimezone(cst).date().strftime("%A, %B %d, %Y")
    else:
        return utcICCurrent.astimezone(cst).strftime("%A, %B %d, %Y")


def ic_time():
    global utc_now
    utc_now = utc.localize(datetime.utcnow())
    global utcICCurrent
    utcICCurrent = utc.localize(config.IC_START_DATETIME) + (utc_now - utc.localize(config.IRL_START_DATETIME)) * config.DATE_COEFFICIENT
    global minutes_ic
    if utcICCurrent >= utc_now:
        global minutes_ic
        minutes_ic = utc_now.astimezone(cst).hour*60 + utc_now.astimezone(cst).minute
    else:
        minutes_ic = utcICCurrent.astimezone(cst).hour*60 + utcICCurrent.astimezone(cst).minute
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


def ic_datetime():
    global utc_now
    utc_now = utc.localize(datetime.utcnow())
    global utcICCurrent
    utcICCurrent = utc.localize(config.IC_START_DATETIME) + (utc_now - utc.localize(config.IRL_START_DATETIME)) * config.DATE_COEFFICIENT
    datetime_ic = datetime(utcICCurrent.year, utcICCurrent.month, utcICCurrent.day, int(ic_time()[0:2]), int(ic_time()[3:5]))
    return datetime_ic


def ic_datetime_utc():
    global utc_now
    utc_now = utc.localize(datetime.utcnow())
    global utcICCurrent
    utcICCurrent = utc.localize(config.IC_START_DATETIME) + (utc_now - utc.localize(config.IRL_START_DATETIME)) * config.DATE_COEFFICIENT
    if utcICCurrent >= utc_now:
        return utc_now
    else:
        return utcICCurrent
