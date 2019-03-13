# Simple-Secrets

Simple secrets manages credentials and other data you don't want to check in to a repo. It encourages best practice for handling secure configuration by:
- having one central configuration file stored in any mounted location eg a usb stick
- generating a variety of configuration files:
  - .ini files (used by AWS)
  - .properties files
  - .yaml files
  - .json
- checking that the generated files are all in .gitignore
- reformating secret keys to any appropriate format, kebab-case, camel-case, etc 
- ensuring that cloudformation takes these secrets and presents them correctly as env variables for lambdas.
- being runnable from anywhere, so easy to add to any other script

 ##Run Simple Secrets
 
Run this tool by 
```bash
python3 -m simple-secrets -e <env-label> -f <config-file>
```

where:

label | meaning
----- | -------
env-label | simple text label(no space)
config-file | absolute file location of the configuration file


Each run will check whether it would make an update to the affected file, and if not, preserves its filestamp.

If it does make a change it renames the old version of the config file, adding a timesatmp suffix.






