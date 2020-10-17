import subprocess
import os
import logzero
from subprocess import CalledProcessError, PIPE
from runner_log_formatter import RunnerLogFormatter
from logzero import logger
from setup import Setup
from config import Config


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
        dir_path = os.path.join(self.config.runners_path, "python", library)
        venv_path = os.path.join(dir_path, "venv", "bin", "activate")
        script_path = os.path.join(dir_path, "main.py")

        cmd = f"source {venv_path}; python {script_path}"
        try:
            subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)
        except CalledProcessError as ex:
            logger.error("run failed")
            raise ex
