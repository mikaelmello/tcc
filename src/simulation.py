import argparse
import sys
from runner import Runner


class ArgumentParser(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Simulation Manager for the Graduation Thesis :)')

        runner = Runner()

        runner.pre_process(parser)

        args = parser.parse_args()

        runner.post_process(args)
        runner.run()


if __name__ == '__main__':
    ArgumentParser()
