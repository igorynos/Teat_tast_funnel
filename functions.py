from loader import db, app
from database import Users
from datetime import timedelta
from pyrogram.errors import UserDeactivated, BotGroupsBlocked
import asyncio


class WaitToSend:
    msg_1 = timedelta(minutes=6)
    msg_2 = timedelta(minutes=39)
    msg_3 = timedelta(days=1, hours=2)

    dict_loop = {}

    def __init__(self, message):
        self.user_id = message.from_user.id
        self.message = message
        self.timer = 0
        self.triger = False
        self.triger_msg_3 = False


async def loop_msg(obj):
    queue_message = 0
    lst_time = [WaitToSend.msg_1, WaitToSend.msg_2, WaitToSend.msg_3]
    obj.timer = lst_time[queue_message]
    while True:
        await asyncio.sleep(1)
        if obj.triger:
            break
        if obj.triger_msg_3 and queue_message == 2:
            break
        obj.timer -= timedelta(seconds=1)
        if obj.timer == timedelta(seconds=0):
            queue_message += 1
            await check_block_user(obj.message, f'Текст{queue_message}')
            try:
                obj.timer = lst_time[queue_message]
            except:
                break


def check_user(user_id):
    result = db.query(Users).filter_by(id=user_id).first()
    return result


async def check_block_user(message, text):
    try:
        await app.send_message(chat_id=message.from_user.id, text=text)
    except (BotGroupsBlocked, UserDeactivated):
        user = db.query(Users).filter_by(id=message.from_user.id).first()
        user.status = 'blocked'
        user.status_updated_at = message.date
        db.commit()
