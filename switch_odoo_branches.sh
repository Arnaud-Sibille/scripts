#!/bin/bash

git -C ~/src/odoo switch $1 && git -C ~/src/enterprise switch $1
