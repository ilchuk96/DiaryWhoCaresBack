import requests
from bs4 import BeautifulSoup
import bs4


wiki_url = 'http://ru.wikipedia.nom.al'
with requests.get(wiki_url + '/wiki/Категория:Фильмы_по_алфавиту') as r:
    soup = BeautifulSoup(r.text)
film_list = soup.find('div', {'class': 'mw-content-ltr'})
items = film_list.find_all('li')
for item in items:
    try:
        if item.find('div', {'class': 'CategoryTreeSection'}):
            continue
        movie_link = item.find('a').get('href')
        movie_title = item.find('a').get('title')
        film_url = wiki_url + movie_link
        print(film_url)
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
            if found:
                ans += str(cur)
            if cur.name == 'h2':
                break
            cur = cur.next
        print(ans)
        break
        with open('0-9/' + movie_title, 'w') as output_file:
            output_file.write(text.text)
    except Exception as e:
        print(e)
