# For UniBorg
# By Priyam Kalra

from uniborg.util import admin_cmd
from telethon.tl import functions, types
import time
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("log")
MODULE_LIST.append("msg")


@borg.on(admin_cmd(pattern="log ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    rep = await event.get_reply_message()
    msg = rep.text
    await log(msg)
    await event.delete()


@borg.on(admin_cmd(pattern="msg ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    chat = event.pattern_match.group(1)
    rep = await event.get_reply_message()
    msg = rep.text
    await borg.send_message(chat, msg)
    await event.delete()


async def log(text):
    LOGGER = Config.PRIVATE_GROUP_BOT_API_ID
    await borg.send_message(LOGGER, text)

SYNTAX.update({
    "log": "\
**Requested Module --> log**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.log (as a reply to target message)```\
\nUsage:  Simply log the replied msg to logger group.\
"
})

SYNTAX.update({
    "msg": "\
**Requested Module --> msg**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.msg <chat_id> (as a reply to target message)```\
\nUsage:  Send a message to another chat.\
\nTip: This is useful for professional channel broadcasts.\
"
})
