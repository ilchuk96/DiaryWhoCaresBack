import requests
from bs4 import BeautifulSoup
import bs4
import os.path
import re

wiki_url = 'http://ru.wikipedia.nom.al'
with requests.get(wiki_url + '/wiki/Категория:Фильмы_по_алфавиту') as r:
    soup = BeautifulSoup(r.text)
film_list = soup.find('div', {'class': 'mw-content-ltr'})
items = film_list.find_all('li')
for item in items:
    if item.find('div', {'class': 'CategoryTreeSection'}):
        continue
    movie_link = item.find('a').get('href')
    movie_title = item.find('a').get('title').replace('/', '\\')
    if os.path.isfile('0-9/' + movie_title):
        print("Уже записано.")
        continue
    film_url = wiki_url + movie_link
    with requests.get(film_url) as film_r:
        film = BeautifulSoup(film_r.text)
        cur = film.h2
        found = False
        ans = ''
        while cur is not None:
            if not isinstance(cur, bs4.NavigableString) and cur.find('span', {'id': 'Сюжет'}) is not None:
                found = True
                cur = cur.next
                continue
            if found and cur.name == 'p':
                ans += str(cur)
            if found and cur.name == 'h2':
                break
            cur = cur.next
    ans = re.sub('<.*?>|[.*?]|Сюжет|В ролях', '', ans)
    with open('0-9/' + movie_title, 'w') as output_file:
        output_file.write(ans)
    print('Записано.')
