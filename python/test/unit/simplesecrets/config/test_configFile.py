from unittest import TestCase
import tempfile
import pathlib
from config.configfile import ConfigFile


class TestConfigFile(TestCase):

    def load_file_to_string(self, filepath):
        with open(filepath) as cf:
            linelist = cf.readlines()
        return linelist

    def create_fresh_config_file(self):
        configFile = ConfigFile()
        dir = tempfile.gettempdir()
        file = pathlib.Path(dir).joinpath('tempfile.txt')
        if file.exists():
            file.unlink()
        configFile.create_empty_configfile(file)
        return file

    def test_create_empty_configfile(self):
        file = self.create_fresh_config_file()
        self.assertTrue(file.exists())
        linelist = self.load_file_to_string(file)
        self.assertListEqual(['[envs.files]\n', '\n'], linelist )

    def test_load_configfile(self):
        file = self.create_fresh_config_file()
        configFile = ConfigFile()
        env_dict = configFile.load_configfile(file)
        self.assertEqual(len(env_dict), 0)
        file.unlink()
        env_dict = configFile.load_configfile(file)
        self.assertEqual(len(env_dict), 0)

