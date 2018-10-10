import pandas as pd
from to_mongo import add_dataset

instagram = pd.read_csv('./to_mongo/500_chunk_c.csv', delimiter=';')

add_dataset(instagram)

print('Done!')