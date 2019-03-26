import requests
from bs4 import BeautifulSoup
import bs4
import os.path
import re

starting_ind = 1
pages = ['0-9', 'А', 'Б', 'В', 'Г', 'Д', 'Ж', 'У', 'З', 'И', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
         'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
wiki_url = 'http://ru.wikipedia.nom.al'
for letter in pages[starting_ind:]:
    print('Текущая буква: ' + letter)
    if letter == '0-9':
        letter_url = '/wiki/Категория:Фильмы_по_алфавиту'
    else:
        letter_url = '/w/index.php?title=Категория:Фильмы_по_алфавиту&from=' + letter
    with requests.get(wiki_url + letter_url) as r:
        soup = BeautifulSoup(r.text)
    film_list = soup.find('div', {'class': 'mw-content-ltr'})
    items = film_list.find_all('li')
    if not os.path.isdir(letter):
        os.mkdir(letter)
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
        with open(letter + '/' + movie_title, 'w') as output_file:
            output_file.write(ans)
        print('Записано.')
