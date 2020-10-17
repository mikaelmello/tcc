import numpy
import time
import onnxruntime as rt


class Classifier:
    def __init__(self):
        self.classifier = rt.InferenceSession("model.onnx")

    def classify(self, values: list):
        scaled = [[0, 0, 0, 0, 0, 0, 0]]
        scale = [
            119.83552861,
            1.42122914,
            1.31913874,
            12.90645335,
            1283.0616716,
            45.84544104,
            11.46346616,
        ]
        mean = [
            1.67900462e02,
            3.11090588e00,
            4.43886897e00,
            4.27830029e01,
            4.23752228e03,
            9.29964257e01,
            3.18708094e01,
        ]
        for i in range(7):
            scaled[0][i] = (values[i] - mean[i]) / scale[i]

        input_name = self.classifier.get_inputs()[0].name
        prediction = self.classifier.run(None, {input_name: scaled})

        return int(prediction[0][0])


def classify(classifier, data):
    start = time.time()
    res = classifier.classify(data)
    end = time.time()

    microseconds = int((end - start) * 1e6)
    return (res, microseconds)


if __name__ == "__main__":
    classifier = Classifier()
    for i in range(100000):
        print(classify(classifier, [4, 4, 4, 4, 4, 4, 4]))
