import os
from Uploader.functions.display_progress import progress_for_pyrogram, humanbytes
from Uploader.config import Config
from Uploader.dl_button import ddl_call_back
from Uploader.button import youtube_dl_call_back
from Uploader.commands import help, start, about

from Uploader.script import Translation, TEXT
from pyrogram import Client, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from Uploader.commands import *
from Uploader.thumbnail import delete_thumbnail


@Client.on_callback_query()
async def button(bot, update):
      cb_data = update.data
      if "|" in cb_data:
          await youtube_dl_call_back(bot, update)
      elif "=" in cb_data:
          await ddl_call_back(bot, update)
      elif cb_data == "help":
          await help(bot, update, "False")
      elif cb_data == "donate":
          await donate(bot, update)
      elif cb_data == "close":
          await update.message.delete()
      elif cb_data == "back":
          await start(bot, update, "False")
      elif cb_data == "about":
          await about(bot, update, "False")
