import os
import csv
import json
from tqdm import tqdm as tqdm


MOVIE_JSON_PATH = './movies'

def get_movie_names():
    return os.listdir(MOVIE_JSON_PATH)


def build_csv_from_movie_data():
    header = ['id', 'title', 'description', 'plot', 'good_description']
    with open('movie_data.csv', 'w') as ouf:
        writer = csv.writer(ouf, delimiter=';')
        writer.writerow(header)
        
        current_id = 0
        movie_names = get_movie_names()
        for movie_name in tqdm(movie_names):
            with open(f'{MOVIE_JSON_PATH}/{movie_name}') as movie_json:
                movie_data_dict = json.load(movie_json)
                if len(movie_data_dict) < 4:
                    continue
                movie_data_list = [current_id, 
                                   movie_data_dict['title'].strip(),
                                   movie_data_dict['description'].strip(),
                                   movie_data_dict['plot'].strip(),
                                   0]
                if len(movie_data_dict['plot']) > 1000:
                    movie_data_list[-1] = 1
                current_id += 1
                writer.writerow(movie_data_list)

print('Start loading movie data..')
build_csv_from_movie_data()
print('Movie data collected.')
