from unittest import TestCase
from simplesecrets.config.configcli import ConfigCli
import io
import sys


class TestConfigCli(TestCase):

    def test_defineparser(self):
        configCli = ConfigCli()
        self.assertIsNotNone(configCli.defineparser())

    def test_invalid_args(self):
        configCli = ConfigCli()
        parser = configCli.defineparser()
        output = configCli.process_args(parser, ['-l'])
#        print(output)
        stde = sys.stderr
        test_stde = io.StringIO()
        try:
            sys.stderr = test_stde
            with self.assertRaises(SystemExit) as cm:
                output = configCli.process_args(parser, ['--invalid'])
        finally:
            sys.stderr = stde
            err_str = test_stde.getvalue()
            test_stde.close()
#        print('--'+err_str)
#        print(cm.exception.args )

    def test_file_only_args(self):
        config_cli = ConfigCli()
        parser = config_cli.defineparser()
        output = config_cli.process_args(parser, ['-f', '/user/home/xxx/.loc/file.yml'])
        self.assertDictEqual ( {'env':None, 'file':['/user/home/xxx/.loc/file.yml'], 'list':False}, output )

    def test_env_file_args(self):
        config_cli = ConfigCli()
        parser = config_cli.defineparser()
        output = config_cli.process_args(parser, ['-e', 'Dev1', '-f', '/user/home/xxx/.loc/file.yml'])
        self.assertDictEqual ( {'env':['Dev1'], 'file':['/user/home/xxx/.loc/file.yml'], 'list':False}, output )

    def test_env_only_args(self):
        config_cli = ConfigCli()
        parser = config_cli.defineparser()
        output = config_cli.process_args(parser, ['-e', 'Dev2'])
        self.assertDictEqual({'env': ['Dev2'], 'file': None, 'list': False}, output)

    def test_list_only_args(self):
        config_cli = ConfigCli()
        parser = config_cli.defineparser()
        output = config_cli.process_args(parser, ['-l'])
        self.assertDictEqual({'env': None, 'file': None, 'list': True}, output)

    def test_parse(self):
        pass
