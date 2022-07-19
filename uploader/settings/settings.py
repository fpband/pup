import logging
logger = logging.getLogger(__name__)

from Uploader.config import Config
from Uploader.script import TEXT
from Uploader.thumbnail import show_thumbnail
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


#################### Sending message for Settings Command ⚙ ####################

@Client.on_message(filters.command('settings') & filters.incoming & filters.private)
async def settings(c, m, cb=False):
    if not cb:
        send_message = await m.reply_text(
            "**Processing.....⏳**",
            #parse_mode="markdown",
            quote=True
        )
    
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
        await c.send_message(
            Config.LOG_CHANNEL,
            f"New User {m.from_user.mention} started."
        )

    settings = await c.db.get_all_settings(m.from_user.id)
    upload_mode = settings['upload_as_file']
    upload_text = 'Upload as File 📤' if upload_mode else 'Upload as Video 📤'

    bot_updates_mode = settings['bot_updates']
    bot_updates_text = 'ON 🔔' if bot_updates_mode else 'OFF 🔕' 

    thumbnail = settings['permanent_thumb']
    thumb_text = 'Show Thumbnail 🎑' if thumbnail else 'Set Custom Thumbnail'

    no_screen_shot = settings['screen_shot']
    screenshot_text = 'ON 📸' if no_screen_shot != 0 else 'OFF 📷' 

    duration_sample_video = settings['sample_video']
    samplevideo_text = 'ON 🔊' if duration_sample_video != 0 else 'OFF 🔇' 

    settings_btn = [
        [
            InlineKeyboardButton(f'{upload_text}', callback_data=f"setting+upload_as_file+{not upload_mode}")
        ],
        [
            InlineKeyboardButton(f"Bot Updates: {bot_updates_text}", callback_data=f"setting+bot_updates+{not bot_updates_mode}")
        ],
        [
            InlineKeyboardButton(f"{thumb_text}", callback_data=f"thumbnail")
        ],
        [
            InlineKeyboardButton(f"Screen Shots: {screenshot_text}", callback_data="screenshots")
        ],
        [
            InlineKeyboardButton(f"Sample Video: {samplevideo_text}", callback_data=f"samplevideo")
        ]
    ]

    if cb:
        if m.message.reply_to_message.text == '/start':
            settings_btn.append([InlineKeyboardButton('《 BACK 》', callback_data='back')])
    try:
        if cb:
            await m.answer()
            await m.message.edit(
                text="⚙️ 𝖢𝗈𝗇𝖿𝗂𝗀 𝖡𝗈𝗍 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌",
               # parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(settings_btn)
            )
        if not cb:
            await send_message.edit(
                text="⚙️ 𝖢𝗈𝗇𝖿𝗂𝗀 𝖡𝗈𝗍 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌",
                #parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(settings_btn)
            )
    except:
        pass


#################### Callbacks related to Settings ⚙ ####################

@Client.on_callback_query(filters.regex('^setting'))
async def settings_cb(c, m):
    if len(m.data.split("+")) == 1:
        return await settings(c, m, cb=True)
    cmd, key, val = m.data.split("+")
    if 'True' in val or 'False' in val:
        value = True if val == 'True' else False
        await c.db.update_settings_status(m.from_user.id, str(key), value)
        await settings(c, m, cb=True)
    else:
        value = int(val)
        await c.db.update_settings_status(m.from_user.id, str(key), value)
        if key == "screen_shot":
            await screen_shot_cb(c, m)
        else:
            await samplevideo_cb(c, m)


@Client.on_callback_query(filters.regex('^thumbnail'))
async def thumb_cb(c, m):
    thumbnail = await c.db.get_settings_status(m.from_user.id, 'permanent_thumb')
    if not thumbnail:
        await m.answer('Send me a photo For saving permanently 🏞', show_alert=True)
    else:
        await show_thumbnail(c, m.message.reply_to_message)
    await settings(c, m, cb=True)


@Client.on_callback_query(filters.regex('^screenshots$'))
async def screen_shot_cb(c, m):
    screen_shot = await c.db.get_settings_status(m.from_user.id, 'screen_shot')
    on_text = "💠 ON" if screen_shot != 0 else "ON"
    off_text = "💠 OFF" if screen_shot == 0 else "OFF"
    text1 = "✅ 1" if screen_shot == 1 else "☑ 1"
    text2 = "✅ 2" if screen_shot == 2 else "☑ 2"
    text3 = "✅ 3" if screen_shot == 3 else "☑ 3"
    text4 = "✅ 4" if screen_shot == 4 else "☑ 4"
    text5 = "✅ 5" if screen_shot == 5 else "☑ 5"
    text6 = "✅ 6" if screen_shot == 6 else "☑ 6"
    text7 = "✅ 7" if screen_shot == 7 else "☑ 7"
    text8 = "✅ 8" if screen_shot == 8 else "☑ 8"
    text9 = "✅ 9" if screen_shot == 9 else "☑ 9"
    text10 = "✅ 10" if screen_shot == 10 else "☑ 10"
    screenshot = [InlineKeyboardButton("Screen Shots", callback_data="None")]
    screenshot_status = [
        InlineKeyboardButton(on_text, callback_data="setting+screen_shot+10"),
        InlineKeyboardButton(off_text, callback_data="setting+screen_shot+0")
    ]
    screenshot_number1 = [
        InlineKeyboardButton(text1, callback_data="setting+screen_shot+1"),
        InlineKeyboardButton(text3, callback_data="setting+screen_shot+3"),
        InlineKeyboardButton(text5, callback_data="setting+screen_shot+5"),
        InlineKeyboardButton(text7, callback_data="setting+screen_shot+7"),
        InlineKeyboardButton(text9, callback_data="setting+screen_shot+9")
    ]
    screenshot_number2 = [
        InlineKeyboardButton(text2, callback_data="setting+screen_shot+2"),
        InlineKeyboardButton(text4, callback_data="setting+screen_shot+4"),
        InlineKeyboardButton(text6, callback_data="setting+screen_shot+6"),
        InlineKeyboardButton(text8, callback_data="setting+screen_shot+8"),
        InlineKeyboardButton(text10, callback_data="setting+screen_shot+10")
    ]
    button = [screenshot, screenshot_status]
    if screen_shot != 0:
        button.append(screenshot_number1)
        button.append(screenshot_number2)
    button.append([InlineKeyboardButton("🔙 Back", callback_data="setting")])
    await m.answer()
    await m.message.edit("**Select The suitable option you need**", reply_markup=InlineKeyboardMarkup(button))


@Client.on_callback_query(filters.regex('^samplevideo$'))
async def samplevideo_cb(c, m):
    sample_video = await c.db.get_settings_status(m.from_user.id, 'sample_video')
    samplevideo = [InlineKeyboardButton("Sample Video", callback_data="None")]
    on_text2 = "💠 ON" if sample_video != 0 else "ON"
    off_text2 = "💠 OFF" if sample_video == 0 else "OFF"
    duration1 = "✅ 30" if sample_video == 30 else "☑ 30"
    duration2 = "✅ 60" if sample_video == 60 else "☑ 60"
    duration3 = "✅ 90" if sample_video == 90 else "☑ 90"
    duration4 = "✅ 120" if sample_video == 120 else "☑ 120"
    duration5 = "✅ 150" if sample_video == 150 else "☑ 150"

    samplevideo_status = [
        InlineKeyboardButton(on_text2, callback_data="setting+sample_video+30"),
        InlineKeyboardButton(off_text2, callback_data="setting+sample_video+0")
    ]
    samplevideo_duration = [
        InlineKeyboardButton(duration1, callback_data="setting+sample_video+30"),
        InlineKeyboardButton(duration2, callback_data="setting+sample_video+60"),
        InlineKeyboardButton(duration3, callback_data="setting+sample_video+90"),
        InlineKeyboardButton(duration4, callback_data="setting+sample_video+120"),
        InlineKeyboardButton(duration5, callback_data="setting+sample_video+150")
    ]
    button = [samplevideo, samplevideo_status]
    if sample_video != 0:
        button.append(samplevideo_duration)
    button.append([InlineKeyboardButton("🔙 Back", callback_data="setting")])
    await m.answer()
    await m.message.edit("**Select The Suitable Option You Need**", reply_markup=InlineKeyboardMarkup(button))
#################### THE END 🌋 ####################
