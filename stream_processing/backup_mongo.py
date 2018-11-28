import pymongo
import pandas as pd

myclient = pymongo.MongoClient(
        "mongodb://cbs:GcAlY5l5yt2CHTacnq4F@devcluster-shard-00-00-ayh0j.mongodb.net:27017,devcluster-shard-00-01-ayh0j.mongodb.net:27017,devcluster-shard-00-02-ayh0j.mongodb.net:27017/test?ssl=true&replicaSet=DevCluster-shard-0&authSource=admin&retryWrites=true")
cbs_db = myclient["cbs"]

df = pd.DataFrame(list(cbs_db["instagram"].find()))
del df['_id']

df.to_csv('./backup.csv', sep=';')