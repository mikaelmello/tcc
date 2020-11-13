import tensorflow as tf
import time
import numpy as np
from pathlib import Path
from tensorflow.keras.models import load_model
import numpy


class Classifier:
    def __init__(self, model_path: str):
        self.model = load_model(model_path)

    def classify(self, values: list):

        input_data = np.asarray(values, dtype=np.float32)
        output_data = self.model.__call__(
            tf.convert_to_tensor(input_data), training=False
        )
        return int(numpy.argmax(output_data))