import tensorflow as tf
 
import numpy as np
import matplotlib as plt
import pandas as pd
 
# print(tf.__version__)
 
train_path = 'CSV/hand_landmarks.csv'
test_path = 'CSV/test_data.csv'
 
train_x = pd.read_csv(train_path, delimiter=',', header=None, usecols=range(1,42))
train_y = pd.read_csv(train_path, delimiter=',', header=None, usecols=[0])
 
train_input = tf.convert_to_tensor(train_x)
train_labels = tf.convert_to_tensor(train_y)
 
 
test_x = pd.read_csv(test_path, delimiter=',', header=None, usecols=range(1,42))
test_y = pd.read_csv(test_path, delimiter=',', header=None, usecols=[0])
 
test_input = tf.convert_to_tensor(test_x)
test_labels = tf.convert_to_tensor(test_y)
 
label_names = ['open', 'closed', 'back', 'blood']
 
model = tf.keras.Sequential([
    tf.keras.layers.Dense(41),
    tf.keras.layers.Dense(4)
])
 
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
 
model.fit(train_input, train_labels, epochs=10)
 
# test_loss, test_acc = model.evaluate(test_input,  test_labels, verbose=2)
 
# print('\nTest accuracy:', test_acc)
 
probability_model = tf.keras.Sequential([model,
                                         tf.keras.layers.Softmax()])
 
predictions = probability_model.predict(test_input)
 
# for i in range():
#     print(predictions[i])
#     print(np.argmax(predictions[i]))
#     print("\n")
