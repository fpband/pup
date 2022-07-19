#(C) Callback fix by CvaTricks


import os
import time
import psutil
import shutil
import string
import asyncio
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.types import Message 
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from Uploader.config import Config
from Uploader.script import Translation
from pyrogram import Client, filters

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


@Client.on_message(filters.command("help") & filters.private & filters.incoming)
async def help(c, m, cb=False):
    button = [[
        InlineKeyboardButton('🏕️ Home', callback_data='back'),
        InlineKeyboardButton('💸 Donate', callback_data='donate')
        ],[
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)

    if cb:
        try:
            await m.message.edit(
                text=TEXT.HELP_USER.format(m.from_user.first_name),
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except:
            pass
    else:
        await m.reply_text(
            text=TEXT.HELP_USER.format(m.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )



@Client.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(c, m, cb=False):
    if not cb:
        start = await m.reply_text("**Checking...**", quote=True)

    button = [
        [
            InlineKeyboardButton('🧔 Developer', url='https://t.me/DKBOTZHELP'),
            InlineKeyboardButton('📘 About', callback_data='about')
        ],
        [
            InlineKeyboardButton('💡 Help', callback_data="help"),
            InlineKeyboardButton('🛠 Settings', callback_data="setting")
        ],
        [
            InlineKeyboardButton('❌ Close', callback_data="close")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        try:
            await m.message.edit(
                text=Translation.START_TEXT.format(m.from_user.first_name), 
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except:
            pass
    else:
        await start.edit(
            text=Translation.START_TEXT.format(m.from_user.first_name), 
            disable_web_page_preview=True,
            reply_markup=reply_markup
        ) 


@Client.on_message(filters.command("about") & filters.private & filters.incoming)
async def about(c, m, cb=False):
    restart_time = Config.RESTART_TIME[0]
    time_format = restart_time.strftime("%d %B %Y %I:%M %p")
    button = [[
        InlineKeyboardButton('🏕️ Home', callback_data='back'),
        InlineKeyboardButton('💸 Donate', callback_data='donate')
        ],[
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        try:
            await m.message.edit(
                text=Translation.ABOUT_TEXT.format(time_format),
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except:
            pass
    else:
        await m.reply_text(
            text=Translation.ABOUT_TEXT.format(time_format),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )

async def donate(bot, update):
    await bot.send_message(update.chat.id, "Thanks for showing interest on Donation")
