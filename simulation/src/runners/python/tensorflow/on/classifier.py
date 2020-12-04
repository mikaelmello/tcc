import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model


class Classifier:
    def __init__(self, model_path: str):
        self.model = load_model(model_path)

    def classify(self, values: list):
        input_data = np.array(values, dtype=np.float32)
        output_data = self.model.__call__(
            tf.convert_to_tensor(input_data), training=False
        )
        return int(np.argmax(output_data))