import argparse
import sys


class ConfigCli:


    def defineparser(self):
        parser = argparse.ArgumentParser(description='Manage secrets files')
        parser.add_argument('-f', '--file', help='specify the env config file location')
        parser.add_argument('-e', '--env', help='name the env that the config file applies to')
        parser.add_argument('-l', '--list', help='list the envs and associated config files held so far')
        return parser

    def process_args(self, parser, argsList):
        args = parser.parse_args(argsList)
        return args

    def parse(self):
        parser = self.defineparser()
        argslist = self.process_args(parser, sys.argv)


