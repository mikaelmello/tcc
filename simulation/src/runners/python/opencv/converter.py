from os import path
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.framework.convert_to_constants import (
    convert_variables_to_constants_v2,
)
import numpy as np


dir_path = "../../../../resources/models/"


# Convert the model
model = tf.keras.models.load_model(path.join(dir_path, "model.h5"))

# Convert Keras model to ConcreteFunction
full_model = tf.function(lambda x: model(x))
full_model = full_model.get_concrete_function(
    tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype)
)

# Get frozen graph def
frozen_func = convert_variables_to_constants_v2(full_model)
frozen_func.graph.as_graph_def()

layers = [op.name for op in frozen_func.graph.get_operations()]
print("-" * 60)
print("Frozen model layers: ")
for layer in layers:
    print(layer)
print("-" * 60)
print("Frozen model inputs: ")
print(frozen_func.inputs)
print("Frozen model outputs: ")
print(frozen_func.outputs)

tf.io.write_graph(
    graph_or_graph_def=frozen_func.graph,
    logdir=dir_path,
    name=f"model.pb",
    as_text=False,
)
tf.io.write_graph(
    graph_or_graph_def=frozen_func.graph,
    logdir=dir_path,
    name=f"model.pbtxt",
    as_text=True,
)
