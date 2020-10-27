import subprocess
import os
import logzero
from subprocess import CalledProcessError, PIPE
from runner_log_formatter import RunnerLogFormatter
from logzero import logger
from setup import Setup
from config import Config
from constants import *


class Runner:
    def __init__(self, config: Config, setup: Setup):
        self.config = config
        self.setup = setup

    def run(self):
        for language in self.config.languages:
            for library in self.config.libraries:
                for gpu_mode in self.config.gpu_modes:
                    self._run(language, library, gpu_mode)

    def _run(self, language: str, library: str, gpu_mode: str):
        formatter = RunnerLogFormatter(language, library, gpu_mode)
        logzero.setup_default_logger(formatter=formatter)

        if not self.config.is_compatible(language, library, gpu_mode):
            logger.warn(f"skipping for incompatibility reasons")
            return

        try:
            logger.info(f"starting")
            self.setup.setup(language, library, gpu_mode)

            if language == "python":
                return self._run_python(library, gpu_mode)
        except Exception as ex:
            logger.error(f"exception: {ex}")

    def _run_python(self, library: str, gpu_mode: str):
        logger.debug(f"running")

        dir_path = os.path.join(RUNNERS_DIR, "python", library)
        venv_path = os.path.join("venv", "bin", "activate")
        script_path = os.path.join("main.py")

        input_path = INPUT_PATH
        output_path = os.path.join(OUTPUT_DIR, f"python_{library}_{gpu_mode}.json")

        cmd = f"source {venv_path}; python {script_path} -m {MODELS_DIR} -i {input_path} -o {output_path}"

        if library in ["onnx"]:
            dir_path = os.path.join(dir_path, gpu_mode)
        else:
            if gpu_mode == "on":
                cmd += " --gpu"

        logger.debug(f"cmd: {cmd}")

        try:
            subprocess.run(
                cmd, shell=True, executable="/bin/bash", check=True, cwd=dir_path
            )
            logger.debug(f"done")
        except CalledProcessError as ex:
            logger.error("run failed")
            raise ex
