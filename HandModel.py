import tensorflow as tf

label_names = ['open', 'closed', 'back', 'blood', 'rock', 'middle finger', 'surfer', 'two', 'one', 'thumbs up', 'three', 'four']
model = tf.keras.models.load_model('NeuralNet/my_model')
probability_model = tf.keras.Sequential([model,tf.keras.layers.Softmax()])
