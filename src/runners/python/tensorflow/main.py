import tensorflow as tf
import time
from pathlib import Path
from tensorflow.keras.models import load_model


class Classifier:
    def __init__(self,):
        model_path = Path.joinpath(
            Path(__file__).parent.absolute(), 'model.h5')

        self.classifier = load_model(model_path)

    def classify(self, values: list):
        scaled = [[0, 0, 0, 0, 0, 0, 0]]
        scale = [119.83552861, 1.42122914, 1.31913874,
                 12.90645335, 1283.0616716, 45.84544104, 11.46346616]
        mean = [1.67900462e+02, 3.11090588e+00, 4.43886897e+00, 4.27830029e+01, 4.23752228e+03, 9.29964257e+01,
                3.18708094e+01]
        for i in range(7):
            scaled[0][i] = (values[i] - mean[i]) / scale[i]

        prediction = self.classifier.predict([scaled])

        return int(prediction[0][0])


def classify(classifier, data):
    start = time.time()
    res = classifier.classify(data)
    end = time.time()

    nanoseconds = int((end - start) * 1e6)
    return (res, nanoseconds)


if __name__ == "__main__":
    classifier = Classifier()
    print(classify(classifier, [1, 2, 3, 4, 5, 6, 7]))
