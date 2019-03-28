import csv


class MovieData:
    def __init__(self):
        self.titles = None
        self.texts = None
        
    def __len__(self):
        return len(self.titles)
        
    def load_csv(self, csvfile, min_length=100, good_only=False):
        with open(csvfile, 'r') as inf:
            reader = csv.reader(inf, delimiter=';')
            header = {v : i for i, v in enumerate(next(reader))}
            titles = []
            texts = []
            for row in reader:
                if good_only:
                    if not int(row[header['good_description']]):
                        continue
                if len(row[header['plot']]) > 100:
                    titles.append(row[header['title']])
                    # texts.append(row[header['description']] + '\n' + row[header['plot']])
                    texts.append(row[header['plot']])
        self.titles = titles
        self.texts = texts
        
    def get_title(self, ix):
        return self.titles[ix]
    
    def get_text(self, ix):
        return self.texts[ix]
