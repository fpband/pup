
# Copyright @Tellybots | @Shrimadhav Uk
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import asyncio
import aiohttp
import json
import math
import os
import shutil
import time
from datetime import datetime
from Uploader.config import Config
from Uploader.script import Translation
from Uploader.thumbnail import *
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from Uploader.functions.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
#from pyrogram import enums 




async def ddl_call_back(bot, update):
    #logger.info(update)
    cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("=")
    youtube_dl_url = update.message.reply_to_message.text
    thumb_image_path = Config.DOWNLOAD_LOCATION + \
        "/" + str(update.from_user.id) + ".jpg"
    custom_file_name = os.path.basename(youtube_dl_url)
    if " " in youtube_dl_url:
        url_parts = youtube_dl_url.split(" * ")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        else:
            for entity in update.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]
        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
    else:
        for entity in update.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]
    
    description = custom_file_name
    if not "." + youtube_dl_ext in custom_file_name:
        custom_file_name += '.' + youtube_dl_ext
    logger.info(youtube_dl_url)
    logger.info(custom_file_name)
    
    start = datetime.now()
    await bot.edit_message_text(
        text=Translation.DOWNLOAD_START.format(custom_file_name),
        chat_id=update.message.chat.id,
        message_id=update.message.id
    )
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user + "/" + custom_file_name
    command_to_exec = []
    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            await download_coroutine(
                bot,
                session,
                youtube_dl_url,
                download_directory,
                update.message.chat.id,
                update.message.id,
                c_time
            )
        except asyncio.TimeoutError:
            await bot.edit_message_text(
                text=Translation.SLOW_URL_DECED,
                chat_id=update.message.chat.id,
                message_id=update.message.id
            )
            return False
    if os.path.exists(download_directory):
        save_ytdl_json_path = Config.DOWNLOAD_LOCATION + "/" + str(update.message.chat.id) + ".json"
        if os.path.exists(save_ytdl_json_path):
            os.remove(save_ytdl_json_path)
        end_one = datetime.now()
        await bot.edit_message_text(
            text=Translation.UPLOAD_START,
            chat_id=update.message.chat.id,
            message_id=update.message.id
        )
        file_size = Config.TG_MAX_FILE_SIZE + 1
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError as exc:
            download_directory = os.path.splitext(download_directory)[0] + "." + "mkv"
            # https://stackoverflow.com/a/678242/4723940
            file_size = os.stat(download_directory).st_size
        if file_size > Config.TG_MAX_FILE_SIZE:
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.RCHD_TG_API_LIMIT,
                message_id=update.message.id
            )
        else:
            # ref: message from @SOURCES_CODES
            start_time = time.time()


            # try to upload file

    

            settings = await bot.db.get_all_settings(update.from_user.id)
            as_file = settings['upload_as_file']
            # try to upload file

            if tg_send_type == "upload_as_file":
                thumbnail = await Gthumb01(bot, update)
                await bot.send_document(
                    chat_id=update.message.chat.id,
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    #parse_mode="HTML",
                    reply_to_message_id=update.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        #custom_file_name,
                        start_time
                    )
                )

            elif tg_send_type == "video":
                 width, height, duration = await Mdata01(download_directory)
                 thumbnail = await Gthumb02(bot, update, duration, download_directory)
                 await bot.send_video(
                    chat_id=update.message.chat.id,
                    video=download_directory,
                    caption=description,
                    # parse_mode="HTML",
                    duration=duration,
                    width=width,
                    height=height,
                    thumb=thumbnail,
                    supports_streaming=True,
                    reply_to_message_id=update.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        #custom_file_name,
                        start_time
                    )
                )
            if tg_send_type == "audio":
                duration = await Mdata03(download_directory)
                thumbnail = await Gthumb01(bot, update)
                await bot.send_audio(
                    chat_id=update.message.chat.id,
                    audio=download_directory,
                    caption=description,
                   # parse_mode="HTML",
                    duration=duration,
                    thumb=thumbnail,
                    reply_to_message_id=update.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        #custom_file_name,
                        start_time
                    )
                ) 
            elif tg_send_type == "vm":
                width, duration = await Mdata02(download_directory)
                thumbnail = await Gthumb02(bot, update, duration, download_directory)
                await bot.send_video_note(
                    chat_id=update.message.chat.id,
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumb_image_path,
                    reply_to_message_id=update.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        #custom_file_name,
                        start_time
                    )
                )           
            
     
            else:
                logger.info("✅ " + custom_file_name)

            end_two = datetime.now()
            settings = await c.db.get_all_settings(m.from_user.id)
            screen_shots = settings['screen_shot']
            sample_video = settings['sample_video']

    # if screenshots
            if screen_shots != 0:
                try:
                    send_text = await m.reply_text(text="**Generating Screenshots...😎**")

                    if duration > 0:
                        images = []
                        ttl_step = duration // screen_shots
                        random_start = random.randint(0, duration - (screen_shots * ttl_step))
                        current_ttl = random_start
                        for looper in range(0, screen_shots):
                            ss_img = await take_screen_shot(description, tmp_directory_for_each_user, current_ttl)
                            current_ttl = current_ttl + ttl_step
                            images.append(ss_img)
        
              
                        media_album_p = []
                        if images is not None:
                            i = 0
                            caption = "**© @DKBOTZ**"
                            for image in images:
                                if image != None:
                                    if i == 0:
                                        media_album_p.append(
                                            InputMediaPhoto(
                                                media=images[i],
                                                caption=caption,
                                        #parse_mode="markdown"
                                            )
                                        )
                                    else:
                                        media_album_p.append(
                                            InputMediaPhoto(
                                                media=image
                                            )
                                        )
                                    i = i + 1
                            await send_text.delete()
                            await m.reply_chat_action("upload_photo")
                            await m.reply_media_group(
                                media=media_album_p,
                                disable_notification=True,
                                quote=True,
                            )
                    else:
                        await send_text.edit("**😑 Failed To Generate Screenshots**")

                except Exception as e:
                    print(e)
                    await send_text.edit("**Unable To Generate Screenshots 😔**\n\nError: {e}")

    # if sample video is needed
            if sample_video != 0:
                await generate_sample(description, bot, update)

            try:
                os.remove(description)
                shutil.rmtree(tmp_directory_for_each_user)
            except Exception as e:
                print(e)
            await complete_process(bot, update)
            try:
                os.remove(download_directory)
                os.remove(thumb_image_path)
            except:
                pass
            time_taken_for_download = (end_one - start).seconds
            time_taken_for_upload = (end_two - end_one).seconds
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                chat_id=update.message.chat.id,
                message_id=update.message.id,
                disable_web_page_preview=True
            )

            logger.info("✅ Downloaded in: " + str(time_taken_for_download))
            logger.info("✅ Uploaded in: " + str(time_taken_for_upload))



    else:
        await bot.edit_message_text(
            text=Translation.NO_VOID_FORMAT_FOUND.format("Incorrect Link"),
            chat_id=update.message.chat.id,
            message_id=update.message.id,
            disable_web_page_preview=True
        )


async def download_coroutine(bot, session, url, file_name, chat_id, message_id, start):
    downloaded = 0
    display_message = ""
    async with session.get(url, timeout=Config.PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(Config.CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += Config.CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = """**Download Status**
URL: {}
File Size: {}
Downloaded: {}
ETA: {}""".format(
    url,
    humanbytes(total_length),
    humanbytes(downloaded),
    TimeFormatter(estimated_total_time)
)
                        if current_message != display_message:
                            await bot.edit_message_text(
                                chat_id,
                                message_id,
                                text=current_message
                            )
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
                        pass
        return await response.release()

