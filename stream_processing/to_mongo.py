import pymongo


def add_dataset(dataset):
    myclient = pymongo.MongoClient(
        "mongodb://cbs:GcAlY5l5yt2CHTacnq4F@devcluster-shard-00-00-ayh0j.mongodb.net:27017,devcluster-shard-00-01-ayh0j.mongodb.net:27017,devcluster-shard-00-02-ayh0j.mongodb.net:27017/test?ssl=true&replicaSet=DevCluster-shard-0&authSource=admin&retryWrites=true")
    cbs_db = myclient["cbs"]
    instagram = cbs_db["instagram"]

    for index, row in dataset.iterrows():
        if instagram.find({'url': row['url']}).count() > 0: continue

        data = {
            'datum': row['datum'],
            'url': row['url'],
            'sentiment': row['sentiment'],
            'discussielengte': row['discussielengte'],
            'views': row['views'],
            'GPS breedtegraad': row['GPS breedtegraad'],
            'GPS lengtegraad': row['GPS lengtegraad'],
            'bericht tekst': row['bericht tekst'],
            'likes count': row['likes count'],
            'datum utc': row['datum utc'],
            'hashtags': row['hashtags'],
        }

        instagram.insert_one(data)

