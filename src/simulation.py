import argparse
import sys
import os
from pathlib import Path
from runner import Runner
from setup import Setup
from config import Config


class ArgumentParser(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Simulation Manager for the Graduation Thesis :)"
        )

        config = Config()

        config.pre_process(parser)
        args = parser.parse_args()
        config.post_process(args)

        setup = Setup(config)
        runner = Runner(config, setup)

        runner.run()


if __name__ == "__main__":
    ArgumentParser()
