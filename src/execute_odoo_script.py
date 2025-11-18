#!/usr/bin/python3

import argparse
import os

from utils import execute_command, get_value_from_config, guess_odoo_repo_version


ARGUMENTS = {
    ("db", ): {
        "help": "database to execute the script on",
    },
    ("script", ): {
        "help": "script to run in the db",
    },
    ("--commit", ): {
        "action": "store_true",
        "help": "commit the script to the database (append `env.cr.commit()`)",
    },
    ('-v', '--venv'): {
        "help": "Virtual env to use",
    }
}


def execute_odoo_script(db, script_path, commit=False, venv=False, extra_args=False):
    with open(script_path, 'r') as script:
        input_code = script.read()
        if commit:
            input_code += '\nenv.cr.commit()\n'

    if not venv:
        venv = guess_odoo_repo_version() or 'master'
    venv_path = os.path.join(get_value_from_config('venv_dir'), venv)
    python_path = os.path.join(venv_path, 'bin/python') if os.path.exists(venv_path) else 'python3'
    command = [
        python_path,
        get_value_from_config('odoo_bin_path'),
        'shell',
        '-d',
        db,
        "--log-handler",
        ":CRITICAL",
        *extra_args,
    ]
    execute_command(command, input_str=input_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    execute_odoo_script(args.db, args.script, commit=args.commit, venv=args.venv, extra_args=extra_args)
