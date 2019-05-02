from unittest import TestCase
from simplesecrets.env_config.envsecretsfile import EnvSecretsFile


class TestEnvSecretsFile(TestCase):

    def test_create_empty_env_config(self):
        env_secrets_file = EnvSecretsFile()
        text = env_secrets_file.create_empty_env_config()
        print(text)

