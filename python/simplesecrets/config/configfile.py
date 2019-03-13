import configparser
import pathlib

class ConfigFile:
    USER_HOME_DIR_PATH = pathlib.Path.home()
    MODULE_SUB_DIR = '/.simplesecrets'
    MODULE_CONFIG_FILENAME = 'ss.config'

    def create_empty_configfile(self, configfile_path):
        config = configparser.ConfigParser()
        config['envs.files'] ={}
        with open(configfile_path, 'w') as configfile:
            config.write(configfile)

    def envs_as_dict(self, config):
        return dict(config.items('envs.files'))

    def get_configfile_path(self):
        config_dir = self.USER_HOME_DIR_PATH.joinpath(self.MODULE_SUB_DIR)
        config_dir.mkdir(exist_ok=True)
        configfile_path = config_dir.joinpath(self.MODULE_CONFIG_FILENAME)
        return configfile_path

    def load_configfile(self, configfile_path):
        if not configfile_path.exists():
            self.create_empty_configfile(configfile_path)
        config = configparser.ConfigParser()
        with open(configfile_path) as cf:
            config.read_file(cf)
        return self.envs_as_dict(config)


