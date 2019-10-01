#!/usr/bin/env bash

python3.7 -V > /dev/null 2>&1 || {
	echo >&2 "Python 3.7 doesn't seem to be installed.  Do you have a weird installation?"
	echo >&2 "If you have python 3.7, use it to run run.py instead of this script."
	exit 1; }

python3.7 run.py