#!/bin/bash

LIBRARY_VERSION=`cat library/setup.py | grep version | awk -F"'" '{print $2}'`
LIBRARY_NAME=`cat library/setup.py | grep name | awk -F"'" '{print $2}'`

printf "$LIBRARY_NAME $LIBRARY_VERSION Python Library: Installer\n\n"

if [ $(id -u) -ne 0 ]; then
	printf "Script must be run as root. Try 'sudo ./install.sh'\n"
	exit 1
fi

cd library

printf "Installing for Python 2..\n"
python setup.py install

if [ -f "/usr/bin/python3" ]; then
	printf "Installing for Python 3..\n"
	python3 setup.py install
fi

cd ..

printf "Done!\n"
