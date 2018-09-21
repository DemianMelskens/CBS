import instaloader
from instaloader import Post
from tqdm import tqdm
import pandas as pd
import requests
import os
import sys


def check_create_path(path):
    directory = os.path.dirname(path)

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)


def download_insta_picture_from_post(url, download_path):
    try:
        shortcode = url.split("/")[-2]
        L = instaloader.Instaloader()
        post = Post.from_shortcode(L.context, shortcode)
        response = requests.get(post.url)
        filename = shortcode + '.jpg'
        path = download_path + filename

        if post.is_video:
            print('Post skipped because its a video', url)
            return False

        with open(path, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

        return True
    except:
        print('Could not download file', sys.exc_info()[0], url)
        return False


def download_insta_images(csv_file, download_path):
    check_create_path(download_path)
    inst_data = pd.read_csv(csv_file, delimiter=';')
    for url in inst_data['url']:
        download_insta_picture_from_post(url, download_path)


# Example
download_insta_images(
    csv_file='../data/Coosto_berichten.csv',
    download_path='./pics/')
