# -*- coding: utf-8 -*-
from parser import build_min_games_list
from auth import api_tg_key
from json import loads
from time import strftime, ctime
from os.path import exists
from os import makedirs
import logging
from aiogram import Bot, Dispatcher, executor, types, exceptions, asyncio
from wiki import get_country_code
import sqlite3


def check_db(filename):
    return exists(filename)


def logs_creator():
    if exists('./logs') == False:
        makedirs('logs')
    logging.basicConfig(level=logging.INFO,
                        filename=f'./logs/EGSBOT.log', datefmt='[%a, %c]')


bot = Bot(api_tg_key)
dp = Dispatcher(bot)


print(exceptions)


def update_user_table(message):
    db_file = f'database.db'
    schema_file = f'schema.sql'

    with open(schema_file, 'r') as rf:
        # Read the schema from the file
        schema = rf.read()

    with sqlite3.connect(db_file) as conn:
        print(f'[{ctime()}]Created the connection!')
        # Execute the SQL query to create the table
        conn.executescript(schema)
        print(f'[{ctime()}] Created the Table! Now inserting')
        conn.executescript(f"""
                        insert into users_data (user_name, user_id, country_code)
                        values
                        ({message.from_user.full_name}, {message.from_user.id}, {message.text})
                        """)
        print(f'[{ctime()}] Inserted values into the table!')
    print(f'[{ctime()}] Closed the connection!')


def main():
    logs_creator()
    executor.start_polling(dp, skip_updates=True)


@dp.message_handler(commands=['start'])
async def start_help_message(message: types.Message):
    await message.reply(f'Hello, {message.from_user.first_name}!\nThis is Auto notiefier bot. It will be notify you about new free promotions from Epic Games Store!\nThere is also code on [Github](https://github.com/Wyndace/EGSFreeGamesNotifierBot)\nEnjoy!', parse_mode='markdown')
    print()


@dp.errors_handler(exception=exceptions.BotBlocked)
async def error_bot_blocked(update: types.Update, exception: exceptions.BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(
        f"[{ctime()}] Hello, Wyndace! I have gotten the {exception}, from {update}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True


@dp.errors_handler(exception=exceptions.BotKicked)
async def error_bot_blocked(update: types.Update, exception: exceptions.BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(
        f"[{ctime()}] Hello, Wyndace! I have gotten the {exception}\nfrom {update}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True

if __name__ == "__main__":
    main()
