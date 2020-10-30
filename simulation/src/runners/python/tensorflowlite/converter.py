from os import path
import tensorflow as tf

dir_path = "../../../../resources/models/"

# Convert the model
model = tf.keras.models.load_model(path.join(dir_path, "model.h5"))
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open(path.join(dir_path, "model.tflite"), "wb") as f:
    f.write(tflite_model)
