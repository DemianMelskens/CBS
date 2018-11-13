import pymongo
import pandas as pd


def count_words(data):
    all_words = []

    for i, row in data.iterrows():
        all_words.extend(
            row['bericht tekst'].split(' '))

    all_words = pd.Series(all_words)
    print(all_words.value_counts())


def count_hashtags(data):
    all_words = []

    for i, row in data.iterrows():
        all_words.extend(
            row['hashtags'].split(' '))

    all_words = pd.Series(all_words)
    print(all_words.value_counts())


def count_countries(data):
    all_words = []

    for i, row in data.iterrows():
        all_words.append(str(row['country']))

    all_words = pd.Series(all_words)
    print(all_words.value_counts())


def count_towns(data):
    all_words = []

    for i, row in data.iterrows():
        all_words.append(str(row['town']))

    all_words = pd.Series(all_words)
    print(all_words.value_counts())


myclient = pymongo.MongoClient(
    "mongodb://cbs:GcAlY5l5yt2CHTacnq4F@devcluster-shard-00-00-ayh0j.mongodb.net:27017,"
    "devcluster-shard-00-01-ayh0j.mongodb.net:27017,"
    "devcluster-shard-00-02-ayh0j.mongodb.net:27017/test?ssl=true&replicaSet=DevCluster-shard-0&authSource=admin"
    "&retryWrites=true")
cbs_db = myclient["cbs"]

# df = pd.DataFrame(list(cbs_db["instagram"].find({"country":"France"})))
df = pd.DataFrame(list(cbs_db["instagram"].find()))
del df['_id']

print('Data loaded')

count_hashtags(df)
