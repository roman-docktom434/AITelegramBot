import aiohttp
from bs4 import BeautifulSoup
from parsing.parsing_links import start_parsing


# Парсинг текстов и фотографии новости
async def news_parser(url):
    links_data = start_parsing(url)

    async with aiohttp.ClientSession() as session:
        for new in links_data:
            link = new[0]
            date = new[1]

            if "Ссылки одинаковы" in link:
                continue

            try:
                async with session.get(link, timeout=10) as response:
                    if response.status != 200:
                        continue

                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    texts = soup.find_all('div', class_='article__text')
                    if not texts:
                        continue

                    first_paragraph = texts[0].text.split("РИА Новости. ")[-1]
                    other_paragraphs = "\n".join(text.text for text in texts[1:])
                    result = first_paragraph + "\n" + other_paragraphs
                    photo_container = soup.find('div', class_='photoview__open')
                    photo = None
                    if photo_container and photo_container.find('img'):
                        photo = photo_container.find('img')['src']

                    if photo:
                        if photo.startswith('//'):
                            photo = 'https:' + photo
                        if not photo.startswith('http'):
                            photo = None
                        yield result, photo, date, link
                    else:
                        yield result, None, date, link

            except Exception as e:
                print(f"Ошибка при загрузке новости {link}: {e}")