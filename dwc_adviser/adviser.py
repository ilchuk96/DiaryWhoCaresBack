from dwc_adviser.preprocessor import SimpleAnalyzer
import random
import numpy as np
from abc import ABC, abstractmethod
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances


class Adviser(ABC):
    def __init__(self, movie_data):
        self.movie_data = movie_data
    
    @abstractmethod
    def make_suggestion(self, diary_entry, n_sugg=5):
        pass
    
class RandomAdviser(Adviser):
    def make_suggestion(self, diary_entry, n_sugg=5):
        magic = [random.randrange(1, len(self.movie_data)) for _ in range(n_sugg)]
        return [self.movie_data.titles[i] for i in magic]
    
class TfidfAdviser(Adviser):
    def __init__(self, movie_data):
        super().__init__(movie_data)
        self.tfidf_vectorizer = TfidfVectorizer(min_df=5, max_df=0.9, analyzer=SimpleAnalyzer().analyzer)
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.movie_data.texts)
    
    def make_suggestion(self, diary_entry, n_sugg=5):
        distances = euclidean_distances(self.tfidf_vectorizer.transform([diary_entry]), self.tfidf_matrix)
        ixs = np.argsort(distances)[0][:n_sugg]
        return [self.movie_data.titles[i] for i in ixs]
