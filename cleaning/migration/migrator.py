import pymongo
from bson.binary import Binary
import instaloader
from instaloader import Post
import requests
import copy
from io import BytesIO
from PIL import Image
from time import sleep


def reset_cloud_migration_fields():
    cbs_db_cloud = pymongo.MongoClient(
        "mongodb://cbs:GcAlY5l5yt2CHTacnq4F@devcluster-shard-00-00-ayh0j.mongodb.net:27017,"
        "devcluster-shard-00-01-ayh0j.mongodb.net:27017,"
        "devcluster-shard-00-02-ayh0j.mongodb.net:27017/test?ssl=true&replicaSet=DevCluster-shard-0&authSource=admin"
        "&retryWrites=true")["cbs"]["instagram"]
    cbs_db_cloud.update_many({}, {"$unset": {"migrated": 1}})


def remove_all_documents_in_ties_db():
    cbs_db_ties = pymongo.MongoClient(
        "mongodb://cbs_user:cbs_pwd@tiestheunissen.nl:27017/test")["test"]["instagram"]
    cbs_db_ties.delete_many({})


def download_insta_picture_from_post(url):
    shortcode = url.split("/")[-2]
    L = instaloader.Instaloader()
    post = Post.from_shortcode(L.context, shortcode)
    response = requests.get(post.url)

    if post.is_video:
        raise Exception('This post is a video, it will not be downloaded')

    return response.content


def migrate_posts(amount):
    cbs_db_ties = pymongo.MongoClient(
        "mongodb://cbs_user:cbs_pwd@tiestheunissen.nl:27017/test")["test"]["instagram"]
    cbs_db_cloud = pymongo.MongoClient(
        "mongodb://cbs:GcAlY5l5yt2CHTacnq4F@devcluster-shard-00-00-ayh0j.mongodb.net:27017,"
        "devcluster-shard-00-01-ayh0j.mongodb.net:27017,"
        "devcluster-shard-00-02-ayh0j.mongodb.net:27017/test?ssl=true&replicaSet=DevCluster-shard-0&authSource=admin"
        "&retryWrites=true")["cbs"]["instagram"]

    posts = cbs_db_cloud.find({"migrated": {"$exists": False}}).limit(amount)

    for post in posts:
        newPost = copy.deepcopy(post)
        del newPost['_id']

        try:
            img = Image.open(BytesIO(download_insta_picture_from_post(post['url'])))
            img = img.resize((32, 32), Image.ANTIALIAS)
            memFile = BytesIO()
            img.save(memFile, format='PNG')
            newPost['image'] = Binary(memFile.getvalue())

            cbs_db_ties.insert_one(newPost)
        except Exception as ex:
            print(ex)

        cbs_db_cloud.update_one({"_id": post['_id']}, {'$set': {'migrated': True}})


while True:
    migrate_posts(100)
    sleep(10)
