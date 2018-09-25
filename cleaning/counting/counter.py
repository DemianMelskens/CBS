import pandas as pd


# Loads dictionaries with words to remove from the given path
def load_dicts(path):
    dicts = []

    with open(path + 'stopwords-nl.txt', 'r') as f:
        dicts.extend(f.read().splitlines())

    with open(path + 'stopwords-eng.txt', 'r') as f:
        dicts.extend(f.read().splitlines())

    return dicts


# Cleans wrong and non alphabetic words from the dataset
def clean_words(dataset, wrong_words):
    dataset['bericht tekst'] = dataset['bericht tekst'].astype(str)
    dataset['bericht tekst'] = dataset['bericht tekst'].str.strip()
    dataset['bericht tekst'] = dataset['bericht tekst'].str.lower()

    dataset['bericht tekst'] = dataset['bericht tekst'].replace(r',', '', regex=True)
    dataset['bericht tekst'] = dataset['bericht tekst'].replace('\.', '', regex=True)

    for i, row in dataset.iterrows():
        words = row['bericht tekst'].split(' ')
        clean_words = []
        for word in words:
            if word.isalpha() and not any(word in d for d in wrong_words):
                clean_words.append(word)

        dataset.at[i, 'bericht tekst'] = ' '.join(clean_words)

    return dataset


insta = clean_words(pd.read_csv('../data/joined.csv', ';'),
                    load_dicts('../data/'))

all_words = []

for i, row in insta.iterrows():
    all_words.extend(
        row['bericht tekst'].split(' '))

all_words = pd.Series(all_words)
print(all_words.value_counts())
