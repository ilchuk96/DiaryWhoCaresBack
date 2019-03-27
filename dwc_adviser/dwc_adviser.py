from dwc_adviser.movie_data import MovieData
from dwc_adviser.adviser import RandomAdviser


class MainAdviser:
    def __init__(self):
        self.MOVIE_DATA_CSV = 'dwc_adviser/movie_data.csv'

        self.movie_data = MovieData()
        self.movie_data.load_csv(self.MOVIE_DATA_CSV)

        self.adviser = RandomAdviser(self.movie_data)

    def make_suggestion(self, diary_entry):
        return self.adviser.make_suggestion(diary_entry)
