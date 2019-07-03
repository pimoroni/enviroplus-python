#!/bin/bash

LIBRARY_VERSION=`cat library/setup.cfg | grep version | awk -F" = " '{print $2}'`
LIBRARY_NAME=`cat library/setup.cfg | grep name | awk -F" = " '{print $2}'`

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

printf "Disabling serial..\n"
# Enable serial terminal over /dev/ttyAMA0
raspi-config nonint do_serial 0
# Disable serial port
raspi-config nonint set_config_var enable_uart 0 /boot/config.txt
# Switch serial port back to miniUART
sed -i 's/^dtoverlay=pi3-miniuart-bt # for Enviro+/#dtoverlay=pi3-miniuart-bt # for Enviro+/' /boot/config.txt

printf "Done!\n"
