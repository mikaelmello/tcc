from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import load_model
from os import path
import onnx
import keras2onnx

path = "../../../../../resources/models/"
onnx_model_name = f"{path}model.onnx"

model = load_model(f"{path}model.h5")
onnx_model = keras2onnx.convert_keras(model, model.name)
onnx.save_model(onnx_model, onnx_model_name)