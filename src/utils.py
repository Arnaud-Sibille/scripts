import configparser
import os
import re
import subprocess

REPOS_PATH = [
    "/home/odoo/src/odoo",
    "/home/odoo/src/enterprise",
]

CONFIG_FILE_NAME = '.config'

def extract_version_from_branch_name(branch_name):
    tokens = branch_name.split('-')
    if tokens[0] == 'saas':
        return f'saas-{tokens[1]}'
    return tokens[0]

def get_repo_current_branch(repo_path):
    get_branch_command = [
        "git",
        "-C",
        repo_path,
        "rev-parse",
        "--abbrev-ref",
        "HEAD",
    ]
    output = execute_command(get_branch_command, get_output=True)
    return output.decode('utf-8').strip()

def guess_odoo_repo_version():
    for repo in get_versionned_odoo_repos():
        branch = get_repo_current_branch(repo)
        version = extract_version_from_branch_name(branch)
        if re.match(r'^(master|(saas-)?\d+.\d+)$', version):
            return version

def get_repo_directory():
    current_file_dir = os.path.abspath(__file__)
    return os.path.abspath(os.path.join(current_file_dir, '../..'))

def get_value_from_config(key):
    config_file_path = os.path.join(get_repo_directory(), CONFIG_FILE_NAME)
    if not os.path.exists(config_file_path):
        raise Exception(f"Cannot find config file {config_file_path}")
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config.get("options", key)

def get_versionned_odoo_repos():
    return get_value_from_config("versionned_odoo_repos").split(',')

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
    print(f"{7 * '*'}- Executing {command}...")
    result = subprocess.run(command, input=input_str.encode() if input_str else None, capture_output=get_output)
    if result.returncode:
        raise Exception(f"Command {command} failed.")
    print(f"{8 * '*'}")
    return result.stdout
