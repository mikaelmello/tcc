import argparse
import sys
import command


class ArgumentParser(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Simulation Manager for the Graduation Thesis :)',
            usage='''python main.py <command> [<args>]

The most commonly used commands are:
   run     Runs a simulation
''')

        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def run(self):
        command.run()


if __name__ == '__main__':
    ArgumentParser()
