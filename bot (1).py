import time
import configparser
import os

from pyrogram import Client, filters, types, enums
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.errors.exceptions.forbidden_403 import Forbidden
from pyrogram.types import Chat


def parse_config():
    config_list = {}
    index = 0
    for root, dirs, files in os.walk('..'):
        for file in files:
            if file.split(".")[-1] == "ini":
                config_list[index] = file.split(".")[0]
                index += 1
    return config_list


API_ID = 19309010
API_HASH = "dfdf154157cca400bd53b00100468fa5"

config_list = parse_config()
name_config = config_list[int(input(f"Список конфигов: {parse_config()}\nНапиши цифру: "))]

config = configparser.ConfigParser()
config.read(name_config + ".ini", encoding="cp1251")

NAME_SESSION = config["INFO"]["NAME_SESSION"]
TIME = float(config["INFO"]["TIME"])
PROMT = config["INFO"]["PROMT"]
USERNAME_BOT = "@dvdafdfasdvsdafv_bot"

app = Client(NAME_SESSION, api_id=API_ID, api_hash=API_HASH, parse_mode=enums.parse_mode.ParseMode.HTML)


@app.on_message(filters.channel)
async def get_post(client, message: types.Message):
    chat_id = message.chat.id
    message_id = message.id
    print(message_id)
    await app.send_message(USERNAME_BOT, f"""Пост из канала {chat_id} {message_id}|:
                    
{message.text.replace('"', '')}

{PROMT}""")


@app.on_message(filters.bot)
async def response(client, message: types.Message):
    response_text = message.reply_to_message.text.replace(PROMT, "").split('|:\n', 2)[0].replace('Пост из канала ',
                                                                                                 '').replace('\n', '')
    chat_id, message_id = response_text.split(' ', 2)[0], int(response_text.split(' ', 2)[1])
    try:
        msg = await app.get_discussion_message(chat_id, message_id)
        await msg.reply(text=message.text, quote=True)
        print(f"[+] Отправил пост в {chat_id}")
    except ChannelPrivate:
        try:
            await app.leave_chat(chat_id)
        except Exception as e:
            print(f"Не страшная ощибка: {e}")

        for i in ["/start", "OK", "/start"]:
            await app.send_message('@spambot', i)
            time.sleep(3)
    except Forbidden:
        chat: Chat
        try:
            chat = await app.get_chat(chat_id)
            await chat.linked_chat.join()
        except Exception as e:
            print('Не удалось вступить в чат', e)
    except Exception as e:
        print('Хуй знает какая ошибка', e)

    time.sleep(TIME)


app.run()
