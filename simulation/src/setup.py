import shutil
import subprocess
from os import path
import logzero
from subprocess import CalledProcessError, PIPE
from runner_log_formatter import RunnerLogFormatter
from logzero import logger
from config import Config


class Setup:
    def __init__(self, config: Config):
        self.config = config

    def setup(self, language: str, library: str, gpu_mode: str):
        logger.debug(f"checking if setup exists")

        if language == "python":
            return self._setup_python(library, gpu_mode)

    def _setup_python(self, library: str, gpu_mode: str):
        dir_path = path.join(self.config.runners_path, "python", library)
        venv_path = path.join(dir_path, "venv")
        activate_path = path.join(venv_path, "bin", "activate")
        script_path = path.join(dir_path, "main.py")
        cwd = dir_path

        cmd_venv = "virtualenv -p /usr/bin/python3 venv"
        cmd_pip = f"source {activate_path}; pip install -r requirements.txt"

        try:
            exists = path.exists(venv_path)
            if exists and not self.config.force_setup:
                return logger.debug(f"setup exists")
            elif exists:
                logger.debug(f"setup exists, but force refresh is enabled")
                shutil.rmtree(venv_path)
            else:
                logger.debug(f"missing setup")

            cmd_venv = "virtualenv -p /usr/bin/python3 venv"

            subprocess.run(
                cmd_venv, shell=True, executable="/bin/bash", check=True, cwd=cwd
            )

            subprocess.run(
                cmd_pip, shell=True, executable="/bin/bash", check=True, cwd=cwd
            )
        except CalledProcessError as ex:
            logger.error("setup failed")
            raise ex
