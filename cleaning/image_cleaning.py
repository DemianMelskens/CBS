from PIL import Image
from os import listdir
from os.path import isfile, join
from resizeimage import resizeimage


IMAGE_PATH = '../pics/'
SAVE_PATH_1 = './resized_1080_1080_cropped/'
SAVE_PATH_2 = './resized_1080_1080/'
SAVE_PATH_3 = './resized_1080_1350_cropped/'
SAVE_PATH_4 = './resized_1080_1350/'
SAVE_PATH_5 = './resized_1080_566_cropped/'
SAVE_PATH_6 = './resized_1080_566/'

onlyfiles = [f for f in listdir(IMAGE_PATH) if isfile(join(IMAGE_PATH, f))]

for file in onlyfiles:
    img = Image.open(IMAGE_PATH + file)

    # 1080x1080 cropped
    temp_img = resizeimage.resize_cover(img, [1080, 1080], validate=False)
    temp_img.save(SAVE_PATH_1 + file, img.format)

    # 1080x1080
    temp_img = img.resize((1080,1080), Image.ANTIALIAS)
    temp_img.save(SAVE_PATH_2 + file, img.format)

    # 1080x1350 cropped
    temp_img = resizeimage.resize_cover(img, [1080, 1350], validate=False)
    temp_img.save(SAVE_PATH_3 + file, img.format)

    # 1080x1350
    temp_img = img.resize((1080, 1350), Image.ANTIALIAS)
    temp_img.save(SAVE_PATH_4 + file, img.format)

    # 1080x566 cropped
    temp_img = resizeimage.resize_cover(img, [1080, 566], validate=False)
    temp_img.save(SAVE_PATH_5 + file, img.format)

    # 1080x566
    temp_img = img.resize((1080, 566), Image.ANTIALIAS)
    temp_img.save(SAVE_PATH_6 + file, img.format)


