# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import time
import sys
import psutil
import asyncio
import platform
import traceback
from datetime import datetime
from userbot import util
from telethon import __version__

DELETE_TIMEOUT = 5
if not os.path.exists(Config.DOWNLOAD_DIRECTORY):
    os.mkdir(Config.DOWNLOAD_DIRECTORY)


@client.on(register(pattern="reload (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def reload_module(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        if shortname in client._modules:  # pylint:disable=E0602
            client.remove_module(shortname)  # pylint:disable=E0602
        client.load_module(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"Successfully reloaded {shortname}")
        await asyncio.sleep(DELETE_TIMEOUT)
        await msg.delete()
    except Exception as e:  # pylint:disable=C0103,W0703
        trace_back = traceback.format_exc()
        # pylint:disable=E0602
        logger.warn(f"Failed to (re)load {shortname}: {trace_back}")
        await event.respond(f"Failed to (re)load {shortname}: {e}")


@client.on(register(pattern="(?:unload) (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def remove_module(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    if shortname == "_core":
        msg = await event.respond(f"{shortname} can not be removed!")
    elif shortname in client._modules:  # pylint:disable=E0602
        client.remove_module(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"Unloaded {shortname}")
    else:
        msg = await event.respond(f"{shortname} is not loaded!")
    await asyncio.sleep(DELETE_TIMEOUT)
    await msg.delete()


@client.on(register(pattern="load"))  # pylint:disable=E0602
async def install_module(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        module = await event.get_reply_message()
        loaded = False
        while not loaded:
            try:
                downloaded_file_name = await client.download_media(  # pylint:disable=E0602
                    module,
                    client._module_path  # pylint:disable=E0602
                )
                if "(" not in downloaded_file_name:
                    client.load_module_from_file(
                        downloaded_file_name)  # pylint:disable=E0602
                    await event.edit("Loaded `{}`".format(os.path.basename(downloaded_file_name)))
                    loaded = True
                else:
                    client.remove_module(module.file.name[:-3])
                    os.remove(f"modules/" + str(module.file.name))
                    await event.edit("`Module already exists, overwriting..`")
                    asyncio.sleep(0.25)
            except Exception as e:  # pylint:disable=C0103,W0703
                await event.edit(str(e))
                os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()


@client.on(register(pattern="share (.*)"))
async def share_module(event):
    if event.fwd_from:
        return
    mone = await event.edit("Searching for required file..")
    input_str = event.pattern_match.group(1)
    module = f"modules/{input_str}.py"
    if os.path.exists(module):
        start = datetime.now()
        c_time = time.time()
        await client.send_file(
            event.chat_id,
            module,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                util.progress(d, t, mone, c_time, "Sharing module..")
            )
        )
        end = datetime.now()
        # os.remove(input_str)
        ms = (end - start).seconds
        await mone.edit(f"Uploaded {input_str} in {ms} seconds.")
    else:
        await mone.edit("404: Module not found")


@client.on(register(pattern="help ?(.*)"))
async def help(event):
    if event.fwd_from:
        return
    key = event.pattern_match.group(1)
    if not key:
        msg = "The-TG-Bot v3 Modules:"
        title = ""
        for key in sorted(Config.HELPER):
            new_title = f"\n\n{key[0].upper()}\n\n"
            if new_title == title:
                title = "\n"
            else:
                title = new_title
            msg += f"{title}~ {key}"
            title = new_title
        msg += f"\n\nNumber of modules: **{modcount}**\nSend .help <module_name> to get help regarding a module."
        await event.edit(msg)
    else:
        msg = ""
        msg += f"Available commands for **{key}** module:\n\n"
        try:
            msg += Config.HELPER[key]
        except KeyError:
            msg = f"**{key}** module doesnt exist!"
        await event.edit(msg)


@client.on(register(pattern="alive ?(.*)", allow_sudo=True))
async def alive(event):
    if event.fwd_from:
        return
    await event.delete()    
    uname = platform.uname()
    username = f"\nUser: `{user}\n"
    memory = psutil.virtual_memory()
    specs = f"`System: {uname.system}\nRelease: {uname.release}\nVersion: {uname.version}\nProcessor: {uname.processor}\nMemory [RAM]: {get_size(memory.total)}`"
    help_string = f"**// The-TG-Bot v3 is running //**\n\n**General Info:**\n`Build Version: {build} {username}`Github Repository: `{Config.GITHUB_REPO_LINK}\n\n**System Specifications:**\n{specs}\n```Python: {sys.version}```\n```Telethon: {__version__}```\n\n**Contact developer:** [Priyam Kalra](https://t.me/justaprudev) \n**Update channel:** [Join](https://t.me/The_TG_Bot) \n**Support group:** [Join](https://t.me/The_TG_Bot_Support)"
    await client.send_file(
        event.chat_id,
        caption=help_string,
        file="logo.png",
        force_document=False,
        allow_cache=False
    )


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


Config.HELPER.update({
    "core": "\
```.load <as_a_reply_to_a_module_file>```\
\nUsage: Load a specified module.\
\n\n```.reload <module_name>```\
\nUsage: Reload any module that was unloaded.\
\n\n```.unload <module_name>```\
\nUsage: Unload any loaded module.\
\n\n```.alive```\
\nUsage: Returns userbot's system stats and some general information.\
\n\n```.help <optional_module_name>```\
\nUsage: Returns help strings for various modules of this userbot.\
\n\n```.restart```\
\nUsage: Restarts the userbot.\
\n\n```.share <module_name>```\
\nUsage: Share any loaded module.\
"
})
