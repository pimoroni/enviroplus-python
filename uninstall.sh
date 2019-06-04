#!/bin/bash

LIBRARY_VERSION=`cat library/setup.py | grep version | awk -F"'" '{print $2}'`
LIBRARY_NAME=`cat library/setup.py | grep name | awk -F"'" '{print $2}'`

printf "$LIBRARY_NAME $LIBRARY_VERSION Python Library: Uninstaller\n\n"

if [ $(id -u) -ne 0 ]; then
	printf "Script must be run as root. Try 'sudo ./uninstall.sh'\n"
	exit 1
fi

cd library

printf "Unnstalling for Python 2..\n"
pip uninstall $LIBRARY_NAME

if [ -f "/usr/bin/pip3" ]; then
	printf "Uninstalling for Python 3..\n"
	pip3 uninstall $LIBRARY_NAME
fi

cd ..

printf "Done!\n"
