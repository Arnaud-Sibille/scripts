#!/usr/bin/python3

import argparse
import os

from utils import execute_command, get_value_from_config, guess_odoo_repo_version


ARGUMENTS = {
    ('-v', '--venv'): {
        "help": "Virtual env to use",
    }
}


def launch_odoo(venv=False, extra_args=[]):
    if not venv:
        venv = guess_odoo_repo_version() or 'master'

    venv_path = os.path.join(get_value_from_config('venv_dir'), venv)
    python_path = os.path.join(venv_path, 'bin/python') if os.path.exists(venv_path) else 'python3'
    execute_command([
        python_path,
        get_value_from_config('odoo_bin_path'),
        *extra_args,
    ])

def main():
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    launch_odoo(venv=args.venv, extra_args=extra_args)

if __name__ == '__main__':
    main()
