from instaloader import Post
import instaloader
import re
import numpy as np


# Download all posts from instagram using an array of urls
def get_posts(urls):
    posts_dict = {}
    L = instaloader.Instaloader()
    for index, url in enumerate(urls):
        shortcode = url.split("/")[-2]

        # time.sleep(0.1)
        try:
            post = Post.from_shortcode(L.context, url.split("/")[-2])
            posts_dict[shortcode] = post
        except:
            pass

    return posts_dict


# Get the indexes of the posts which do not exist anymore
def get_non_exsisting_posts(dataset, posts_dict):
    indexes_to_drop = []

    for index, row in dataset.iterrows():
        shortcode = row['url'].split("/")[-2]
        if not shortcode in posts_dict:
            indexes_to_drop.append(index)

    return indexes_to_drop


# Delete posts from the dataset based on an array of indexes
def del_posts(data, indexes_to_drop):
    for index in indexes_to_drop:
        data = data.drop(index=index, axis=0)
    return data


# Enrich dataset with like count
def add_like_count_to_dataset(dataset, posts_dict):
    for index, row in dataset.iterrows():
        shortcode = row['url'].split("/")[-2]
        if shortcode in posts_dict:
            dataset.at[index, 'likes count'] = posts_dict[shortcode].likes
    return dataset


# Adds utc date to the dataset
def add_date_utc(dataset, posts_dict):
    for index, row in dataset.iterrows():
        shortcode = row['url'].split('/')[-2]
        if shortcode in posts_dict:
            dataset.at[index, 'datum utc'] = posts_dict[shortcode].date_utc

    return dataset


# Refreshes comment count
def refresh_comment_count(dataset, posts_dict):
    for index, row in dataset.iterrows():
        shortcode = row['url'].split('/')[-2]
        if shortcode in posts_dict:
            dataset.at[index, 'discussielengte'] = posts_dict[shortcode].comments

    return dataset


# Refreshes view count
def refresh_views(dataset, posts_dict):
    for index, row in dataset.iterrows():
        shortcode = row['url'].split('/')[-2]
        if shortcode in posts_dict:
            dataset.at[index, 'views'] = posts_dict[shortcode].likes

    return dataset


def improve_sentiment(dataset):
    dataset['sentiment'] = dataset['sentiment'].replace(np.nan, '0')

    return dataset


def isolate_hashtag(data):
    total_hashtags = []
    for index, row in data.iterrows():
        text = row['bericht tekst']

        # find all hashtags in text and isolate them in new column
        total_hashtags.append(' '.join(re.findall(r"#(\w+)", text)))

        # remove hashtags from text
        pattern = re.compile("#(\w+)")
        newText = pattern.sub(r'', text)
        data.at[index, 'bericht tekst'] = newText

    data['hashtags'] = total_hashtags
    return data


def remove_emoji(data):
    indexes_to_drop = []

    for index, row in data.iterrows():
        a = row['bericht tekst']

        # todo: vul aan met meer emoji's
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        newValue = emoji_pattern.sub(r'', a)
        newValue = newValue.replace('🥗', '')
        if newValue == '':
            indexes_to_drop.append(index)

        else:
            data.at[index, 'bericht tekst'] = newValue

    pass
    data = del_posts(data, indexes_to_drop)
    return data


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


# Cleans invalid urls and enriches with like count, data utc, comment count and view count
def clean_und_enrich(dataset):
    dataset = dataset.drop(['zoekopdracht', 'type', 'volgers', 'invloed', 'titel', 'type bron'], axis=1)
    dataset = improve_sentiment(dataset)
    dataset = remove_emoji(dataset)
    posts_dict = get_posts(dataset['url'])
    indexes_to_drop = get_non_exsisting_posts(dataset, posts_dict)
    dataset = del_posts(dataset, indexes_to_drop)
    dataset = add_like_count_to_dataset(dataset, posts_dict)
    dataset = add_date_utc(dataset, posts_dict)
    dataset = refresh_comment_count(dataset, posts_dict)
    dataset = refresh_views(dataset, posts_dict)
    dataset = isolate_hashtag(dataset)
    dataset = clean_words(dataset, load_dicts('../data/'))

    return dataset
