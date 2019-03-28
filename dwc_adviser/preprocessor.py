from abc import ABC, abstractmethod
from sklearn.feature_extraction.text import TfidfVectorizer
from pymorphy2 import MorphAnalyzer
from tqdm import tqdm


def read_vocabulary(vocabulary_path):
    print('Reading russian vocabulary..')
    ex_words = set()
    with open(vocabulary_path, 'r') as inf:
        for line in inf:
            ex_words.add(line.strip())
    return ex_words


class Preprocessor:
    def __new__(cls, vocabulary_path='dwc_adviser/russian_vocabulary.txt'):
        if not getattr(cls, 'instance', None):
            obj = super().__new__(cls)

            obj.tokenizer_uni = TfidfVectorizer(ngram_range=(1, 1), token_pattern=r'\w+').build_analyzer()
            obj.tokenizer_bi = TfidfVectorizer(ngram_range=(2, 2), token_pattern=r'\w+').build_analyzer()

            obj.existing_words = read_vocabulary(vocabulary_path)

            obj.morpher = MorphAnalyzer()
            obj.stop_pos = ['NUMR', 'NPRO', 'PREP', 'CONJ', 'PRCL']
            
            cls.instance = obj
        return cls.instance

    def __init__(self, *args, **kwargs):
        pass

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
        
    def filter_pos(self, words):
        res = []
        for w in tqdm(words):
            p = self.morpher.parse(w)[0]
            if p.tag.POS not in self.stop_pos:
                res.append(w)
        return res
    
    def filter_not_existing(self, words):
        res = []
        for w in tqdm(words):
            ps = self.morpher.parse(w)
            forms = set([w])
            for p in ps:
                forms.add(p.normal_form)
            if self.form_exists(forms):
                res.append(w)
        return res
    
    def normalize(self, words):
        res = set()
        for w in tqdm(words):
            p = self.morpher.parse(w)[0]
            res.add(p.normal_form)
        return list(res)
    
    def normal_form(self, word):
        if word in self.normal_forms:
            return self.normal_forms[word]
        else:
            return word
        
    def normalize_word(self, word):
        return self.morpher.parse(word)[0].normal_form

    def normalize_text(self, text):
        return ' '.join(map(self.normalize_word, SimpleAnalyzer().analyzer(text)))
    
    def cache_normal_forms(self):
        if not getattr(self, 'normal_forms', None):
            words = []
            with open('dwc_adviser/tfidf_vocabulary.txt', 'r') as inf:
                for line in inf:
                    words.append(line.strip())
            self.normal_forms = {}
            print('Caching normal forms..')
            for w in tqdm(words):
                if w not in self.normal_forms:
                    self.normal_forms[w] = self.morpher.parse(w)[0].normal_form
    

class Analyzer(ABC):
    def __init__(self):
        self.preprocessor = Preprocessor()
    
    @abstractmethod
    def analyzer(self, text):
        pass


class SimpleAnalyzer(Analyzer):
    def analyzer(self, text):
        return self.preprocessor.tokenize(text)

    
class NormalizedAnalyzer(Analyzer):
    def __init__(self):
        super().__init__()
        self.preprocessor.cache_normal_forms()
    
    def analyzer(self, text):
        words = self.preprocessor.tokenize(text)
        return list(map(self.preprocessor.normal_form, words))
