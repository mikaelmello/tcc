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
                    for i in range(self.config.count):
                        self._run(language, library, gpu_mode, i)

    def _run(self, language: str, library: str, gpu_mode: str, id: int):
        formatter = RunnerLogFormatter(language, library, gpu_mode, id)
        logzero.setup_default_logger(formatter=formatter)

        if not self.config.is_compatible(language, library, gpu_mode):
            return

        try:
            logger.info(f"starting")
            if id == 0:
                self.setup.setup(language, library, gpu_mode)

            if language == "python":
                return self._run_python(library, gpu_mode, id)
            else:
                return self._run_java(library, gpu_mode, id)
        except Exception as ex:
            logger.error(f"exception: {ex}")

    def _run_java(self, library: str, gpu_mode: str, id: int):
        logger.debug(f"running")

        dir_path = os.path.join(RUNNERS_DIR, "java", library, gpu_mode)
        jar_path = os.path.join(
            dir_path, "target", f"java-{library}-{gpu_mode}-1.0-SNAPSHOT-bin.jar"
        )

        input_path = INPUT_PATH
        output_path = os.path.join(OUTPUT_DIR, f"java_{library}_{gpu_mode}_{id}.json")

        cmd = f"java -jar {jar_path} -m {MODELS_DIR} -i {input_path} -o {output_path}"

        if gpu_mode == "off":
            cmd = f"export CUDA_VISIBLE_DEVICES=-1; {cmd}"
        else:
            cmd = f"export CUDA_VISIBLE_DEVICES=0; {cmd}"

        logger.debug(f"cmd: {cmd}")

        try:
            subprocess.run(
                cmd, shell=True, executable="/bin/bash", check=True, cwd=dir_path
            )
            logger.debug(f"done")
        except CalledProcessError as ex:
            logger.error("run failed")
            raise ex

    def _run_python(self, library: str, gpu_mode: str, id: int):
        logger.debug(f"running")

        dir_path = os.path.join(RUNNERS_DIR, "python", library)
        venv_path = os.path.join("venv", "bin", "activate")
        script_path = os.path.join("main.py")

        input_path = INPUT_PATH
        output_path = os.path.join(OUTPUT_DIR, f"python_{library}_{gpu_mode}_{id}.json")

        cmd = f"source {venv_path}; python {script_path} -m {MODELS_DIR} -i {input_path} -o {output_path}"

        if gpu_mode == "off":
            cmd = f"export CUDA_VISIBLE_DEVICES=-1; {cmd}"
        else:
            cmd = f"export CUDA_VISIBLE_DEVICES=0; {cmd}"

        if library in ["onnx", "tensorflow"]:
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
