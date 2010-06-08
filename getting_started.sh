#!/bin/sh
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
else
	python go-pylons.py --no-site-packages mydevenv
fi
