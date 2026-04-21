#!/bin/bash
set -x

git switch $1 && git pull && git switch - && git rebase $1
