import argparse
import logging
import sys
import subprocess
import os
import pathlib
from logzero import logger

_LANGUAGES = ["java", "python"]
_LIBRARIES = ["opencv", "tensorflow", "pytorch", "deeplearning4j"]
_GPU_MODES = ["on", "off"]

_RUNNERS_PATH = os.path.join(pathlib.Path(
    __file__).parent.parent.absolute(), "runners")


def check_allowed(list):
    def check(value):
        if value not in list:
            raise argparse.ArgumentTypeError(
                f"{value} is not allowed, allowed values: {list}"
            )
        return value

    return check


def main():
    parser = argparse.ArgumentParser(description="Runs a simulation")
    parser.add_argument("run", help="Run")

    parser.add_argument(
        "--language",
        "-p",
        dest="languages",
        action="append",
        type=check_allowed(_LANGUAGES),
        default=None,
        help="when present, runs the simulation only on specified languages",
    )
    parser.add_argument(
        "--library",
        "-l",
        dest="libraries",
        action="append",
        type=check_allowed(_LIBRARIES),
        default=None,
        help="when present, runs the simulation only on specified languages",
    )
    parser.add_argument(
        "--gpu-mode",
        "-g",
        dest="gpu_modes",
        action="append",
        type=check_allowed(_GPU_MODES),
        default=None,
        help="when present, runs the simulation only on specified languages",
    )

    args = parser.parse_args(sys.argv[1:])

    if not args.languages:
        args.languages = _LANGUAGES
    if not args.libraries:
        args.libraries = _LIBRARIES
    if not args.gpu_modes:
        args.gpu_modes = _GPU_MODES

    for language in args.languages:
        for library in args.libraries:
            for gpu_mode in args.gpu_modes:
                _run(language, library, gpu_mode)


def _compatible(language, library, gpu_mode):
    if language == "java" and library == "pytorch":
        return False

    if language == "python" and library == "deeplearning4j":
        return False

    return True


def _run(language, library, gpu_mode):
    if not _compatible(language, library, gpu_mode):
        logger.warn(f"skipping {language} {library} gpu {gpu_mode}")
        return

    logger.info(f"running {language} {library} gpu {gpu_mode}")

    if language == "python":
        return _python_run(library, gpu_mode)


def _python_run(library, gpu_mode):
    dir_path = os.path.join(_RUNNERS_PATH, "python", library)
    venv_path = os.path.join(dir_path, 'venv', 'bin', 'activate')
    script_path = os.path.join(dir_path, "main.py")

    cmd = f'source {venv_path}; echo $PATH; python {script_path}'
    subprocess.run(cmd, shell=True, executable='/bin/bash')
