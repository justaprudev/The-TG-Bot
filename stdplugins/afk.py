# For UniBorg
# Syntax (.afk <optional reason>)"
import asyncio
import datetime
from telethon import events
from telethon.tl import functions, types
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST


borg.storage.USER_AFK = {}  # pylint:disable=E0602
borg.storage.afk_time = None  # pylint:disable=E0602
borg.storage.last_afk_message = {}  # pylint:disable=E0602

MODULE_LIST.append("afk")

@borg.on(events.NewMessage(outgoing=True))  # pylint:disable=E0602
async def set_not_afk(event):
    current_message = event.message.message
    if ".afk" not in current_message and "yes" in borg.storage.USER_AFK:  # pylint:disable=E0602
        try:
            status = "Set AFK mode to False"
            await log(status)
        except Exception as e:  # pylint:disable=C0103,W0703
            await borg.send_message(  # pylint:disable=E0602
                event.chat_id,
                "Please set `PRIVATE_GROUP_BOT_API_ID` " + \
                "for the proper functioning of afk functionality " + \
                "in @UniBorg\n\n `{}`".format(str(e)),
                reply_to=event.message.id,
                silent=True
            )
        borg.storage.USER_AFK = {}  # pylint:disable=E0602
        borg.storage.afk_time = None  # pylint:disable=E0602


@borg.on(events.NewMessage(pattern=r"\.afk ?(.*)", outgoing=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if not borg.storage.USER_AFK:  # pylint:disable=E0602
        last_seen_status = await borg(  # pylint:disable=E0602
            functions.account.GetPrivacyRequest(
                types.InputPrivacyKeyStatusTimestamp()
            )
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            borg.storage.afk_time = datetime.datetime.now()  # pylint:disable=E0602
        borg.storage.USER_AFK.update({"yes": reason})  # pylint:disable=E0602
        if reason:
            await event.edit(f" ** I'm Unavailable at the Current Moment because of  {reason}.**")
        else:
            await event.edit(f"**** I'm Unavailable at the Current Moment***")
        await asyncio.sleep(5)
        try:
            status = f"Set AFK mode to True, and Reason is {reason}"
            await log(status)
        except Exception as e:  # pylint:disable=C0103,W0703
            logger.warn(str(e))  # pylint:disable=E0602


@borg.on(events.NewMessage(  # pylint:disable=E0602
    incoming=True,
    func=lambda e: bool(e.mentioned or e.is_private)
))
async def on_afk(event):
    if event.fwd_from:
        return
    afk_since = "**a while ago**"
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if borg.storage.USER_AFK and not (await event.get_sender()).bot:  # pylint:disable=E0602
        reason = borg.storage.USER_AFK["yes"]  # pylint:disable=E0602
        if borg.storage.afk_time:  # pylint:disable=E0602
            now = datetime.datetime.now()
            datime_since_afk = now - borg.storage.afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "**yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` **ago**"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s` **ago**"
            else:
                afk_since = f"`{int(seconds)}s` **ago**"
        msg = None
        message_to_reply = f"**My Master is AFK since** {afk_since} " + \
            f"**cuz {reason}**" \
            if reason \
            else f"**My Master is AFK since** {afk_since}"
        msg = await event.reply(message_to_reply)
        await asyncio.sleep(5)
        if event.chat_id in borg.storage.last_afk_message:  # pylint:disable=E0602
            await borg.storage.last_afk_message[event.chat_id].delete()  # pylint:disable=E0602
        borg.storage.last_afk_message[event.chat_id] = msg  # pylint:disable=E0602

async def log(text):
    LOGGER = Config.PRIVATE_GROUP_BOT_API_ID
    await borg.send_message(LOGGER, text)


SYNTAX.update({
    "afk": "\
**Requested Module --> afk**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.afk <optional_reason>```\
\nUsage: Changed afk mode to **true**.\
"
})
