import argparse
import sys
from config.ssconfigfile import SsConfigFile


class ConfigCli:

    def __init__(self):
        self.config_file = SsConfigFile()
        self.configfile_path = self.config_file.init_configfile_path()


    def defineparser(self):
        parser = argparse.ArgumentParser(
            description='Manage secrets files',
            epilog='Use with both -e, -f to register a new env. Then use just -e to rerun the same env file. Use just -f to avoid associating with env')
        parser.add_argument('-f', '--file', help='specify the env config file location', nargs=1)
        parser.add_argument('-e', '--env', help='name the env that the config file applies to', nargs=1)
        parser.add_argument('-l', '--list', help="list the envs and associated config files. Don't use with other options", action='store_true')
        return parser

    def process_args(self, parser, argsList):
        args_dict = parser.parse_args(argsList)
        return vars(args_dict) # return dict with params

    def parse(self):
        parser = self.defineparser()
        argslist = self.process_args(parser, sys.argv)

    def store_args(self, args_dict):
        options = self.config_file.load_ss_config(self.configfile_path)

