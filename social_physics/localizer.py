import pymongo
import pandas as pd
from geopy.geocoders import Nominatim
import math
from time import sleep
import traceback


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


def getplace(lat, lon):
    if math.isnan(lat) or math.isnan(lon):
        return "unknown", "unknown"
    geolocator = Nominatim(user_agent="3478ewjqi238u4dsjiwq3284u9erinjeqwi3248jd")
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

    if 'country' in location.raw['address'].keys():
        country = location.raw['address']['country']
    elif 'country_code' in location.raw['address'].keys():
        if location.raw['address']['country_code'] == 'nl':
            country = 'The Netherlands'
        else:
            raise Exception('Unknown country code')
    else:
        country = 'unknown'

    return town, country


while (True):
    try:
        myclient = pymongo.MongoClient(
            "mongodb://cbs:GcAlY5l5yt2CHTacnq4F@devcluster-shard-00-00-ayh0j.mongodb.net:27017,devcluster-shard-00-01-ayh0j.mongodb.net:27017,devcluster-shard-00-02-ayh0j.mongodb.net:27017/test?ssl=true&replicaSet=DevCluster-shard-0&authSource=admin&retryWrites=true")
        cbs_db = myclient["cbs"]
        instagram = cbs_db["instagram"]
        df = pd.DataFrame(list(instagram.find({"town": {"$exists": False}}).limit(1000)))
        print(df.shape)
        df = df.sample(frac=1).reset_index(drop=True)
        print('Next batch')
        update_location(df)
    except Exception as e:
        print(e)
        traceback.print_exc()
