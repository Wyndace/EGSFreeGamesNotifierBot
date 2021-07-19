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


def logs_creator():
    if exists('./logs') == False:
        makedirs('logs')
    logging.basicConfig(level=logging.INFO,
                        filename=f'./logs/EGSBOT.log', datefmt='[%a, %c]')


bot = Bot(api_tg_key)
dp = Dispatcher(bot)


print(exceptions)


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
