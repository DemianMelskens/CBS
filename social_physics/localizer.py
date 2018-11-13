import pymongo
import pandas as pd
from geopy.geocoders import Nominatim
import math
from time import sleep


def update_location(data):
    myclient = pymongo.MongoClient(
        "mongodb://cbs:GcAlY5l5yt2CHTacnq4F@devcluster-shard-00-00-ayh0j.mongodb.net:27017,devcluster-shard-00-01-ayh0j.mongodb.net:27017,devcluster-shard-00-02-ayh0j.mongodb.net:27017/test?ssl=true&replicaSet=DevCluster-shard-0&authSource=admin&retryWrites=true")
    cbs_db = myclient["cbs"]
    instagram = cbs_db["instagram"]

    for index, row in data.iterrows():
        lat = row['GPS breedtegraad']
        lon = row['GPS lengtegraad']

        town, country = getplace(lat, lon)
        instagram.find({'url': row['url']})

        myquery = {"url": row['url']}
        newvalues = {"$set": {"town": town, "country": country}}

        instagram.update_one(myquery, newvalues)
    pass


def getplace(lat, lon):
    if math.isnan(lat) or math.isnan(lon):
        return "unknown", "unknown"
    geolocator = Nominatim(user_agent="fontys-cbs-instagram")
    location = geolocator.reverse("{}, {}".format(lat, lon))
    sleep(2)
    if 'error' in location.raw.keys():
        print('Error', "{}, {}".format(lat, lon))
        return "unknown", "unknown"
    if 'city' in location.raw['address'].keys():
        town = location.raw['address']['city']
    elif 'town' in location.raw['address'].keys():
        town = location.raw['address']['town']
    else:
        town = 'unknown'
    country = location.raw['address']['country']
    return town, country


while (True):
    try:
        myclient = pymongo.MongoClient(
            "mongodb://cbs:GcAlY5l5yt2CHTacnq4F@devcluster-shard-00-00-ayh0j.mongodb.net:27017,devcluster-shard-00-01-ayh0j.mongodb.net:27017,devcluster-shard-00-02-ayh0j.mongodb.net:27017/test?ssl=true&replicaSet=DevCluster-shard-0&authSource=admin&retryWrites=true")
        cbs_db = myclient["cbs"]
        instagram = cbs_db["instagram"]
        df = pd.DataFrame(list(instagram.find({"town": {"$exists": False}}).limit(10)))
        print('Next batch')
        update_location(df)
    except Exception as e:
        print(e)
