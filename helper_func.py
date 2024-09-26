
import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import OWNER_ID
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from database.database import kingdb #get_all_channels, get_all_admins, admin_exist, ban_user_exist
from plugins.request_forcesub import privateChannel

async def check_banUser(filter, client, update):
    user_id = update.from_user.id
    return await kingdb.ban_user_exist(user_id)

async def check_admin(filter, client, update):
    #Admin_ids = await get_all_admins()

    user_id = update.from_user.id

    # if Admin_ids:
    #     if user_id in Admin_ids:
    #         return True
    #if user_id == OWNER_ID:
        #return True
            
    return any([user_id == OWNER_ID, await kingdb.admin_exist(user_id)])

async def is_subscribed(filter, client, update):
    Channel_ids = await kingdb.get_all_channels()
    
    if not Channel_ids:
        return True

    user_id = update.from_user.id

    if any([user_id == OWNER_ID, await kingdb.admin_exist(user_id)]):
        return True
        
    member_status = ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER
    
    REQFSUB = await kingdb.get_request_forcesub()
                    
    for id in Channel_ids:
        if not id:
            continue
            
        try:
            member = await client.get_chat_member(chat_id=id, user_id=user_id)
        except UserNotParticipant:
            if REQFSUB and await privateChannel(client, id):
                return await kingdb.reqSent_user_exist(id, user_id)
            return False
    
        if member.status not in member_status:
            if REQFSUB and await privateChannel(client, id):
                return await kingdb.reqSent_user_exist(id, user_id)
            return False

    return True

async def is_userJoin(client, user_id, channel_id):
    REQFSUB = await kingdb.get_request_forcesub()
    
    try:
        member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}
    except UserNotParticipant:
        if REQFSUB and await privateChannel(client, channel_id):
                return await kingdb.reqSent_user_exist(channel_id, user_id)
        return False
    except Exception as e:
        print(f"An error occurred on is_userJoin(): {e}")
        return False
    
async def encode(string):
    try:
        string_bytes = string.encode("ascii")
        base64_bytes = base64.urlsafe_b64encode(string_bytes)
        base64_string = (base64_bytes.decode("ascii")).strip("=")
        return base64_string
    except Exception as e:
        print(f'Error occured on encode, reason: {e}')

async def decode(base64_string):
    try:
        base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.
        base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
        string_bytes = base64.urlsafe_b64decode(base64_bytes) 
        string = string_bytes.decode("ascii")
        return string
    except Exception as e:
        print(f'Error occured on decode, reason: {e}')

async def get_messages(client, message_ids):
    try:
        messages = []
        total_messages = 0
        while total_messages != len(message_ids):
            temb_ids = message_ids[total_messages:total_messages+200]
            try:
                msgs = await client.get_messages(
                    chat_id=client.db_channel.id,
                    message_ids=temb_ids
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                msgs = await client.get_messages(
                    chat_id=client.db_channel.id,
                    message_ids=temb_ids
                )
            except:
                pass
            total_messages += len(temb_ids)
            messages.extend(msgs)
        return messages
    except Exception as e:
        print(f'Error occured on get_messages, reason: {e}')

async def get_message_id(client, message):
    if message.forward_from_chat:
        if message.forward_from_chat.id == client.db_channel.id:
            return message.forward_from_message_id
        else:
            return 0
    elif message.forward_sender_name:
        return 0
    elif message.text:
        pattern = r"https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern,message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    else:
        return 0


def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


subscribed = filters.create(is_subscribed)
is_admin = filters.create(check_admin)
banUser = filters.create(check_banUser)
