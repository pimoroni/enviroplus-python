#!/bin/bash

LIBRARY_VERSION=`cat library/setup.py | grep version | awk -F"'" '{print $2}'`
LIBRARY_NAME=`cat library/setup.py | grep name | awk -F"'" '{print $2}'`
CONFIG=/boot/config.txt
DATESTAMP=`date "+%Y-%M-%d-%H-%M-%S"`

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

printf "Backing up $CONFIG\n"
cp $CONFIG "config.preinstall-$DATESTAMP.txt"

printf "Setting up serial for PMS5003..\n"
# Disable serial terminal over /dev/ttyAMA0
raspi-config nonint do_serial 1
# Enable serial port
raspi-config nonint set_config_var enable_uart 1 $CONFIG
# Switch serial port to full UART for stability (may adversely affect bluetooth)
sed -i 's/^#dtoverlay=pi3-miniuart-bt/dtoverlay=pi3-miniuart-bt/' $CONFIG
if ! grep -q -E "^dtoverlay=pi3-miniuart-bt" $CONFIG; then
	printf "dtoverlay=pi3-miniuart-bt\n" >> $CONFIG
fi

printf "Done!\n"
