from unittest import TestCase
from config.configcli import ConfigCli


class TestConfigCli(TestCase):

    def test_defineparser(self):
        configCli = ConfigCli()
        self.assertIsNotNone(configCli.defineparser())

    def test_process_args(self):
        configCli = ConfigCli()
        parser = configCli.defineparser()
        output = configCli.process_args(parser, ['-h'])
        print(output)
        with self.assertRaises(SystemExit) as cm:
            output = configCli.process_args(parser, ['--invalid'])
        print(cm.exception.args)

    def test_parse(self):
        pass
