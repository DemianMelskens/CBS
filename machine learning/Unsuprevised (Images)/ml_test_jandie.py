from PIL import Image, ImageFile
from os import listdir
from os.path import isfile, join
import numpy as np
from sklearn.cluster import KMeans
from shutil import copyfile
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering

ImageFile.LOAD_TRUNCATED_IMAGES = True

SAVE_PATH_1 = './resized_1080_1080_cropped/'
SAVE_PATH_2 = './resized_1080_1080/'
SAVE_PATH_3 = './resized_1080_1350_cropped/'
SAVE_PATH_4 = './resized_1080_1350/'
SAVE_PATH_5 = './resized_1080_566_cropped/'
SAVE_PATH_6 = './resized_1080_566/'

IMAGE_PATH = SAVE_PATH_1

onlyfiles = [f for f in listdir(IMAGE_PATH) if isfile(join(IMAGE_PATH, f))]

images = []

for idx, file in enumerate(onlyfiles):
    print(idx, file)
    with Image.open(IMAGE_PATH + file).convert('L') as img:
        data = np.asarray(img.resize((128,128), Image.ANTIALIAS))
        data = data.reshape(-1)
        images.append(data)

    if idx == 1500: break;

images = np.asarray(images)

# k = KMeans(n_clusters=18)
# k.fit(images)
# y_k = k.predict(images)

# k = SpectralClustering(n_clusters=18)
# k.fit(images)
# y_k = k.labels_

k = AgglomerativeClustering(n_clusters=18)
k.fit(images)
y_k = k.labels_

print(y_k)

for idx, label in enumerate(y_k):
    copyfile(IMAGE_PATH + onlyfiles[idx], './groups/' + str(label) + '/' + onlyfiles[idx])