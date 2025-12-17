#!/bin/bash
SRC_PATH=$HOME/scripts/src

python3 $SRC_PATH/launch_odoo.py -d $1 -i accountant --with-demo --stop
