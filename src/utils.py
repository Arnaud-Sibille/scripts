import configparser
import os
import subprocess

REPOS_PATH = [
    "/home/odoo/src/odoo",
    "/home/odoo/src/enterprise",
]


def get_odoorc_path():
    home_directory = os.path.expanduser("~")
    odoorc_path = os.path.join(home_directory, ".odoorc")
    if os.path.exists(odoorc_path):
        return odoorc_path
    raise Exception("~/.odoorc not found")

def get_value_from_odoorc(key):
    odoorc_path = get_odoorc_path()
    config = configparser.ConfigParser()
    config.read(odoorc_path)
    value = config.get("options", key)
    if not value:
        raise Exception(f"Could not find '{key}' in [options] of {odoorc_path}.")
    return value

def get_filestore_dir():
    return get_value_from_odoorc('data_dir')

def get_filestore_path(db_name):
    filestore_dir = get_filestore_dir()
    filestore_path = os.path.join(filestore_dir, db_name)
    if os.path.exists(filestore_path):
        return filestore_path
    return None    

def execute_command(command, get_output=False, input_str=None):
    result = subprocess.run(command, input=input_str.encode() if input_str else None, capture_output=get_output)
    if result.returncode:
        raise Exception(f"Command {command} failed.")
    return result.stdout
