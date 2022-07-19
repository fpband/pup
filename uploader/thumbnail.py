# Copyright @Tellybots | @ShriMadhavUk | @PlanetBots

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import random
import numpy
import os
from PIL import Image
import time

# the Strings used for this "thing"
from Uploader.script import Translation
from pyrogram import Client

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters
from Uploader.functions.help_Nekmo_ffmpeg import take_screen_shot
import psutil
import shutil
import string
import asyncio
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from Uploader.functions.forcesub import handle_force_subscribe

from Uploader.config import Config

from Uploader.script import TEXT

f = filters.command(["delthumb"])
s = filters.command("showthumb")


################## Saving thumbnail 🖼 ##################

@Client.on_message(filters.photo & filters.incoming & filters.private)
async def save_photo(c, m):

    send_message = await m.reply_text(
        "**Processing.....⏳**",
       # parse_mode="markdown",
        quote=True
    )

    is_user_exist = await c.db.is_user_exist(m.from_user.id)
    if not is_user_exist:
        await c.db.add_user(m.from_user.id)

    download_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"
    await c.db.update_settings_status(m.from_user.id, 'permanent_thumb', m.id)
    await m.download(
        file_name=download_location,
        block=False
    )

    await send_message.edit(
        text=TEXT.SAVED_CUSTOM_THUMBNAIL
       # parse_mode="markdown"
    )


################## Deleting permanent thumbnail 🗑 ##################

@Client.on_message(filters.command("deletethumbnail") & filters.incoming & filters.private)
async def delete_thumbnail(c, m):

    send_message = await m.reply_text(
        "**Processing.....⏳**",
        #parse_mode="markdown",
        quote=True
    )

    is_user_exist = await c.db.is_user_exist(m.from_user.id)
    if not is_user_exist:
        await c.db.add_user(m.from_user.id)

    download_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"
    thumbnail = await c.db.get_settings_status(m.from_user.id, 'permanent_thumb')

    if not thumbnail:
        text = TEXT.NO_CUSTOM_THUMB_NAIL_FOUND

    if thumbnail:
        try:
            await c.db.update_settings_status(m.from_user.id, 'permanent_thumb', '')
        except:
            pass
        text = TEXT.DELETED_CUSTOM_THUMBNAIL

    try:
        os.remove(download_location)
    except:
        pass

    await send_message.edit(
        text=text
        #parse_mode="markdown"
    )


################## Sending permanent thumbnail 🕶 ##################

@Client.on_message(filters.command("showthumbnail") & filters.incoming & filters.private)
async def show_thumbnail(c, m):

    send_message = await m.reply_text(
        "**Processing.....⏳**",
       # parse_mode="markdown",
        quote=True
    )

    is_user_exist = await c.db.is_user_exist(m.from_user.id)
    if not is_user_exist:
        await c.db.add_user(m.from_user.id)

    thumbnail = await c.db.get_settings_status(m.from_user.id, 'permanent_thumb')
    if not thumbnail:
         await send_message.edit(
             text=TEXT.NO_CUSTOM_THUMB_NAIL_FOUND
         )
    if thumbnail:
         download_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"

         if not os.path.exists(download_location):
             thumb_nail = await c.get_messages(m.chat.id, thumbnail)
             try:
                 photo_location = await thumb_nail.download(file_name=download_location)
             except:
                 await c.db.update_settings_status(m.from_user.id, 'permanent_thumb', '')
                 return await send_message.edit(text=TEXT.NO_CUSTOM_THUMB_NAIL_FOUND)
         else:
             photo_location = download_location

         await send_message.delete()
         await m.reply_photo(
             photo=photo_location,
             caption=TEXT.THUMBNAIL_CAPTION,
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("𝐃𝐞𝐥𝐞𝐭𝐞 𝐓𝐡𝐮𝐦𝐛𝐧𝐚𝐢𝐥 🗑️", callback_data="del")]]),
             #parse_mode="markdown",
             quote=True
         )


################## THE END 🛑 ##################




async def Gthumb01(bot, update):
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await bot.db.get_settings_status(update.from_user.id, 'permanent_thumb')
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
        Image.open(thumbnail).convert("RGB").save(thumbnail)
        img = Image.open(thumbnail)
        img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None

    return thumbnail

async def Gthumb02(bot, update, duration, download_directory):
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await bot.db.get_settings_status(update.from_user.id, 'permanent_thumb')
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
    else:
        thumbnail = await take_screen_shot(download_directory, os.path.dirname(download_directory), random.randint(0, duration - 1))

    return thumbnail

async def Mdata01(download_directory):

          width = 0
          height = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")
              if metadata.has("height"):
                  height = metadata.get("height")

          return width, height, duration

async def Mdata02(download_directory):

          width = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")

          return width, duration

async def Mdata03(download_directory):

          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds

          return duration
