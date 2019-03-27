import csv
from abc import ABC, abstractmethod
import random


class Adviser(ABC):
    def __init__(self, movie_data):
        self.movie_data = movie_data
    
    @abstractmethod
    def make_suggestion(self, diary_entry):
        pass
    
class RandomAdviser(Adviser):
    def make_suggestion(self, diary_entry):
        magic = random.randrange(1, len(self.movie_data))
        return self.movie_data.get_title(magic)
