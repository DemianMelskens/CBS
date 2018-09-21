import pandas as pd

insta = pd.read_csv('../data/joined.csv', ';')

dicts = []

with open('../data/stopwords-nl.txt', 'r') as f:
    dicts.extend(f.read().splitlines())

with open('../data/stopwords-eng.txt', 'r') as f:
    dicts.extend(f.read().splitlines())

words_to_remove = []

for word in dicts:
    if word.isalpha():
        words_to_remove.append(word)

insta = pd.read_csv('../data/joined.csv', ';')

insta['bericht tekst'] = insta['bericht tekst'].astype(str)
insta['bericht tekst'] = insta['bericht tekst'].str.strip()
insta['bericht tekst'] = insta['bericht tekst'].str.lower()

insta['bericht tekst'] = insta['bericht tekst'].replace(r',', '', regex=True)
insta['bericht tekst'] = insta['bericht tekst'].replace('\.', '', regex=True)

for word in words_to_remove:
    insta['bericht tekst'] = insta['bericht tekst'].replace('(?:^|\W)'+ word + '(?:$|\W)', ' ', regex=True)

all_words = []

for i, row in insta.iterrows():
    words = row['bericht tekst'].split(' ')
    all_words.extend(words)

clean_words = []

for word in all_words:
    if word.isalpha():
        clean_words.append(word.strip())

clean_words = pd.Series(clean_words)
print(clean_words.value_counts())

# TODO: Keep only clean words in dataset
