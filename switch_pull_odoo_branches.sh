#!/bin/bash

~/scripts/switch_odoo_branches.sh $1 && git -C ~/src/odoo pull && git -C ~/src/enterprise pull
