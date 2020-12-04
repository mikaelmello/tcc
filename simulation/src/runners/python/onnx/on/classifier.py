import numpy as np
import onnxruntime as rt


class Classifier:
    def __init__(self, model_path: str):
        self.session = rt.InferenceSession(model_path)

    def classify(self, values: list):
        input_name = self.session.get_inputs()[0].name
        prediction = self.session.run(None, {input_name: values})

        return int(np.argmax(prediction))