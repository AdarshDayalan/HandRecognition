# import tensorflow as tf

import numpy as np
import matplotlib as plt
import pandas as pd

# print(tf.__version__)

train_path = 'CSV/hand_landmarks.csv'
test_path = 'CSV/test_data.csv'

train_x = pd.read_csv(train_path, header=None, usecols=[1,42])
train_y = pd.read_csv(train_path, header=None, usecols=[0,0])

label_names = ['open', 'closed']