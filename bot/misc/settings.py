from bot.misc.env import DB

#####################
#     ALL ROLE      #
#####################

ROLE = [(1, "ADMIN"), (2, "SUPERVISOR"), (3, "MANAGER"), (4, "USER")]
ACCESS = [(1, "HEAD_MANAGER"), (2, "LTD_MANAGER"), (3, "ADDRESS_MANAGER")]


#####################
# DATABASE SETTINGS #
#####################


SETTING_DB = DB().get_setting("postgres")

