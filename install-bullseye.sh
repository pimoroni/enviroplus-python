#!/bin/bash
CONFIG=/boot/config.txt
DATESTAMP=`date "+%Y-%m-%d-%H-%M-%S"`
CONFIG_BACKUP=false
APT_HAS_UPDATED=false
USER_HOME=/home/$SUDO_USER
RESOURCES_TOP_DIR=$USER_HOME/Pimoroni
WD=`pwd`
USAGE="sudo $0 (--unstable)"
POSITIONAL_ARGS=()
UNSTABLE=false
PYTHON="/usr/bin/python3"
CODENAME=`lsb_release -sc`

distro_check() {
	if [[ $CODENAME != "bullseye" ]]; then
		printf "This installer is for Raspberry Pi OS: Bullseye only, current distro: $CODENAME\n"
		exit 1
	fi
}

user_check() {
	if [ $(id -u) -ne 0 ]; then
		printf "Script must be run as root. Try 'sudo $0'\n"
		exit 1
	fi
}

confirm() {
	if [ "$FORCE" == '-y' ]; then
		true
	else
		read -r -p "$1 [y/N] " response < /dev/tty
		if [[ $response =~ ^(yes|y|Y)$ ]]; then
			true
		else
			false
		fi
	fi
}

prompt() {
	read -r -p "$1 [y/N] " response < /dev/tty
	if [[ $response =~ ^(yes|y|Y)$ ]]; then
		true
	else
		false
	fi
}

success() {
	echo -e "$(tput setaf 2)$1$(tput sgr0)"
}

inform() {
	echo -e "$(tput setaf 6)$1$(tput sgr0)"
}

warning() {
	echo -e "$(tput setaf 1)$1$(tput sgr0)"
}

function do_config_backup {
	if [ ! $CONFIG_BACKUP == true ]; then
		CONFIG_BACKUP=true
		FILENAME="config.preinstall-$LIBRARY_NAME-$DATESTAMP.txt"
		inform "Backing up $CONFIG to /boot/$FILENAME\n"
		cp $CONFIG /boot/$FILENAME
		mkdir -p $RESOURCES_TOP_DIR/config-backups/
		cp $CONFIG $RESOURCES_TOP_DIR/config-backups/$FILENAME
		if [ -f "$UNINSTALLER" ]; then
			echo "cp $RESOURCES_TOP_DIR/config-backups/$FILENAME $CONFIG" >> $UNINSTALLER
		fi
	fi
}

function apt_pkg_install {
	PACKAGES=()
	PACKAGES_IN=("$@")
	for ((i = 0; i < ${#PACKAGES_IN[@]}; i++)); do
		PACKAGE="${PACKAGES_IN[$i]}"
		if [ "$PACKAGE" == "" ]; then continue; fi
		printf "Checking for $PACKAGE\n"
		dpkg -L $PACKAGE > /dev/null 2>&1
		if [ "$?" == "1" ]; then
			PACKAGES+=("$PACKAGE")
		fi
	done
	PACKAGES="${PACKAGES[@]}"
	if ! [ "$PACKAGES" == "" ]; then
		echo "Installing missing packages: $PACKAGES"
		if [ ! $APT_HAS_UPDATED ]; then
			apt update
			APT_HAS_UPDATED=true
		fi
		apt install -y $PACKAGES
		if [ -f "$UNINSTALLER" ]; then
			echo "apt uninstall -y $PACKAGES"
		fi
	fi
}

while [[ $# -gt 0 ]]; do
	K="$1"
	case $K in
	-u|--unstable)
		UNSTABLE=true
		shift
		;;
	-p|--python)
		PYTHON=$2
		shift
		shift
		;;
	*)
		if [[ $1 == -* ]]; then
			printf "Unrecognised option: $1\n";
			printf "Usage: $USAGE\n";
			exit 1
		fi
		POSITIONAL_ARGS+=("$1")
		shift
	esac
done

distro_check
user_check

if [ ! -f "$PYTHON" ]; then
	printf "Python path $PYTHON not found!\n"
	exit 1
fi

PYTHON_VER=`$PYTHON --version`

inform "Installing. Please wait..."

$PYTHON -m pip install --upgrade configparser

CONFIG_VARS=`$PYTHON - <<EOF
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
	warning "Error parsing configuration...\n"
	exit 1
fi

eval $CONFIG_VARS

RESOURCES_DIR=$RESOURCES_TOP_DIR/$LIBRARY_NAME
UNINSTALLER=$RESOURCES_DIR/uninstall.sh

mkdir -p $RESOURCES_DIR

cat << EOF > $UNINSTALLER
printf "It's recommended you run these steps manually.\n"
printf "If you want to run the full script, open it in\n"
printf "an editor and remove 'exit 1' from below.\n"
exit 1
EOF

printf "$LIBRARY_NAME $LIBRARY_VERSION Python Library: Installer\n\n"

if $UNSTABLE; then
	warning "Installing unstable library from source.\n\n"
else
	printf "Installing stable library from pypi.\n\n"
fi

cd library

printf "Installing for $PYTHON_VER...\n"
apt_pkg_install "${PY3_DEPS[@]}"
if $UNSTABLE; then
	$PYTHON setup.py install > /dev/null
else
	$PYTHON -m pip install --upgrade $LIBRARY_NAME
fi
if [ $? -eq 0 ]; then
	success "Done!\n"
	echo "$PYTHON -m pip uninstall $LIBRARY_NAME" >> $UNINSTALLER
fi

cd $WD

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
		inform "Adding $CONFIG_LINE to $CONFIG\n"
		sed -i "s/^#$CONFIG_LINE/$CONFIG_LINE/" $CONFIG
		if ! grep -q "^$CONFIG_LINE" $CONFIG; then
			printf "$CONFIG_LINE\n" >> $CONFIG
		fi
	fi
done

if [ -d "examples" ]; then
	if confirm "Would you like to copy examples to $RESOURCES_DIR?"; then
		inform "Copying examples to $RESOURCES_DIR"
		cp -r examples/ $RESOURCES_DIR
		echo "rm -r $RESOURCES_DIR" >> $UNINSTALLER
		success "Done!"
	fi
fi

printf "\n"

if [ -f "/usr/bin/pydoc" ]; then
	printf "Generating documentation.\n"
	pydoc -w $LIBRARY_NAME > /dev/null
	if [ -f "$LIBRARY_NAME.html" ]; then
		cp $LIBRARY_NAME.html $RESOURCES_DIR/docs.html
		rm -f $LIBRARY_NAME.html
		inform "Documentation saved to $RESOURCES_DIR/docs.html"
		success "Done!"
	else
		warning "Error: Failed to generate documentation."
	fi
fi

success "\nAll done!"
warning "If this is your first time installing you should --reboot-- for hardware changes to take effect.\n"
warning "This library is installed for python 3 *only* make sure to use \"python3\" when running examples.\n"
