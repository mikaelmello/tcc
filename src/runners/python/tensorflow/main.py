import tensorflow as tf
import time
import numpy as np
from pathlib import Path
from tensorflow.keras.models import load_model


class Classifier:
    def __init__(self,):
        model_path = Path.joinpath(
            Path(__file__).parent.absolute(), 'saved_model')

        converter = tf.lite.TFLiteConverter.from_saved_model(str(model_path))
        tflite_model = converter.convert()

        print(model_path)
        self.classifier = tf.lite.Interpreter(model_content=tflite_model)
        self.classifier.allocate_tensors()
        self.input_details = self.classifier.get_input_details()
        self.output_details = self.classifier.get_output_details()
        print("cool")
        print(self.input_details)
        print(self.output_details)

    def classify(self, values: list):
        scaled = [[0, 0, 0, 0, 0, 0, 0]]
        scale = [119.83552861, 1.42122914, 1.31913874,
                 12.90645335, 1283.0616716, 45.84544104, 11.46346616]
        mean = [1.67900462e+02, 3.11090588e+00, 4.43886897e+00, 4.27830029e+01, 4.23752228e+03, 9.29964257e+01,
                3.18708094e+01]
        for i in range(7):
            scaled[0][i] = (values[i] - mean[i]) / scale[i]

        input_data = np.array(scaled, dtype=np.float32)
        self.classifier.set_tensor(0, input_data)
        self.classifier.invoke()
        output_data = self.classifier.get_tensor(13)
        return int(output_data[0][0])


def classify(classifier, data):
    for i in range(100000):
        res = classifier.classify(data)
    start = time.time()
    for i in range(1000000):
        res = classifier.classify(data)
    end = time.time()

    seconds = (end - start)
    print(1000000/seconds)
    return (res, seconds)


if __name__ == "__main__":
    classifier = Classifier()
    for i in range(1):
        print(classify(classifier, [1, 2, 3, 4, 5, 6, 7]))
