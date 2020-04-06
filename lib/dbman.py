# dbman.py
# I decided to just make this an alias file as keeping SQL secure while defining custom commands is poopy
# Originally was meant to be a file which had commands and almost a microlanguage for adjusting values
# but that's way too complicated so it's just a way of now preventing us from reassigning c and conn
# in every function which uses sqlite3.

import sqlite3
import config

conn = sqlite3.connect(config.DB_PATH)
c = conn.cursor()
