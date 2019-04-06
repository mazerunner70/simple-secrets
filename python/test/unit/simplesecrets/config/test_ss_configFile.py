from unittest import TestCase
import tempfile
import pathlib
from simplesecrets.config.ssconfigfile import SsConfigFile


class TestConfigFile(TestCase):

    def load_file_to_string(self, filepath):
        with open(filepath) as cf:
            linelist = cf.readlines()
        return linelist

    def create_fresh_config_file(self):
        configFile = SsConfigFile()
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
        self.assertListEqual([
                              '[envs.files]\n',
                              '\n',
                              '[Default]\n',
                              'last_config_file_used = \n',
                              'last_env_specified = \n',
                              '\n'
                              ], linelist )

    def test_load_configfile(self):
        file = self.create_fresh_config_file()
        configFile = SsConfigFile()
        config = configFile.load_ss_config(file)
        self.assertEqual(len(config), 2)
        file.unlink()
        #confirm still works if config file not present
        env_dict = configFile.load_ss_config(file)
        self.assertEqual(len(env_dict), 2)

    def test_update_config(self):
        file = self.create_fresh_config_file()
        ss_config_file = SsConfigFile()
        ss_config = ss_config_file.load_ss_config(file)
        # Case 1 trying to specify neither env or file when no substitues are available in ss_config, error
        with self.assertRaises(ValueError) as cm:
            ss_config_file.update_ss_config(ss_config, '','')
        # Case 2 specify just file, works, updates config
        ss_config_file.update_ss_config(ss_config, '', 'file_location')
        self.assertEqual(ss_config[ss_config_file.DEFAULT][ss_config_file.LAST_CONFIG_FILE_USED], 'file_location')
        self.assertEqual(ss_config[ss_config_file.DEFAULT][ss_config_file.LAST_ENV_SPECIFIED], '')
        # Case 3 now specify neither env or file, and get back file
        ss_config_file.update_ss_config(ss_config, '', '')
        self.assertEqual(ss_config[ss_config_file.DEFAULT][ss_config_file.LAST_CONFIG_FILE_USED], 'file_location')
        self.assertEqual(ss_config[ss_config_file.DEFAULT][ss_config_file.LAST_ENV_SPECIFIED], '')
        # Case 4 specify env only and get error if file does not exist
        with self.assertRaises(ValueError) as cm:
            ss_config_file.update_ss_config(ss_config, 'dummy1', '')
        # Case 5 specify both env and file and set that into the env list
        ss_config_file.update_ss_config(ss_config, 'dummy1', 'file_loc_dummy')
        self.assertEqual(ss_config[ss_config_file.DEFAULT][ss_config_file.LAST_CONFIG_FILE_USED], 'file_loc_dummy')
        self.assertEqual(ss_config[ss_config_file.DEFAULT][ss_config_file.LAST_ENV_SPECIFIED], 'dummy1')
        self.assertEqual(ss_config[ss_config_file.ENVS_FILES].get('dummy1'), 'file_loc_dummy')

    




