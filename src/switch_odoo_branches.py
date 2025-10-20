#!/usr/bin/python3

import argparse

from utils import execute_command, REPOS_PATH


ARGUMENTS = {
    ("version", ) : {
        "help": "version to switch the versionned odoo addons to",
    },
    ("-p", "--pull") : {
        "action": "store_true",
        "help": "pull the branch after switching",
    },
}


def switch_repo(repo_path, branch):
    switch_command = [
        "git",
        "-C",
        repo_path,
        "switch",
        branch,
    ]
    execute_command(switch_command)

def pull_repo(repo_path):
    pull_command = [
        "git",
        "-C",
        repo_path,
        "pull",
    ]
    execute_command(pull_command)

def switch_odoo_branches(version, pull=False):
    for repo_path in REPOS_PATH:
        # to avoid considering again the community repo
        switch_repo(repo_path, version)
        if pull:
            pull_repo(repo_path)


def main():
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    switch_odoo_branches(args.version, args.pull)

if __name__ == "__main__":
    main()
