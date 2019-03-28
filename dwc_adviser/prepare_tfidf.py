from preprocessor import Preprocessor
from collections import defaultdict
import csv
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer


print('Reading words..')
all_words = defaultdict(int)
with open('movie_data.csv', 'r') as inf:
    reader = csv.reader(inf, delimiter=';')
    header = {v : i for i, v in enumerate(next(reader))}
    for row in reader:
        text = row[header['description']] + '\n' + row[header['plot']]
        tokens = set(TfidfVectorizer(ngram_range=(1, 1), token_pattern=r'\w+').build_analyzer()(text))
        for t in tokens:
            all_words[t] += 1

print('Removing rare words..')
min_df = 5
freq_words = []
for w in tqdm(all_words):
    if all_words[w] >= min_df:
        freq_words.append(w)
print(len(freq_words))
# print(sorted(all_words))

print('Removing non-existing words..')
preproc = Preprocessor(vocabulary_path='russian_vocabulary.txt')
ex_filtered = preproc.filter_not_existing(freq_words)
print(len(ex_filtered))
#print(sorted(ex_filtered))

print('Removing non-semantic part-of-speech..')
pos_filtered = preproc.filter_pos(ex_filtered)
print(len(pos_filtered))
#print(sorted(pos_filtered))

print('Normalizing words..')
normalized = preproc.normalize(pos_filtered)
print(len(normalized))
# print(sorted(normalized))

print('Writing full vocabulary..')
with open('tfidf_vocabulary.txt', 'w') as ouf:
    for w in sorted(pos_filtered):
        ouf.write(w + '\n')

print('Writing normalized tfidf vocabulary..')
with open('tfidf_vocabulary_norm.txt', 'w') as ouf:
    for w in sorted(normalized):
        ouf.write(w + '\n')
