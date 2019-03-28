from dwc_adviser.movie_data import MovieData
from dwc_adviser.adviser import RandomAdviser, TfidfAdviser, TfidfCleanAdviser


class MainAdviser:
    def __init__(self):
        print('Initializing adviser..')

        self.MOVIE_DATA_CSV = 'dwc_adviser/movie_data.csv'

        print('Loading movie data..')
        self.movie_data = MovieData()
        self.movie_data.load_csv(self.MOVIE_DATA_CSV)
        # self.movie_data_good_only = MovieData()
        # self.movie_data_good_only.load_csv(self.MOVIE_DATA_CSV, good_only=True)

        self.adviser = TfidfCleanAdviser(self.movie_data)
        # self.adviser_good_only = TfidfCleanAdviser(self.movie_data_good_only)

        print('Adviser is ready!')

    def make_suggestion(self, diary_entry, n_sugg=5, good_only=False):
        if good_only:
            raise NotImplemented("Good only mode temporarily turned off")
            return self.adviser_good_only.make_suggestion(diary_entry, n_sugg)
        else:
            return self.adviser.make_suggestion(diary_entry, n_sugg)
