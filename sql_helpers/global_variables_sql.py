# global variables will be assigned here
# can be imported in any module to make life easier.
from sample_config import Config
LOGGER = Config.PRIVATE_GROUP_BOT_API_ID
BLACKLIST = Config.UB_BLACK_LIST_CHAT
SUDO_USERS = Config.SUDO_USERS
PACK_NAME = Config.PACK_NAME
ANIM_PACK_NAME = Config.ANIM_PACK_NAME
DEPLOYLINK = Config.HEROKU_LINK
REPOLINK = Config.REPO_LINK
PACKS = Config.PACKS_CONTENT
# add modules to this list using MODULES_LIST.append(MODULE_NAME)
# add syntax to this dictionary using SYNTAX.update
SYNTAX = {}
MODULE_LIST=[]