import pymongo
import copy
from io import BytesIO
from PIL import Image
import numpy as np
import time


def get_ml_data():
    cbs_db_ties = pymongo.MongoClient(
        "mongodb://cbs_user:cbs_pwd@tiestheunissen.nl:27017/test")["test"]["data"]

    posts = cbs_db_ties.find({})

    data = {'images': [], 'posts': [], 'labels':[]}

    for post in posts:
        newPost = copy.deepcopy(post)
        del newPost['_id']

        try:
            img = Image.open(BytesIO(newPost['image']))
            data['images'].append(np.asarray(img))
            data['labels'].append(newPost['label'])

            del newPost['image']
            del newPost['label']

            data['posts'].append(copy.deepcopy(newPost))
        except Exception as ex:
            print(ex)

    return data


start_time = time.time()
get_ml_data()
elapsed_time = time.time() - start_time

print('Elapsed time', elapsed_time)
