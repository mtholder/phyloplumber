#!/bin/sh
set -x
if ! test -f go-pylons.py
then
	if ! test -x `which wget`
	then
		echo "The script needs go-pylons.py  Please, do one of the following:"
		echo "    1.install wget from  http://www.gnu.org/software/wget    OR"
		echo "    2. download the go-pylons.py script from"
		echo "    	http://pylonshq.com/download/1.0/go-pylons.py"
		echo "    and then place the downloaded script in this directory"
		exit 1
	else
		wget http://pylonshq.com/download/1.0/go-pylons.py
	fi
fi

if ! test -x `which python`
then
	echo "Please install python. Versions 2.4, 2.5, 2.6, and 2.7 should all work"
	echo
	echo "If you have python installed, make sure that \"python\" is on your PATH"
	exit 1
fi

if test -f "mydevenv/bin/activate"
then
	echo "mydevenv/bin/activate found, assuming that go-pylons.py has been run "
	echo "    successfully. If you want the getting_started.sh script to reinstall"
	echo "    pylons then remove that file."
else
	python go-pylons.py --no-site-packages mydevenv
fi


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

if ! test -d "phyloplumber"
then
	git clone git://github.com/mtholder/phyloplumber.git
fi
