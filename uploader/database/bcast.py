import traceback
import datetime
import logging
import asyncio
import time
import io

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    UserIsBlocked,
    PeerIdInvalid,
)
from Uploader.config import Config

is_cancelled = []


async def send_msg(m, user_id):
    try:
        await m.reply_to_message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x + 1)
        return self._send_msg(user_id)
    except InputUserDeactivated as e:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked as e:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid as e:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


@Client.on_message(filters.command('broadcast') & filters.private & filters.user(Config.AUTH_USERS))
async def broadcast(c, m):
    if len(m.command) == 1:
        all_users = await c.db.get_user_update()
    else:
        all_users = await c.db.get_all_users()

    message = await m.reply_text("initiating board cast", quote=True)
    cast_id = f"{m.from_user.id}/{m.id}"
    is_cancelled.append(cast_id)

    start_time = time.time()
    total_users = await c.db.total_users_count()
    done = 0
    failed = 0
    success = 0

    log_file = io.BytesIO()
    log_file.name = f"{datetime.datetime.utcnow()}_broadcast.txt"
    broadcast_log = ""
    async for user in all_users:
        await asyncio.sleep(0.5)

        if cast_id not in is_cancelled:
            break

        sts, msg = await send_msg(m, user_id=int(user["id"]))
        if msg is not None:
            broadcast_log += msg

        if sts == 200:
            success += 1
        else:
            failed += 1

        if sts == 400:
            await c.db.delete_user(user["id"])

        done += 1

        try:
            if cast_id not in is_cancelled:
                break
            buttons = [[InlineKeyboardButton('Cancel', callback_data=f'cancel_boardcast+{cast_id}')]]
            await message.edit(
                f"Total Users: {total_users}\n\nDone: {done}\n\nFalied: {failed}\n\nSuccess: {success}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except:
            pass


    log_file.write(broadcast_log.encode())
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    update_text = (
            f"#broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\n"
            f"Total done {done}, {success} success and {failed} failed.\n"
            "Status: {}".format("Completed" if cast_id in is_cancelled else "Cancelled")
    )

    await message.edit(update_text)
    if failed == 0:
        await c.send_message(
            chat_id=Config.LOG_CHANNEL,
            text=update_text,
        )
    else:
        await c.send_document(
            chat_id=Config.LOG_CHANNEL,
            document=log_file,
            caption=update_text,
        )


@Client.on_callback_query(filters.regex('^cancel_boardcast'))
async def cancel_bc(c, m):
    await m.answer()
    cmd, cast_id = m.data.split("+")
    if cast_id in is_cancelled:
        is_cancelled.remove(cast_id)
        await m.message.edit('Trying to cancel Board Cast')
    else:
        await m.message.edit('Already Cancelled')
