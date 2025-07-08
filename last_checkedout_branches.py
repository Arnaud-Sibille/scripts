import argparse
import subprocess
import re

ARGS = [
    (
        ("-n", "--number",),
        {
            'type': int,
            'default': 10,
            'help': 'Maximum of branches to display.  If negative, all branches found are displayed.',
        }
    ),
]


def last_checkedout_branches(nb_to_display):
    process_res = subprocess.run(['git', 'reflog'], capture_output=True, text=True)
    if error := process_res.stderr:
        raise Exception(error.strip())

    git_logs = process_res.stdout.strip()

    branch_name_pattern = r'[A-Za-z\d/_\.-]+'
    branch_checkout_pattern = r'[\da-f]+\s+HEAD@\{\d+\}:\s+checkout:\s+moving from\s+' + branch_name_pattern + r'\s+to\s+(' + branch_name_pattern + r')$'

    branches = []
    for git_log in git_logs.split('\n'):
        match = re.match(branch_checkout_pattern, git_log)
        if match:
            branch = match.group(1)
            if branch not in branches:
                branches.append(branch)
        if len(branches) == nb_to_display:
            break

    return branches


def main():
    parser = argparse.ArgumentParser()
    for pos_args, kw_args in ARGS:
        parser.add_argument(*pos_args, **kw_args)
    args = parser.parse_args()
    if branches := last_checkedout_branches(args.number):
        print('\n'.join(branches))

if __name__ == '__main__':
    main()
