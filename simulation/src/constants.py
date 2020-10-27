import os
from pathlib import Path

RUNNERS_DIR = os.path.join(Path(__file__).parent.absolute(), "runners")
MODELS_DIR = os.path.join(Path(__file__).parent.parent.absolute(), "resources", "models")
OUTPUT_DIR = os.path.join(Path(__file__).parent.parent.absolute(), "data", "output")
INPUT_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "data", "input", "workload.zip")

LANGUAGES = ["java", "python"]
LIBRARIES = ["opencv", "tensorflow", "onnx", "deeplearning4j"]
GPU_MODES = ["on", "off"]
