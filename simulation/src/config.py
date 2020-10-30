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
from constants import *


class Config:
    def __init__(self):
        self.languages = LANGUAGES
        self.libraries = LIBRARIES
        self.gpu_modes = GPU_MODES
        self.force_setup = False

    def pre_process(self, parser):
        parser.add_argument(
            "--language",
            "-p",
            dest="languages",
            action="append",
            choices=LANGUAGES,
            default=None,
            help="when present, runs the simulation only on specified languages",
        )

        parser.add_argument(
            "--library",
            "-l",
            dest="libraries",
            action="append",
            choices=LIBRARIES,
            default=None,
            help="when present, runs the simulation only on specified libraries",
        )

        parser.add_argument(
            "--gpu-mode",
            "-g",
            dest="gpu_modes",
            action="append",
            choices=GPU_MODES,
            default=None,
            help="when present, runs the simulation only on specified gpu modes",
        )

        parser.add_argument(
            "--setup",
            "-s",
            dest="force_setup",
            action="store_const",
            const=True,
            default=False,
            help="when present, refreshes the setup of the involved combinations",
        )

    def post_process(self, args):
        if args.languages:
            self.languages = args.languages
        if args.libraries:
            self.libraries = args.libraries
        if args.gpu_modes:
            self.gpu_modes = args.gpu_modes

        self.force_setup = args.force_setup

    def is_compatible(self, language: str, library: str, gpu_mode: str):
        if language == "python" and library == "deeplearning4j":
            return False

        if language == "java" and library == "opencv":
            return False

        if language == "java" and library == "tensorflowlite":
            return False

        if library == "tensorflowlite" and gpu_mode == "on":
            return False

        return True