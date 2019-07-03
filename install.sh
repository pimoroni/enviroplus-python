#!/bin/bash

CONFIG=/boot/config.txt
DATESTAMP=`date "+%Y-%M-%d-%H-%M-%S"`
CONFIG_BACKUP=false

CONFIG_VARS=`python - <<EOF
from configparser import ConfigParser
c = ConfigParser()
c.read('library/setup.cfg')
p = dict(c['pimoroni'])
# Convert multi-line config entries into bash arrays
for k in p.keys():
    fmt = '"{}"'
    if '\n' in p[k]:
        p[k] = "'\n\t'".join(p[k].split('\n')[1:])
        fmt = "('{}')"
    p[k] = fmt.format(p[k])
print("""
LIBRARY_NAME="{name}"
LIBRARY_VERSION="{version}"
""".format(**c['metadata']))
print("""
PY3_DEPS={py3deps}
PY2_DEPS={py2deps}
SETUP_CMDS={commands}
CONFIG_TXT={configtxt}
""".format(**p))
EOF`

if [ $? -ne 0 ]; then
	printf "Error parsing configuration...\n"
	exit 1
fi

function do_config_backup {
	if [ ! $CONFIG_BACKUP == true ]; then
		CONFIG_BACKUP=true
		FILENAME="/boot/config.preinstall-$LIBRARY_NAME-$DATESTAMP.txt"
		printf "Backing up $CONFIG to $FILENAME\n"
		cp $CONFIG $FILENAME
	fi
}

function apt_pkg_install {
	PACKAGES=()
	PACKAGES_IN=("$@")
	for ((i = 0; i < ${#PACKAGES_IN[@]}; i++)); do
		PACKAGE="${PACKAGES_IN[$i]}"
		printf "Checking for $PACKAGE\n"
		dpkg -L $PACKAGE > /dev/null 2>&1
		if [ "$?" == "1" ]; then
			PACKAGES+=("$PACKAGE")
		fi
	done
	PACKAGES="${PACKAGES[@]}"
	if ! [ "$PACKAGES" == "" ]; then
		echo "Installing missing packages: $PACKAGES"
		sudo apt update
		sudo apt install -y $PACKAGES
	fi
}

eval $CONFIG_VARS

printf "$LIBRARY_NAME $LIBRARY_VERSION Python Library: Installer\n\n"

if [ $(id -u) -ne 0 ]; then
	printf "Script must be run as root. Try 'sudo ./install.sh'\n"
	exit 1
fi

cd library

printf "Installing for Python 2..\n"
apt_pkg_install "${PY2_DEPS[@]}"
python setup.py install

if [ -f "/usr/bin/python3" ]; then
	printf "Installing for Python 3..\n"
	apt_pkg_install "${PY3_DEPS[@]}"
	python3 setup.py install
fi

cd ..

for ((i = 0; i < ${#SETUP_CMDS[@]}; i++)); do
	CMD="${SETUP_CMDS[$i]}"
	# Attempt to catch anything that touches /boot/config.txt and trigger a backup
	if [[ "$CMD" == *"raspi-config"* ]] || [[ "$CMD" == *"$CONFIG"* ]] || [[ "$CMD" == *"\$CONFIG"* ]]; then
		do_config_backup
	fi
	eval $CMD
done

for ((i = 0; i < ${#CONFIG_TXT[@]}; i++)); do
	CONFIG_LINE="${CONFIG_TXT[$i]}"
	if ! [ "$CONFIG_LINE" == "" ]; then
		do_config_backup
		printf "Adding $CONFIG_LINE to $CONFIG\n"
		sed -i "s/^#$CONFIG_LINE/$CONFIG_LINE/" $CONFIG
		if ! grep -q "^$CONFIG_LINE" $CONFIG; then
			printf "$CONFIG_LINE\n" >> $CONFIG
		fi
	fi
done

printf "Done!\n"
