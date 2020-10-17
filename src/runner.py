import argparse
import logging
import sys
import subprocess
import os
import pathlib
import logzero
from subprocess import CalledProcessError, PIPE
from runner_log_formatter import RunnerLogFormatter
from logzero import logger

_LANGUAGES = ["java", "python"]
_LIBRARIES = ["opencv", "tensorflow", "pytorch", "deeplearning4j"]
_GPU_MODES = ["on", "off"]

_RUNNERS_PATH = os.path.join(pathlib.Path(
    __file__).parent.absolute(), "runners")


class Runner():
    def __init__(self):
        self.languages = _LANGUAGES
        self.libraries = _LIBRARIES
        self.gpu_modes = _GPU_MODES

    def pre_process(self, parser):
        parser.add_argument(
            "--language",
            "-p",
            dest="languages",
            action="append",
            choices=_LANGUAGES,
            default=None,
            help="when present, runs the simulation only on specified languages",
        )

        parser.add_argument(
            "--library",
            "-l",
            dest="libraries",
            action="append",
            choices=_LIBRARIES,
            default=None,
            help="when present, runs the simulation only on specified languages",
        )

        parser.add_argument(
            "--gpu-mode",
            "-g",
            dest="gpu_modes",
            action="append",
            choices=_GPU_MODES,
            default=None,
            help="when present, runs the simulation only on specified languages",
        )

    def post_process(self, args):
        if args.languages:
            self.languages = args.languages
        if args.libraries:
            self.libraries = args.libraries
        if args.gpu_modes:
            self.gpu_modes = args.gpu_modes

    def run(self):
        for language in self.languages:
            for library in self.libraries:
                for gpu_mode in self.gpu_modes:
                    self._run(language, library, gpu_mode)

    def _run(self, language, library, gpu_mode):
        formatter = RunnerLogFormatter(language, library, gpu_mode)
        logzero.setup_default_logger(formatter=formatter)

        if not self._compatible(language, library, gpu_mode):
            logger.warn(f"skipping for incompatibility reasons")
            return

        logger.info(f"starting")

        if language == "python":
            return self._python_run(library, gpu_mode)

    def _compatible(self, language, library, gpu_mode):
        if language == "java" and library == "pytorch":
            return False

        if language == "python" and library == "deeplearning4j":
            return False

        return True

    def _python_run(self, library, gpu_mode):
        dir_path = os.path.join(_RUNNERS_PATH, "python", library)
        venv_path = os.path.join(dir_path, 'venv', 'bin', 'activate')
        script_path = os.path.join(dir_path, "main.py")

        cmd = f'source {venv_path}; echo $PATH; python {script_path}'
        try:
            subprocess.run(cmd, shell=True,
                           executable='/bin/bash', check=True, stderr=PIPE, stdout=PIPE)
        except CalledProcessError as ex:
            logger.error('failed')
