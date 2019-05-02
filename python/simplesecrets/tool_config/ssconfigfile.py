import configparser
import pathlib
from datetime import date

#Singleton pattern - only one access to the config file at a time
class SsConfigFile:

    #config file sections/keys
    DEFAULT = 'Default'
    ENVS_FILES = 'envs.files'
    LAST_CONFIG_FILE_USED = 'last_config_file_used'
    LAST_ENV_SPECIFIED = 'last_env_specified'

    USER_HOME_DIR_PATH = pathlib.Path.home()
    MODULE_SUB_DIR = '.simplesecrets'
    MODULE_CONFIG_FILENAME = 'ss.config'

    def initialise(self):
        ss_configfile_path = self.init_configfile_path()
        self.ss_config = self.load_ss_config(ss_configfile_path)

    def create_empty_configfile(self, ss_configfile_path):
        config = configparser.ConfigParser()
        config[self.ENVS_FILES] ={}
        config[self.DEFAULT] ={self.LAST_CONFIG_FILE_USED: '', self.LAST_ENV_SPECIFIED: ''}
        self.today = date.today()
        with open(ss_configfile_path, 'w') as configfile:
            configfile.write('# Configuration for Simple Secrets\n')
            configfile.write('# (https://github.com/mazerunner70/simple-secrets)\n')
            configfile.write(f'# Created {self.today.strftime("%d/%m/%Y")}\n\n')
            config.write(configfile)


    def init_configfile_path(self):
        config_dir = self.USER_HOME_DIR_PATH.joinpath(self.MODULE_SUB_DIR)
        config_dir.mkdir(exist_ok=True)
        configfile_path = config_dir.joinpath(self.MODULE_CONFIG_FILENAME)
        return configfile_path

    def load_ss_config(self, ss_configfile_path):
        if not ss_configfile_path.exists():
            self.create_empty_configfile(ss_configfile_path)
        parser = configparser.ConfigParser()
        with open(ss_configfile_path) as cf:
            parser.read_file(cf)
        return self.as_dict(parser)

    def save_ss_config(self, ss_configfile_path, ss_config):
        # Only update config file if it changes
        file_based_config = self.as_dict(self.load_ss_config(ss_configfile_path))
        if not file_based_config == ss_config:
            with open(ss_configfile_path, "w") as ss_configfile:
                ss_config.write(ss_configfile)


    def update_ss_config(self, ss_config, env_name, env_configfile_name):
        if not env_name:
            # directly specify config file to use
            if not env_configfile_name:
                # Where filename is already known from on a previous usage
                env_configfile_name = ss_config[self.DEFAULT][self.LAST_CONFIG_FILE_USED]
                if not env_configfile_name:
                    raise ValueError('Must have specified filename or envname on this or previous invoke. See -h for options')
            ss_config[self.DEFAULT][self.LAST_CONFIG_FILE_USED] = env_configfile_name
            ss_config[self.DEFAULT][self.LAST_ENV_SPECIFIED] = ''
        else:
            # involve the env specifier
            if not env_configfile_name:
                # use env-file mapping already in config
                env_configfile_name = ss_config[self.ENVS_FILES].get(env_name)
                if not env_configfile_name:
                    raise ValueError('env name must be associated with a configuration file. See -h for options')
            ss_config[self.DEFAULT][self.LAST_CONFIG_FILE_USED] = env_configfile_name
            ss_config[self.DEFAULT][self.LAST_ENV_SPECIFIED] = env_name
            ss_config[self.ENVS_FILES][env_name] = env_configfile_name



    def as_dict(self, parser):
        config = {}
        for section in parser.sections():
            config[section] = {}
            for key, val in parser.items(section):
                config[section][key] = val
        return config

    def get_default_env(self):
        return self.ss_config.get(self.DEFAULT, {}).get(self.LAST_ENV_SPECIFIED)

    def get_default_file(self):
        return self.ss_config.get(self.DEFAULT, {}).get(self.LAST_CONFIG_FILE_USED)

    def get_mapped_envs(self):
        return self.ss_config[self.ENVS_FILES]

