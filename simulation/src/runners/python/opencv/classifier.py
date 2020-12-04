import cv2
import numpy as np


class Classifier:
    def __init__(self, model_path: str, gpu: bool):
        self.net = cv2.dnn.readNetFromONNX(model_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

        if gpu:  # does not work
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        else:
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def classify(self, values: list):
        self.net.setInput(np.array(values))
        prediction = self.net.forward()

        return int(np.argmax(prediction))