#!/bin/sh


################################################################################
# Verify python
################################################################################
if ! test -x `which python`
then
	echo "Please install python. Versions 2.4, 2.5, 2.6, and 2.7 should all work"
	echo
	echo "If you have python installed, make sure that \"python\" is on your PATH"
	exit 1
fi

################################################################################
# Install Pylons
################################################################################
if ! test -f go-pylons.py
then
	if ! test -x `which wget`
	then
		echo "The script needs go-pylons.py  Please, do one of the following:"
		echo "    1. Install wget from  http://www.gnu.org/software/wget"
		echo "OR"
		echo "    2. Download the go-pylons.py script from"
		echo "    	http://pylonshq.com/download/1.0/go-pylons.py"
		echo "    and then place the downloaded script in this directory"
		exit 1
	else
		wget http://pylonshq.com/download/1.0/go-pylons.py || exit 1
	fi
fi

if test -f "mydevenv/bin/activate"
then
	echo "mydevenv/bin/activate found, assuming that go-pylons.py has been run "
	echo "    successfully. If you want the getting_started.sh script to reinstall"
	echo "    pylons then remove that file."
else
	python go-pylons.py --no-site-packages mydevenv || exit 1
fi


################################################################################
# Verify git
################################################################################
if ! test -x `which git`
then
	echo "You must install git"
	echo
	echo "This will allow you to easily pull down the latest version of the"	
	echo "    phyloplumber source code and pull new changes as they become available."
	echo
	echo "You can obtain git from here: http://git-scm.com "
	exit 1
fi


################################################################################
# Get the source code for phyloplumber
################################################################################
if ! test -d "phyloplumber"
then
	git clone git://github.com/mtholder/phyloplumber.git  || exit 1
fi


################################################################################
# Create a file to source to get the env set up
################################################################################
echo "Creating phyloplumber_env.sh bash script"
echo '#!/bin/sh' > phyloplumber_env.sh
echo 'export PHYLOPLUMBER_PARENT='`pwd` >> phyloplumber_env.sh
echo 'export PHYLOPLUMBER_ROOT=${PHYLOPLUMBER_PARENT}/phyloplumber' >> phyloplumber_env.sh
echo 'source ${PHYLOPLUMBER_PARENT}/mydevenv/bin/activate' >> phyloplumber_env.sh




################################################################################
# Get the correct env settings by sourcing the file
################################################################################

source phyloplumber_env.sh  || exit 1

################################################################################
# Install sphinx to the devenv
################################################################################
easy_install sphinx

################################################################################
# Checkout dendropy and use "setup.py develop" command to install it the dev env
################################################################################

if ! test -d dendropy
then
	git clone git://github.com/jeetsukumaran/DendroPy.git || exit 1
fi
cd dendropy || exit 1
python setup.py develop || exit 1
cd ..


################################################################################
# install phyloplumber using the "setup.py develop" command
################################################################################
cd phyloplumber || exit 1
python setup.py develop || exit 1
cd ..


echo "phyloplumber_env.sh has been written. Whenever you want to work on phyloplumber"
echo "    from the command line, then (from a bash shell) source this file to "
echo "    configure your environment"

