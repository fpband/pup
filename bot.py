
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os
import pytz
import datetime
from Uploader.config import Config

from Uploader.database.database import Database

from pyrogram import Client as Clinton

if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(root="Uploader")
    Warrior = Clinton("@UPLOADER_X_BOT",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,

    plugins=plugins)
    Warrior.db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)
    Warrior.broadcast_ids = {}
    Warrior.run()

