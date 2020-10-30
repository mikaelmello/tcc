import shutil
import subprocess
from os import path
import logzero
from subprocess import CalledProcessError, PIPE
from runner_log_formatter import RunnerLogFormatter
from logzero import logger
from config import Config
from constants import *


class Setup:
    def __init__(self, config: Config):
        self.config = config

    def setup(self, language: str, library: str, gpu_mode: str):
        logger.debug(f"checking if setup exists")

        if language == "python":
            return self._setup_python(library, gpu_mode)
        else:
            return self._setup_java(library, gpu_mode)

    def _setup_java(self, library: str, gpu_mode: str):
        dir_path = path.join(RUNNERS_DIR, "java", library, gpu_mode)
        jar_path = path.join(
            dir_path, "target", f"java-{library}-{gpu_mode}-1.0-SNAPSHOT-bin.jar"
        )

        cmd_package = "mvn package"

        try:
            exists = path.exists(jar_path)
            if exists and not self.config.force_setup:
                return logger.debug(f"setup exists")
            elif exists:
                logger.debug(f"setup exists, but force refresh is enabled")
                shutil.rmtree(path.join(dir_path, "target"))
            else:
                logger.debug(f"missing setup")

            subprocess.run(
                cmd_package,
                shell=True,
                executable="/bin/bash",
                check=True,
                cwd=dir_path,
            )
        except CalledProcessError as ex:
            logger.error("setup failed")
            raise ex

    def _setup_python(self, library: str, gpu_mode: str):
        dir_path = path.join(RUNNERS_DIR, "python", library)
        venv_path = path.join("venv")
        activate_path = path.join(venv_path, "bin", "activate")

        cmd_venv = "virtualenv -p /usr/bin/python3 venv"
        cmd_pip = f"source {activate_path}; pip install -r requirements.txt"

        if library in ["onnx"]:
            dir_path = os.path.join(dir_path, gpu_mode)

        try:
            exists = path.exists(path.join(dir_path, venv_path))
            if exists and not self.config.force_setup:
                return logger.debug(f"setup exists")
            elif exists:
                logger.debug(f"setup exists, but force refresh is enabled")
                shutil.rmtree(path.join(dir_path, venv_path))
            else:
                logger.debug(f"missing setup")

            cmd_venv = "virtualenv -p /usr/bin/python3 venv"

            subprocess.run(
                cmd_venv, shell=True, executable="/bin/bash", check=True, cwd=dir_path
            )

            subprocess.run(
                cmd_pip, shell=True, executable="/bin/bash", check=True, cwd=dir_path
            )
        except CalledProcessError as ex:
            logger.error("setup failed")
            raise ex
