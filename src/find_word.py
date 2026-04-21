#!/usr/bin/python3

import argparse

from .find_in_repos import find_in_repos

ARGUMENTS = {
    ("search_pattern", ): {
        "help": "regex pattern",
    },
}

def main():
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    search_pattern = r'\b' + args.word + r'\b'
    find_in_repos(search_pattern, extra_args=extra_args)

if __name__ == "__main__":
    main()
