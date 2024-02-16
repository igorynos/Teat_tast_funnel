from loader import app, db
from pyrogram import filters
from database import Users
from functions import WaitToSend, check_user, loop_msg
from pyrogram.errors import UserDeactivated, BotGroupsBlocked


@app.on_message(filters.text)
async def main_handler(client, message):
    message_text = message.text
    triger = ['прекрасно', 'ожидать', 'тригер1']
    if any(word.lower() in message_text.lower() for word in triger):
        await trigers(client, message)
    await start_user(client, message)

async def start_user(client, message):
    if check_user(message.from_user.id) is None:
        user = Users(id=message.from_user.id, 
                     created_at=message.date, 
                     status="alive",
                     status_updated_at = message.date
                     )
        
        db.add(user)
        db.commit()
       
        WaitToSend.dict_loop[f'{message.from_user.id}'] = WaitToSend(message)
        await loop_msg(WaitToSend.dict_loop[f'{message.from_user.id}'])

async def trigers(client, message):
    user = db.query(Users).filter_by(id=message.from_user.id).first()
    message_text = message.text.lower()
    triger = ['Прекрасно', 'Ожидать']
    triger_msg_3 = 'Тригер1'
    if any(word.lower() in message_text for word in triger):
        user.status = 'finished'
        user.status_updated_at = message.date
        try:
            WaitToSend.dict_loop[f'{message.from_user.id}'].triger = True
        except:
            pass
    if triger_msg_3.lower() in message_text.lower():
        user.status = 'finished'
        user.status_updated_at = message.date
        try:    
            WaitToSend.dict_loop[f'{message.from_user.id}'].triger_msg_3 = True
            
        except:
            pass
    db.commit()

