import tensorflow as tf

import pandas as pd
import os
 
# print(tf.__version__)
 
train_path = 'CSV/hand_landmarks.csv'
test_path = 'CSV/test_data.csv'
 
train_x = pd.read_csv(train_path, delimiter=',', header=None, usecols=range(1,43))
train_y = pd.read_csv(train_path, delimiter=',', header=None, usecols=[0])
 
train_input = tf.convert_to_tensor(train_x)
train_labels = tf.convert_to_tensor(train_y)
 
 
test_x = pd.read_csv(test_path, delimiter=',', header=None, usecols=range(1,43))
test_y = pd.read_csv(test_path, delimiter=',', header=None, usecols=[0])
 
test_input = tf.convert_to_tensor(test_x)
test_labels = tf.convert_to_tensor(test_y)
 
label_names = ['open', 'closed', 'back', 'blood', 'rock', 'middle finger', 'surfer', 'two', 'one', 'thumbs up', 'three', 'four']
# model = tf.keras.models.load_model('NeuralNet/my_model')

model = tf.keras.Sequential([
    tf.keras.layers.Dense(42),
    tf.keras.layers.Dense(15),
    tf.keras.layers.Dense(5),
    tf.keras.layers.Dense(len(label_names))
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_input, train_labels, epochs=10)
model.save('NeuralNet/my_model')