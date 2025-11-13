#!/usr/bin/python3

import argparse
import subprocess

from utils import REPOS_PATH


ARGUMENTS = {
    ("field_name", ): {
        "help": "name of the field to look for",
    },
}


def find_field_def(field_name, extra_args=[]):
    search_pattern = r'\b' + field_name + r' = fields\.'
    for repo_path in REPOS_PATH:
        grep_command = [
            'grep',
            '-n',
            '-r',
            '-E',
            '--include',
            '*.py',
            search_pattern,
            repo_path,
        ]
        # don't use execute_command as no match found will be raised as an exception
        subprocess.run(grep_command + extra_args)


def main():
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    find_field_def(args.field_name, extra_args=extra_args)

if __name__ == "__main__":
    main()
