import tensorflow as tf
import numpy as np


class Classifier:
    def __init__(self, model_path: str):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_tensor = self.interpreter.get_input_details()[0]["index"]
        self.output_tensor = self.interpreter.get_output_details()[0]["index"]

    def classify(self, values: list):
        input_data = np.array(values, dtype=np.float32)
        self.interpreter.set_tensor(self.input_tensor, input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_tensor)
        return int(np.argmax(output_data))