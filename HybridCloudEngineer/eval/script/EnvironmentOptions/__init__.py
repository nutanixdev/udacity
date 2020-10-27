#!/usr/bin/env/python3

import sys
import argparse
import subprocess
from Messages import Messages


class EnvironmentOptions():
    '''
    class the blueprint evaluation environment
    '''

    '''
    class constructor
    '''
    def __init__(self):
        self.criteria = ''
        self.directory = ''
        self.blueprint = ''
        self.full_bp = ''
        self.valid = False
        self.dsl = False
        self.debug = False

    def __repr__(self):
        '''
        decent __repr__ for debuggability
        this is something recommended by Raymond Hettinger
        '''
        return (f'{self.__class__.__name__}(criteria={self.criteria},'
                f'directory={self.directory},'
                f'blueprint={self.blueprint},'
                f'full_bp={self.full_bp},'
                f'value={self.valid},'
                f'dsl={self.dsl},'
                f'debug={self.debug})')

    def get_options(self):
        '''
        gather script parameters from the command line
        '''
        parser = argparse.ArgumentParser(description='Evaluate '
                                         + 'a Udacity '
                                         + 'student\' Nutanix Calm '
                                         + 'Blueprint')

        parser.add_argument('--criteria', '-c',
                            help='JSON file containing evaluation criteria. '
                                 + 'Defaults to "criteria/p3.json".')
        parser.add_argument('--directory', '-d',
                            help='Directory containing exported Nutanix Calm '
                                 + 'Blueprints. '
                                 + 'Defaults to the current directory.')
        parser.add_argument('--blueprint', '-b',
                            help='Nutanix Calm Blueprint file in JSON format. '
                                 + 'Set to "all" to process all blueprints '
                                 + 'in the specified directory. '
                                 + 'Defaults to "blueprint.py".')
        parser.add_argument('--valid', '-v',
                            choices=["true", "false"],
                            help='Specify that the script should process '
                                 + 'valid blueprints only. '
                                 + 'Defaults to False.')
        parser.add_argument('--dsl',
                            choices=["true", "false"],
                            help='Specify that the DSL is not required for '
                            + 'this run.  Used for troubleshooting only.')
        parser.add_argument('--debug',
                            choices=["enable", "disable"],
                            help='Enable debug mode and show detailed info '
                                 + 'when certain events are triggered. '
                                 + 'Defaults to False.')

        args = parser.parse_args()

        self.criteria = (args.criteria if args.criteria
                         else "criteria/p3.json")
        self.directory = (args.directory if args.directory else ".")
        self.blueprint = (args.blueprint if args.blueprint else "blueprint.py")
        self.valid = (args.valid if args.valid == "true" else False)
        self.dsl = (args.dsl if args.dsl == "true" else False)
        self.debug = True if args.debug == 'enable' else False

    def check_environment(self, messages: Messages):
        '''
        check the environment and make sure it has all the required commands
        '''

        # setup the list of required commands
        required_commands = ['calm'] if self.dsl else []

        try:
            for command in required_commands:
                subprocess.run(
                    [command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                location = subprocess.run(
                    ['which', command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(f'{messages.info} {command} found in '
                      + f'{location.stdout.decode()}', end="")
        except FileNotFoundError:
            print(f'{messages.error} Unable to execute the `{command}` '
                  + f'command.  Please ensure the `{command}` command '
                  + 'is accessible and executable in your PATH.')
            print(f'{messages.info} Environment requirements not met.  If you '
                  + 'not yet done so, please run setup for this script: \n'
                  + f'{messages.info} pip3 install -e .\n')
            sys.exit()
