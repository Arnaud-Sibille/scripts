#!/bin/bash
set -x

git fetch dev $1 && git switch $1  && git reset --hard dev/$1
