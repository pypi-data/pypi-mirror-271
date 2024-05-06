################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Kalo Pake Ini Kode Minimal Cantumkan Credits . Gw Boleh Mikir Juga Anjing, Meski Liat Ultroid
"""
################################################################

import re
import asyncio
from .class_log import LOGGER
from .database import ndB
from Mix import nlx
from random import randint
from os import execvp
from sys import executable
import wget
import random
from pyrogram.errors import *
from pyrogram.raw.functions.messages import DeleteHistory



def extract_api_token(text):
    match = re.search(r"Use this token to access the HTTP API:\s*([\w:]+)", text)
    if match:
        return match.group(1)
    else:
        return None


def extract_api_token_2(text):
    match = re.search(r"You can use this token to access HTTP API:\s*([\w:]+)", text)
    if match:
        return match.group(1)
    else:
        return None


async def autobot():
    LOGGER.info("MEMBUAT BOT TELEGRAM UNTUK ANDA DI @BotFather, Mohon Tunggu")
    gw = nlx.me
    name = gw.first_name + " Asisstant"
    if gw.username:
        username = gw.username + "_bot"
    else:
        username = "mix_" + (str(gw.id))[5:] + "_bot"
    bf = "@BotFather"

    await nlx.send_message(bf, "/start")
    await asyncio.sleep(1)
    await nlx.send_message(bf, "/newbot")
    await asyncio.sleep(1)

    async for aa in nlx.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None

    if isdone and isdone.startswith("Sorry,"):
        await nlx.send_message(bf, "/token")
        async for msg in nlx.search_messages(
            bf, query="You can use this token to access HTTP API:", limit=1
        ):
            if msg.text:
                donee = msg.text
                token = extract_api_token_2(donee)
                if token:
                    ndB.set_key("BOT_TOKEN", token)
                    LOGGER.info(
                        f"Selesai. Berhasil membuat @{username} untuk digunakan sebagai bot asisten Anda!"
                    )
                    await enable_inline(username)
                    return
                else:
                    LOGGER.error("Token API tidak ditemukan.")
                    import sys

                    sys.exit(1)

    if isdone and isdone.startswith("Alright, a new bot."):
        await nlx.send_message(bf, name)
    else:
        await nlx.send_message(bf, "/token")
        await asyncio.sleep(2)
        await nlx.send_message(bf, f"@{nlx.me.username}_bot")
        async for msg in nlx.search_messages(
            bf, query="You can use this token to access HTTP API:", limit=1
        ):
            if msg.text:
                donee = msg.text
                token = extract_api_token_2(donee)
                if token:
                    ndB.set_key("BOT_TOKEN", token)
                    LOGGER.info(
                        f"Selesai. Berhasil membuat @{username} untuk digunakan sebagai bot asisten Anda!"
                    )
                    await enable_inline(username)
                    return
                else:
                    LOGGER.error("Token API tidak ditemukan.")
                    import sys

                    sys.exit(1)

    await asyncio.sleep(1)
    async for aa in nlx.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Good."):
        await nlx.send_message(bf, username)
    await asyncio.sleep(1)
    async for aa in nlx.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "mix_" + (str(gw.id))[6:] + str(ran) + "_bot"
        await nlx.send_message(bf, username)
    await asyncio.sleep(3)
    async for aa in nlx.search_messages(
        bf, query="Use this token to access the HTTP API:", limit=1
    ):
        if aa.text:
            donee = aa.text
            token = extract_api_token(donee)
            if token:
                ndB.set_key("BOT_TOKEN", token)
                LOGGER.info(
                    f"Selesai. Berhasil membuat @{username} untuk digunakan sebagai bot asisten Anda!"
                )
                await enable_inline(username)
            else:
                LOGGER.error("Token API tidak ditemukan.")
                import sys

                sys.exit(1)
        else:
            LOGGER.error(
                "Harap Hapus Beberapa bot Telegram Anda di @Botfather atau Setel Var BOT_TOKEN dengan token bot"
            )
            import sys

            sys.exit(1)


async def enable_inline(username):
    gw = nlx.me
    if gw.username:
        user_name = gw.username
    else:
        user_name = gw.mention
    pp = random.choice(
        [
            "https://telegra.ph//file/19b336da463a05d7d8f8c.jpg",
            "https://telegra.ph//file/2eaf853d09c319465a8f4.jpg",
            "https://telegra.ph//file/7d2e8f0ae636e2f6dc381.jpg",
        ]
    )
    bb = wget.download(pp)
    LOGGER.info(f"Menyesuaikan Bot Asisten di @BotFather")
    bf = "BotFather"
    await nlx.send_message(bf, "/setuserpic")
    await asyncio.sleep(2)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(2)
    await nlx.send_photo(bf, bb)
    await asyncio.sleep(2)
    await nlx.send_message(bf, "/setabouttext")
    await asyncio.sleep(2)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(2)
    await nlx.send_message(bf, f"Mix-Userbot Asisten My Owner : @{user_name}")
    await asyncio.sleep(2)
    await nlx.send_message(bf, "/setdescription")
    await asyncio.sleep(2)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(2)
    await nlx.send_message(
        bf,
        f"Powerful Mix-Userbot Assistant\nMy Owner : @{user_name}\n\nPowered By ~ @KynanSupport",
    )
    await asyncio.sleep(2)
    await nlx.send_message(bf, "/setinline")
    await asyncio.sleep(2)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(2)
    await nlx.send_message(bf, "Search")
    LOGGER.info("Customisation Done")
    execvp(executable, [executable, "-m", "Mix"])