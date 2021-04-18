import lib.dbman as db


def auth_check_st(guild, roles):
    st_only = True
    return auth_check(guild, roles, st_only)


def auth_check_st_nar(guild, roles):
    st_only = False
    return auth_check(guild, roles, st_only)


def auth_check(guild, roles, st_only):
    authorized = False
    for role in roles:
        if (st_only and guild.get("st_id") == role.id) or \
                (not st_only and (role.id == (guild.get("st_id") or (guild.get("narrator_id"))))):
            authorized = True
    return authorized
