
import os
from pathlib import Path

RUNNERS_PATH = os.path.join(Path(__file__).parent.absolute(), "runners")

LANGUAGES = ["java", "python"]
LIBRARIES = ["opencv", "tensorflow", "pytorch", "deeplearning4j"]
GPU_MODES = ["on", "off"]
