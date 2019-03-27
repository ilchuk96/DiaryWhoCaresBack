from movie_data import MovieData
from adviser import RandomAdviser, TfidfAdviser


class MainAdviser:
    def __init__(self):
        self.MOVIE_DATA_CSV = 'movie_data.csv'

        self.movie_data = MovieData()
        self.movie_data.load_csv(self.MOVIE_DATA_CSV)

        self.adviser = TfidfAdviser(self.movie_data)

    def make_suggestion(self, diary_entry):
        return self.adviser.make_suggestion(diary_entry)
