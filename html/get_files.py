import shutil
import requests
from bs4 import BeautifulSoup
import bs4
import os.path
import re
import json

starting_ind = 0
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
        if os.path.isdir('0-9/' + movie_title):
            print("Уже записано.")
            continue

        film_url = wiki_url + movie_link
        with requests.get(film_url) as film_r:
            film = BeautifulSoup(film_r.text)

        description = film.find('div', {'class': 'mw-parser-output'}).find('p')
        description = re.sub('<.*?>|[.*?]', '', description.text)

        cur = film.h2
        found = False
        plot = ''
        while cur is not None:
            if not isinstance(cur, bs4.NavigableString) and cur.find('span', {'id': 'Сюжет'}) is not None:
                found = True
                cur = cur.next
                continue
            if found and cur.name == 'p':
                plot += str(cur)
            if found and cur.name == 'h2':
                break
            cur = cur.next
        plot = re.sub('<.*?>|[.*?]|Сюжет|В ролях', '', plot)
        os.mkdir(letter + '/' + movie_title)

        ans = {'id': movie_title, 'title': movie_title, 'description': description, 'plot': plot}
        with open(letter + '/' + movie_title + '/' + movie_title + '.json', 'w') as output_file:
            json.dump(ans, output_file, ensure_ascii=False)

        img = film.find('img', {'alt': 'Постер фильма'})
        if img is not None:
            img_url = 'http:' + img.get('src')
            extension = img_url.split('.')[-1]
            response = requests.get(img_url, stream=True)
            with open(letter + '/' + movie_title + '/' + movie_title + '.' + extension, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

        print('Записано.')
