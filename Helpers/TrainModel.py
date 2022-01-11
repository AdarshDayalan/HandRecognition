import tensorflow as tf

import pandas as pd
import os

from constants import label_names
 
# print(tf.__version__)
 
train_path = 'CSV/hand_landmarks.csv'
# test_path = 'CSV/test_data.csv'

train_data = pd.read_csv(train_path, delimiter=',', header=None)
train_data = train_data.sample(frac = 1)
 
train_x = train_data[range(1, 43)]
train_y = train_data[0]

train_input = tf.convert_to_tensor(train_x)
train_labels = tf.convert_to_tensor(train_y)

# test_x = pd.read_csv(test_path, delimiter=',', header=None, usecols=range(1,43))
# test_y = pd.read_csv(test_path, delimiter=',', header=None, usecols=[0])
 
# test_input = tf.convert_to_tensor(test_x)
# test_labels = tf.convert_to_tensor(test_y)
 
model = tf.keras.Sequential([
    tf.keras.layers.Dense(42),
    tf.keras.layers.Dense(84),
    tf.keras.layers.Dense(24),
    tf.keras.layers.Dense(len(label_names))
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_input, train_labels, epochs=25)
model.save('NeuralNet/my_model')