import os
import dotenv
dotenv.load_dotenv()
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models.ai import copywriter
from groq import Groq


BOT_TOKEN = os.getenv("BOT_TOKEN")
RIA_URL = os.getenv("RIA_URL")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = os.getenv("ADMIN_ID")
API_KEY = os.getenv("API_KEY")

client = Groq(
    api_key=os.environ.get("API_KEY"),
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def monitoring(url):
    while True:
        try:
            async for text, photo, date, link in copywriter(url, client):
                if photo:
                    sent_message = await bot.send_photo(
                        chat_id=f"@{CHANNEL_ID}",
                        photo=photo,
                        caption=f"{text}\n\n✨<a href='https://t.me/{CHANNEL_ID}'>Свежесть | Подписаться</a>",
                        parse_mode="HTML"
                    )
                else:
                    sent_message = await bot.send_message(
                        chat_id=f"@{CHANNEL_ID}",
                        text=f"{text}\n\n✨<a href='https://t.me/{CHANNEL_ID}'>Свежесть | Подписаться</a>",
                        parse_mode="HTML"
                    )

                post_id = sent_message.message_id
                post_url = f"https://t.me/{CHANNEL_ID}/{post_id}"

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="👀 Посмотреть пост", url=post_url)]
                ])

                await bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"✅ Пост опубликован!\n\nВремя парсинга: {date},\nСсылка на оригинал: {link}",
                    reply_markup=keyboard
                )
        except Exception as e:
                    print(f"Ошибка в мониторинге: {e}")
                    await asyncio.sleep(5)
async def main():
    asyncio.create_task(monitoring(RIA_URL))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())