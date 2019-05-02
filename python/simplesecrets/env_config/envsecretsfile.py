import ruamel.yaml
import sys


class EnvSecretsFile:
    def create_file(self):
        pass

    def load_file(self, env_config_filename):
        if not env_config_filename.exists():
            self.create_empty_env_configfile(env_config_filename)
        with open(env_config_filename, "r") as envfile:
            try:
                secretslist = yaml.safe_load(envfile)
            #    print (secretslist)
            except yaml.YAMLError as exc:
                print("--", exc)
                sys.exit(1)

    def create_empty_env_config(self):
        empty_config = {
            'secrets': None,
            'files': None
        }
        # yaml_object = yaml.safe_load(empty_config)
        yaml_text = ruamel.yaml.safe_dump(empty_config, default_flow_style=False)
        yaml_object = ruamel.yaml.round_trip_load(yaml_text)


    def create_empty_env_configfile(self, env_config_filename):
        #define python object
        today = date.today()
        with open(ss_configfile_path, 'w') as configfile:
            configfile.write('# Configuration for Simple Secrets\n')
            configfile.write('# (https://github.com/mazerunner70/simple-secrets)\n')
            configfile.write(f'# Created {today.strftime("%d/%m/%Y")}\n\n')
            config.write(configfile)




