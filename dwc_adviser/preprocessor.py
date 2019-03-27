from abc import ABC, abstractmethod
from sklearn.feature_extraction.text import TfidfVectorizer


class Preprocessor:
    def __init__(self):
        self.VOCABULARY_PATH = 'vocab.txt'

        self.tokenizer_uni = TfidfVectorizer(ngram_range=(1, 1), token_pattern=r'\w+').build_analyzer()
        self.tokenizer_bi = TfidfVectorizer(ngram_range=(2, 2), token_pattern=r'\w+').build_analyzer()
        self.existing_words = self.read_vocabulary(self.VOCABULARY_PATH)

    def read_vocabulary(self, vocabulary_path):
        ex_words = set()
        with open(vocabulary_path, 'r') as inf:
            for line in inf:
                ex_words.add(line.strip())
        return ex_words
    
    def word_exists(self, word):
        return word in self.existing_words
    
    def form_exists(self, forms):
        for form in forms:
            if self.word_exists(form):
                return True
        return False
        
    def tokenize(self, text, n_grams=1):
        if n_grams == 1:
            return self.tokenizer_uni(text)
        else:
            return self.tokenizer_bi(text)
    

class Analyzer(ABC):
    def __init__(self):
        self.preprocessor = Preprocessor()
    
    @abstractmethod
    def analyzer(self, text):
        pass


class SimpleAnalyzer(Analyzer):
    def analyzer(self, text):
        return self.preprocessor.tokenize(text)
