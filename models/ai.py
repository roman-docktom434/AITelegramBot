import time
from parsing.parsing_a_news import news_parser


async def reporter(url, client):
    async for text, photo, date, link in news_parser(url):

        response_from_reporter = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Ты высококачеcтвенный репортер. Твоя задача кратко и ясно сократить новость. Вот новость: {text}. В ответе я хочу видеть только текст, ничего не более. Не используй Markdown.",
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        print(f"[LOG] [{time.strftime('%H:%M:%S')}] Репортер ответил. Переходим к копирайтеру...")
        yield response_from_reporter.choices[0].message.content, photo, date, link


async def copywriter(url, client):
    async for response_from_reporter, photo, date, link in reporter(url, client):
        response_from_copywriter = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Ты высококачеcтвенный копирайтер. Твоя задача разбить текст на абзацы по смыслу. Вот твой текст: {response_from_reporter}. В ответе я хочу видеть только граммотный и орфограческий правильный текст, ничего не более. Не используй Markdown.",
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        yield response_from_copywriter.choices[0].message.content, photo, date, link


