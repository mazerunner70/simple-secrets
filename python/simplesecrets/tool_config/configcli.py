import argparse
import sys
from simplesecrets.config.ssconfigfile import SsConfigFile
from simplesecrets.ui.table import Table, Colour


class ConfigCli:

    def __init__(self):
        self.config_file = SsConfigFile()
        self.configfile_path = self.config_file.init_configfile_path()


    def defineparser(self):
        parser = argparse.ArgumentParser(
            description='Manage secrets files',
            epilog='Use with both -e, -f to register a new env. Then use just -e to rerun the same env file. '+
                   'Use just -f to avoid associating with env. Running with no params repeats last settings.')
        parser.add_argument('-f', '--file', help='specify the env config file location', nargs=1)
        parser.add_argument('-e', '--env', help='name the env that the config file applies to', nargs=1)
        parser.add_argument('-l', '--list', help="list the envs and associated config files and exit. Overrides other options", action='store_true')
        return parser

    def process_args(self, parser, argsList):
        args_dict = parser.parse_args(argsList)
        return vars(args_dict) # return dict with params

    def execute(self):
        parser = self.defineparser()
        argslist = self.process_args(parser, sys.argv)
        if argslist['list']:
            self.list_envs()
            sys.exit(0)
        argslist += {'env_configfile' : self.get_envconfig_filename()}


    def store_args(self, args_dict):
        options = self.config_file.load_ss_config(self.configfile_path)

    def list_envs(self):
        default_file = self.config_file.get_default_file()
        mapped_envs = self.config_file.get_mapped_envs()
        if len(mapped_envs) == 0 and default_file is None:
            print('No envs or defaults mapped to config files, use options -e, -f together to register a config')
            return
        table = Table()
        print('List of known env files (red highlights current default')
        colourmap = self.get_colourmap(mapped_envs, default_file)
        text = table.colour_table(mapped_envs, ['Env name', 'config file'], None, colourmap)
        print(text)
        if default_file:
            colour = Colour.RED if default_file in mapped_envs.values() else Colour.RESET
            print('\nDefault file: '+colour.value+default_file+Colour.RESET.value)

    def get_envconfig_filename(self):
        # assuming default file or env is set
        return self.config_file.get_default_file() or self.config_file.get_mapped_envs()[self.config_file.get_default_env()]






