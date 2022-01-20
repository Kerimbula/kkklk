from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from asyncio import sleep
import config as c
import random
import sqlite3

bot = Bot(token=c.token, parse_mode="html")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    startbtn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text="💎Click")
    btn2 = KeyboardButton(text="👤Profil")
    btn3 = KeyboardButton(text="🌐Admin")
    btn4 = KeyboardButton(text="📚Bot info")
    startbtn.add(btn1)
    startbtn.add(btn2, btn3)
    startbtn.add(btn4)
    connection = sqlite3.connect('user.db')
    db = connection.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS user (
    id BIGINT,
    money BIGINT,
    status TEXT,
    dr TEXT,
    zall BIGINT, 
    vall BIGINT
    )""")
    connection.commit()
    db.execute("SELECT * FROM user WHERE id = (?)", (m.from_user.id, ))
    data = db.fetchone()
    if data is None:
        dr = datetime.now().date()
        await m.answer(f'<b>Salam! {m.from_user.first_name}!</b>', reply_markup=startbtn)
        await bot.send_message(1004250581, f"#новый_пользователь\nНик: <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>\nИд: <code>{m.from_user.id}</code>")
        db.execute(f"INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", (m.from_user.id, 0, "не подтверждён", dr, 0, 0))
        connection.commit()
    else:
        await m.answer("<b>Yene? Pul ishle!</b>", reply_markup=startbtn)
       
@dp.message_handler(content_types=['text'])
async def texts(m: types.Message):
    connection = sqlite3.connect('user.db')
    db = connection.cursor()
    db.execute("SELECT * FROM user WHERE id = (?)", (m.from_user.id, ))
    data = db.fetchone()
    if m.text == '👤Profil':
        un = m.from_user.username
        pr = un[:5]
        if un != '':
            username = m.from_user.username
        else:
            username = m.from_user.first_name
        vivod = InlineKeyboardMarkup()
        v = KeyboardButton(text="💰Chykarmak", callback_data="vivod")
        vivod.add(v)
        await m.answer(f"<b>Sizin profiliniz:</b>\n\n⭐Sizin nikynyz: {username}\n⭐Sizin idnyz: {m.from_user.id}\n⭐Balansynyz: {data[1]}\n⭐Ishlediniz: {data[4]}\n⭐Hachan geleniniz: {data[3]}", reply_markup=vivod)
    if m.text == '🌐Tex Komek':
        s = m.text
        if s == '🌐Tex Komek':
            ad = InlineKeyboardMarkup()
            a = KeyboardButton(text="Yazmak", url="https://t.me/CulerVPN")
            ad.add(a)
            await m.answer("👇Knopka bas admina yazmak uchin", reply_markup=ad) 
    elif m.text == '📚Bot info':
        brnow = datetime.now().date()
        conn = sqlite3.connect('user.db')
        sql = conn.cursor()
        sql.execute("SELECT * FROM user WHERE dr = (?)", (brnow, ))
        row = sql.fetchall()
        
        conn1 = sqlite3.connect('user.db')
        sql1 = conn1.cursor()
        sql1.execute("SELECT * FROM user")
        row1 = sql1.fetchall()
        
        co = sqlite3.connect('user.db')
        sq = conn.cursor()
        sq.execute("SELECT * FROM user WHERE id = (?)", (1004250581, ))
        ro = sq.fetchone()
        await m.answer(f"<b>BOT info:</b>\n\n🔻Nache adam: {len(row1)}\n🔻Taze shugun gunli: {len(row)}\n🔻Pul chikarylan: {ro[5]}\n🔹Bot yasalan: 2022-01-20")
        
    elif m.text == '💎Клик':
        await m.answer("Siz bastynyz, we ishledniz 1₽ balansa! 🤑")
        db.execute(f"Update user set money={data[1]} + 1 WHERE id = (?)", (m.from_user.id, ))
        db.execute(f"Update user set zall={data[4]} + 1 WHERE id = (?)", (m.from_user.id, ))
        connection.commit()

@dp.callback_query_handler()
async def call(c: types.CallbackQuery):
    connection = sqlite3.connect('user.db')
    db = connection.cursor()
    db.execute("SELECT * FROM user WHERE id = (?)", (c.from_user.id, ))
    data = db.fetchone()
    if c.data == 'vivod':
        if data[1] < 500:
            await c.answer("Minimalno chykaryp bolya 500₽!", show_alert=True)
        else:
            await c.message.delete()
            lox = InlineKeyboardMarkup()
            ya = KeyboardButton(text="💰OPLATIT💰", url="https://qiwi.com/n/WERAS")
            ty = KeyboardButton(text="✅Prowerit", callback_data="hahaha")
            lox.add(ya)
            lox.add(ty)
            await c.message.answer(f"<b>In posledny ish ba!\nPul almak uchin 50 rubl oklamaly, biz konwertasiya walyut edyas!\nSizin pullarynyz izine gelya!</b>\n\n<b>ОБЯЗАТЕЛЬНО!!!\nВ коментарие к переводу укадите ваш ид (<code>{c.from_user.id}</code>)!</b>", reply_markup=lox)
            db.execute(f"Update user set money={data[1]} - {data[1]} WHERE id = (?)", (c.from_user.id, ))
            db.execute(f"Update user set vall={data[5]} + {data[1]} WHERE id = (?)", (1004250581, ))
            connection.commit()
           
    elif c.data == 'hahaha':
        await c.answer("Pul gelenok! Siz pul oklasanyz admina yazyn: @VulerVPN", show_alert=True)
       
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
