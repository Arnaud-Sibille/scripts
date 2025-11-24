#!/usr/bin/python3

import argparse
import subprocess

from utils import get_versionned_odoo_repos


ARGUMENTS = {
    ("word", ): {
        "help": "word to look for",
    },
}


def find_word(word, extra_args=[]):
    search_pattern = r'\b' + word + r'\b'
    addons_path = get_versionned_odoo_repos()
    for addon_path in addons_path:
        grep_command = [
            'grep',
            '-n',
            '-r',
            '-E',
            '--include',
            '*.py',
            '--include',
            '*.js',
            '--include',
            '*.xml',
            '--include',
            '*.css',
            '--include',
            '*.scss',
            search_pattern,
            addon_path,
        ]
        command = grep_command + extra_args
        print(command)
        subprocess.run(command)


def main():
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    find_word(args.word, extra_args=extra_args)

if __name__ == "__main__":
    main()
