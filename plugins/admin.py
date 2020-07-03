# For The-TG-Bot-3.0
# Syntax (.pin <loud (optional)>, .promote <optional_rank>, .demote, .ban, .unban, .mute, .unmute, .kick as a reply to a user's msg)

from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights
from datetime import datetime
import sys
from userbot import syntax

@bot.on(command("pin ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    silent = True
    cmd = event.pattern_match.group(0)
    if "ping" in cmd:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "loud":
        silent = False
    if event.message.reply_to_msg_id is not None:
        message_id = event.message.reply_to_msg_id
        try:
            await bot(UpdatePinnedMessageRequest(
                event.chat_id,
                message_id,
                silent
            ))
        except Exception as e:
            await event.edit(str(e))
        else:
            await event.delete()
    else:
        await event.edit("Reply to a message to pin it.")

@bot.on(command(pattern="promote ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str != "":
        admin_rank = input_str
    else:
        admin_rank = "admeme"
    start = datetime.now()
    to_promote_id = None
    rights = ChatAdminRights(
        change_info=True,
        post_messages=True,
        edit_messages=True,
        delete_messages=True,
        ban_users=False,
        invite_users=True,
        pin_messages=True,
        add_admins=False
    )
    reply_msg_id = event.message.id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_promote_id = r_mesg.sender_id
    try:
        await bot(EditAdminRequest(event.chat_id, to_promote_id, rights, admin_rank))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"Say hello to ```{to_promote_id}```, our new admeme!")


banned_rights = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)


@bot.on(command("(ban) ?(.*)"))
async def _(event):

    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "ban":
        rights = banned_rights

    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    if to_ban_id in Config.SUDO_USERS:
        await event.edit("**Wait! WHAT?!\nDid you just try to ban my creator?!?!\nBYE!**")
        sys.exit()
    else:
        try:
            await bot(EditBannedRequest(event.chat_id, to_ban_id, rights))
        except (Exception) as exc:
            await event.edit(str(exc))
        else:
            await event.edit(f"Gone, ```{to_ban_id}``` is gone!")


demoted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=True,
    send_gifs=None,
    send_games=True,
    send_inline=None,
    embed_links=None
)


@bot.on(command("(demote) ?(.*)"))
async def _(event):

    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "demote":
        rights = demoted_rights

    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    if to_ban_id in Config.SUDO_USERS:
        await event.edit("**Wait! WHAT?!\nDid you just try to demote my creator?!?!\nBYE!**")
        sys.exit()
    else:
        try:
            await bot(EditBannedRequest(event.chat_id, to_ban_id, rights))
        except (Exception) as exc:
            await event.edit(str(exc))
        else:
            await event.edit(f"Oh boy, ```{to_ban_id}``` has been demoted!")

muted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)


@bot.on(command("(mute) ?(.*)"))
async def _(event):

    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "mute":
        rights = muted_rights

    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    if to_ban_id in Config.SUDO_USERS:
        await event.edit("**Wait! WHAT?!\nDid you just try to mute my creator?!?!\nBYE!**")
        sys.exit()
    else:
        try:
            await bot(EditBannedRequest(event.chat_id, to_ban_id, rights))
        except (Exception) as exc:
            await event.edit(str(exc))
        else:
            await event.edit(f"Successfully taped ```{to_ban_id}```!")


unmuted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None
)


@bot.on(command("(unmute) ?(.*)"))
async def _(event):
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".unban"
    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "unmute":
        rights = unmuted_rights

    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False

    try:
        await bot(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"Okay, ```{to_ban_id}``` is no longer taped!")

unbanned_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None
)


@bot.on(command("(unban) ?(.*)"))
async def _(event):

    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "unban":
        rights = unbanned_rights

    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    try:
        await bot(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"Well, ```{to_ban_id}``` can join now!")

kicked_rights1 = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

kicked_rights2 = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None
)


@bot.on(command("(kick) ?(.*)"))
async def _(event):

    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "kick":
        rights = kicked_rights1
        rights2 = kicked_rights2
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    if to_ban_id in Config.SUDO_USERS:
        await event.edit("**Wait! WHAT?!\nDid you just try to kick my creator?!?!\nBYE!**")
        sys.exit()
    else:
        try:
            await bot(EditBannedRequest(event.chat_id, to_ban_id, rights))
        except (Exception) as exc:
            await event.edit(str(exc))
        try:
            await bot(EditBannedRequest(event.chat_id, to_ban_id, rights2))
        except (Exception) as exc:
            await event.edit(str(exc))
        else:
            await event.edit(f"```{to_ban_id}``` has been yeeted!")

syntax.update({
    "admin": "\
```.ban <userid>``` (or as a reply to a message of targer user)\
\nUsage: bans target user.\
\n\n```.unban <userid>``` (or as a reply to a message of targer user)\
\nUsage: unbans target user.\
\n\n```.mute <userid>``` (or as a reply to a message of targer user)\
\nUsage: mutes target user.\
\n\n```.unmute <userid>``` (or as a reply to a message of targer user)\
\nUsage: unmutes target user.\
\n\n```.promote <optional_rank>``` (must be a reply to a message of targer user)\
\nUsage: promotes target user.\
\n\n```.demote <userid>``` (or as a reply to a message of targer user)\
\nUsage: demotes target user.\
\n\n```.kick <userid>``` (or as a reply to a message of targer user)\
\nUsage: kicks target user.\
\n\n```.pin``` (as a reply to a message)\
\nUsage: pins target msg.\
"
})
