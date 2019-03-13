#!/usr/bin/env python3.6

# Takes a secrets file at /vagrant/env-secrets.yml and creates several possible output files:
# ~/.aws/credentials
# ~/.env (a .properties -style file)
# ./aws/sam-app/sam-template.yml (rewrites this to accept parameters)
# ./scripts/cloud-formation-secrets.json (ensure this is in .gitignore)

import yaml
import os
import sys
import datetime
import string
import json
import re
from pathlib import Path
import time

class SubTag(yaml.YAMLObject):
    yaml_tag = u'!Sub'
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return "%s(name=%r, text=%r" % ( self.__class__.__name__, self.name, self.text)
    @classmethod
    def from_yaml(cls, loader, node):
        return SubTag(node.value)
    @classmethod
    def to_yaml(cls, dumper, data):
        #    print("553", dumper.represent_scalar(cls.yaml_tag, data.text))
        return dumper.represent_scalar(cls.yaml_tag, data.text)
yaml.SafeLoader.add_constructor('!Sub', SubTag.from_yaml)
yaml.SafeDumper.add_multi_representer(SubTag, SubTag.to_yaml)

class RefTag(yaml.YAMLObject):
    yaml_tag = u'!Ref'
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return "%s(text=%r)" % ( self.__class__.__name__, self.text)
    @classmethod
    def from_yaml(cls, loader, node):
        return RefTag(node.value)
    @classmethod
    def to_yaml(cls, dumper, data):
        #    print("553", dumper.represent_scalar(cls.yaml_tag, data.text))
        return dumper.represent_scalar(cls.yaml_tag, data.text)
yaml.SafeLoader.add_constructor('!Ref', RefTag.from_yaml)
yaml.SafeDumper.add_multi_representer(RefTag, RefTag.to_yaml)

class GetAttTag(yaml.YAMLObject):
    yaml_tag = u'!GetAtt'
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return "%s(text=%r)" % ( self.__class__.__name__, self.text)
    @classmethod
    def from_yaml(cls, loader, node):
        return GetAttTag(node.value)
    @classmethod
    def to_yaml(cls, dumper, data):
        #    print("553", dumper.represent_scalar(cls.yaml_tag, data.text))
        return dumper.represent_scalar(cls.yaml_tag, data.text)
yaml.SafeLoader.add_constructor('!GetAtt', GetAttTag.from_yaml)
yaml.SafeDumper.add_multi_representer(GetAttTag, GetAttTag.to_yaml)



def edit_sam_template(file_config, secrets_map, statusRow):
    cf_location = file_config.get('location')
    cf_template = None
    with open(cf_location, "r")  as cf_templatefile:  # Located here as an easy access point for ansible on the vm
        try:
            cf_template = yaml.safe_load(cf_templatefile)
        except yaml.YAMLError as exc:
            print ("--", exc)
            sys.exit(1)
    cf_parameters = cf_template.get('Parameters')
    cf_parameters.clear()
    resources = file_config.get('resources')
    # print("737", type(resources), resources)
    cf_props = {}
    for resource in resources:
        #    print("777", type(resource), resource)
        #    print("772", resource.keys())
        name = resource.get('name')
        secretids = resource.get('secrets')
        for secretid in secretids:
            cf_props[asLogicalId(secretid)] = secrets_map[secretid]
            cf_parameters[asLogicalId(secretid)] = {"Type": "String"}
        cf_resources = cf_template.get('Resources')
        cf_resource = cf_resources.get(name)
        #    print ("cf_resource", name, cf_resource)
        cf_variables = cf_resource.get('Properties').get('Environment').get('Variables')
        cf_variables.clear()
        for secretid in secretids:
            cf_variables[as_env_name(secretid)] = RefTag(asLogicalId(secretid))
        updateFile(file_config.get('cf-config-file'), asProps(cf_props), statusRow)
    #  print("_____")
    return yaml.dump(cf_template, default_flow_style=False)

def asLogicalId(text):
    return text.translate(str.maketrans('','',string.punctuation))

def as_env_name(text):
    nopunct = text.translate(str.maketrans(string.punctuation, '_'*len(string.punctuation)))

    underscored = re.sub(r"([A-Z][0-9a-z]*)(?=[A-Z])", r"\1_", nopunct, 100)
    return underscored.upper()

def addunderscore(matchobj):
    return matchobj.group(1)+"_"+matchobj.group(2)

def create_ini(file_config, secrets_map, statusRow):
    secretids = file_config.get('secrets')
    result = ""
    for secretid in secretids:
        secret = secrets_map.get(secretid)
        result = f'[{secret.get("section")}]\n'
        props = secret.get('properties')
        for key in props:
            result += f'{key} = {props.get(key)}\n'
    return result

def create_props(file_config, secrets_map, statusRow):
    secretids = file_config.get('secrets')
    separator = file_config.get('separator')
    result = ""
    for secretid in secretids:
        #    print ("--", secretid)
        secret = secrets_map.get(secretid)
        result += f'{secretid}{separator}{secret}\n'
    return result

def create_json(file_config, secrets_map, statusRow):
    secretids = file_config.get('secrets')
    result = "[\n"
    sep = ""
    for secretid in secretids:
        #    print ("--", secretid)
        secret = secrets_map.get(secretid)
        result += f'{sep}\n  {{\n    "ParameterKey": "{secretid}",\n    "ParameterValue": "{secret}"\n  }}'
        sep=","
    result += "]"
    return result

def asJson(propsMap):
    return json.dumps(propsMap)

def asProps(propsMap):
    result = ""
    separator = '='
    for prop in propsMap:
        result += f'{prop}{separator}{propsMap[prop]}\n'
    return result




def rename_existing_file(file_location_string):
    os.rename(file_location_string, f"{file_location_string}-{datetime.datetime.now():%Y%m%d%H%M%S}")

def write_out(file_location_string, text):
    os.makedirs(os.path.dirname(file_location_string), exist_ok=True)
    with open(file_location_string, "w") as textfile:
        textfile.write(text)

def load_existing_file(file_location_string):
    filetext = ""
    if (os.path.isfile(file_location_string)):
        with open(file_location_string, "r") as stream:
            filetext = stream.read()
    return filetext

def updateFile(filename, newText, statusRow):
    if Path(filename).is_file():
        reference_text = load_existing_file(filename)
        if newText == reference_text:
            statusRow[3] = 'unchanged'
        else:
            rename_existing_file(filename)
            statusRow[3] = 'overwritten'
    else:
        statusRow[3] = 'created'
    write_out(filename, newText)

def initialisefilestatus(filelist):
    return [ [file.get('name'), file.get('type'), file.get('location'), 'to do'] for file in filelist]

status_colours = {
    'Status     ': '\033[0;37m',
    'to do': '\033[0;33m',
    'processing': '\033[0;32m',
    'created': '\033[0;34m',
    'unchanged': '\033[0;34m',
    'overwritten': '\033[0;34m',
    'failed': '\033[0;31m'
}

def addstatuscolour(list, column_number):
    if column_number == 3:
        return status_colours[list[3]]+list[3]+'\033[0;37m'
    return list[column_number]


def display_secretfiles(files, updating):
    displaylist = files.copy()
    displaylist.insert(0, ['Filename', 'Type', 'Location', 'Status     '])
    widths = []
    for i in range(4):
        widths.append( max([len(file[i]) for file in displaylist])+1)
    horizontalbar = "-"*(sum(widths)+len(widths)+1)
    headerbar = horizontalbar+"\n"
    if updating == True:
        sys.stdout.write("\033[F" * (3+len(displaylist)))  # Cursor up one line
    print(horizontalbar)
    for row in displaylist:
        print ("|"+"|".join([addstatuscolour(row, i)+" "*(widths[i]-len(row[i])) for i in range(4)])+"|")
        print(headerbar, end="")
        headerbar = ""
    print(horizontalbar)


def main():
    print("Secrets management\n")

    for i in range(2):
        print("Loading" + "." * i)
        print("Loading2" + "." * i)
        sys.stdout.write("\033[F" * 2)  # Cursor up one line
        time.sleep(1)


    scriptdir = os.path.dirname(os.path.abspath(__file__))
    print("script home is", scriptdir)
    secretslist = None # set of secrets in file
    with open("/home/vagrant/.env-secrets.yml", "r") as secretsfile:
        try:
            secretslist = yaml.safe_load(secretsfile)
        #    print (secretslist)
        except yaml.YAMLError as exc:
            print ("--", exc)
            sys.exit(1)

    secrets_map = secretslist.get('secrets')
    files = secretslist.get('files')
    # loop through files

    filesstate = initialisefilestatus(files)
    display_secretfiles(filesstate, False)

    for file_config in files:
        statusRow = [row for row in filesstate if row[0] == file_config.get('name')][0]
        statusRow[3] = 'processing'
        display_secretfiles(filesstate, True)
        filetype = file_config.get('type')
        filecreate_types = {
            'ini-file': create_ini,
            'properties-file': create_props,
            'sam-template': edit_sam_template,
            'json-file': create_json
        }
        createfileText = filecreate_types.get(filetype, lambda a: "Invalid month")
        text = createfileText(file_config, secrets_map, statusRow)
        updateFile(file_config.get('location'), text, statusRow)
        display_secretfiles(filesstate, True)
        #sys.exit(10)
    display_secretfiles(filesstate, True)


if __name__ == "__main__":
    main()




