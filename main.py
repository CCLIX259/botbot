import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = ""
CHAT_GPT_TOKEN = ""

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def chat_gpt(message):
    openai.api_key = CHAT_GPT_TOKEN
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return completion.choices[0].text


@dp.message_handler()
async def process_start_command(message: types.Message):
    await message.reply(chat_gpt(message.text))

if __name__ == '__main__':
    executor.start_polling(dp)
