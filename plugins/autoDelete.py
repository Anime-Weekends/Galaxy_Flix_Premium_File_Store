#from bot import Bot
import asyncio
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from database.database import kingdb 
from datetime import datetime, timedelta

#from config import OWNER_ID
#from pyrogram.enums import ParseMode, ChatAction
#from helper_func import is_admin, banUser
#from plugins.FORMATS import * #autodel_cmd_pic, files_cmd_pic, on_txt, off_txt, FILES_CMD_TXT, AUTODEL_CMD_TXT, BAN_TXT, RFSUB_CMD_TXT

#Time conversion for auto delete
def convert_time(duration_seconds: int) -> str:
    periods = [
        ('Yᴇᴀʀ', 60 * 60 * 24 * 365),
        ('Mᴏɴᴛʜ', 60 * 60 * 24 * 30),
        ('Dᴀʏ', 60 * 60 * 24),
        ('Hᴏᴜʀ', 60 * 60),
        ('Mɪɴᴜᴛᴇ', 60),
        ('Sᴇᴄᴏɴᴅ', 1)
    ]

    parts = []
    for period_name, period_seconds in periods:
        if duration_seconds >= period_seconds:
            num_periods = duration_seconds // period_seconds
            duration_seconds %= period_seconds
            parts.append(f"{num_periods} {period_name}{'s' if num_periods > 1 else ''}")

    if len(parts) == 0:
        return "0 Sᴇᴄᴏɴᴅ"
    elif len(parts) == 1:
        return parts[0]
    else:
        return ', '.join(parts[:-1]) +' ᴀɴᴅ '+ parts[-1]


#=====================================================================================##
#.........Auto Delete Functions.......#
#=====================================================================================##
DEL_MSG = """<b>⚠️ Dᴜᴇ ᴛᴏ Cᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs....
<blockquote>Yᴏᴜʀ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴡɪᴛʜɪɴ <a href="https://t.me/{username}">{time}</a>. Sᴏ ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜᴇᴍ ᴛᴏ ᴀɴʏ ᴏᴛʜᴇʀ ᴘʟᴀᴄᴇ ғᴏʀ ғᴜᴛᴜʀᴇ ᴀᴠᴀɪʟᴀʙɪʟɪᴛʏ.</blockquote></b>"""

async def auto_del_notification(client, msg, delay_time, transfer):
    AUTO_DEL = await kingdb.get_auto_delete() #; DEL_TIMER = await get_del_timer()
    if AUTO_DEL: 
        temp = await msg.reply_text(DEL_MSG.format(username=client.username, time=convert_time(delay_time)), disable_web_page_preview = True) 
        await asyncio.sleep(delay_time)
        try:
                if transfer:
                        try:
                                name = "♻️ Cʟɪᴄᴋ Hᴇʀᴇ"; link = f"https://t.me/{client.username}?start={transfer}"
                                button = [[InlineKeyboardButton(text=name, url=link), InlineKeyboardButton(text="Cʟᴏsᴇ ✖️", callback_data = "close")]]
                                await temp.edit_text(text=f"<b>Pʀᴇᴠɪᴏᴜs Mᴇssᴀɢᴇ ᴡᴀs Dᴇʟᴇᴛᴇᴅ 🗑\n<blockquote>Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇs ᴀɢᴀɪɴ, ᴛʜᴇɴ ᴄʟɪᴄᴋ: [<a href={link}>{name}</a>] ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴇʟsᴇ ᴄʟᴏsᴇ ᴛʜɪs ᴍᴇssᴀɢᴇ.</blockquote></b>", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview = True)
                        except Exception as e:
                                await temp.edit_text(f"<b><blockquote>Pʀᴇᴠɪᴏᴜs Mᴇssᴀɢᴇ ᴡᴀs Dᴇʟᴇᴛᴇᴅ 🗑</blockquote></b>")
                                print(f"Error occured while editing the Delete message: {e}")
                else:
                        await temp.edit_text(f"<b><blockquote>Pʀᴇᴠɪᴏᴜs Mᴇssᴀɢᴇ ᴡᴀs Dᴇʟᴇᴛᴇᴅ 🗑</blockquote></b>")
        except Exception as e:
                print(f"Error occured while editing the Delete message: {e}")
        try:
            await msg.delete()
        except Exception as e:
            print(f"Error occurred on auto_del_notification() : {e}")
           
async def delete_message(msg, delay_time):
    AUTO_DEL = await kingdb.get_auto_delete()
    if AUTO_DEL: 
        await asyncio.sleep(delay_time)
        try:
            await msg.delete()
        except Exception as e:
            print(f"Error occurred on delete_message() : {e}")
