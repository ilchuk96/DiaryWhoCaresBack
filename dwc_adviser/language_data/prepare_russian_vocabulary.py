from tqdm import tqdm

print('Start reading OpenCorpora vocabulary..')

corp = set()
with open('dict.opcorpora.txt', 'r') as inf:
    for line in inf:
        line = line.strip()
        if line == '':
            continue
        tokens = line.split()
        if len(tokens) == 1:
            continue
        word = tokens[0].lower()
        corp.add(word)

with open('../russian_vocabulary.txt', 'w') as ouf:
    for word in tqdm(corp):
        ouf.write(word + '\n')

print('Russian vocabulary collected.')
