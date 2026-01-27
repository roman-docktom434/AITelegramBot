import requests
from bs4 import BeautifulSoup
import time


# Обновление сайта для поиска новых ссылок
def update_site(url):
    update_time = time.strftime("%H:%M:%S")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    div_class = soup.find('div', class_='list-item__content')
    link = div_class.find('a', class_='list-item__title color-font-hover-only')['href']
    return link


# Сравнение изначальной ссылки и новой
def parsing_links(link, new_link):
    update_time = time.strftime("%H:%M:%S")
    if new_link != link:
        print(f'[LOG] [{update_time}] Найдена новая ссылка! {new_link}')
        return new_link + "," + update_time
    else:
        print(f'[LOG] [{update_time}] Ссылки одинаковы')
        return 'Ссылки одинаковы'  + "," + update_time

# Получение итоговой ссылки. Переназначение начльной ссылки
def start_parsing(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', class_='list-item__content')
    link = div.find('a', class_='list-item__title color-font-hover-only')['href']
    start_time = time.strftime("%H:%M:%S")
    print(f"[LOG] [{start_time}] Изначальная ссылка: {link}")
    yield link, start_time
    while True:
        new_link = update_site(url)
        updated_link = parsing_links(link=link, new_link=new_link)
        datelink = updated_link.split(',')
        yield datelink[0], datelink[1]
        if new_link != link:
            link = new_link
        time.sleep(120)