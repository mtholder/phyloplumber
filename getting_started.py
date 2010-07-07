#!/usr/bin/env python
import sys, os, subprocess, urllib, logging
log = logging.getLogger(__name__)
major, minor = [int(i) for i in sys.version_info[:2]]
if major != 2 or minor < 4:
    sys.exit("""Please install python. Versions 2.4, 2.5, 2.6, and 2.7 should all work

If you have python installed, make sure that \"python\" is on your PATH
""")

if not os.path.exists('mydevenv/bin/activate'):
    
    if not os.path.exists('go-pylons.py'):
        try:
            sys.stderr.write('Downloading go-pylons.py\n')
            o = open('go-pylons.py', 'w')
            o.write(urllib.urlopen('http://pylonshq.com/download/1.0/go-pylons.py').read())
            o.close()
        except:
            raise
            sys.exit("""The script needs go-pylons.py but the attempt to download it using urllib failed.
    Please, download the go-pylons.py script from
        http://pylonshq.com/download/1.0/go-pylons.py
    and then place the downloaded script in this directory.
    """)
    
    sys.stderr.write('Running go-pylons.py\n')
    if subprocess.call([sys.executable, 'go-pylons.py', '--no-site-packages', 'mydevenv']) != 0:
        sys.exit(1)

if not os.path.exists('phyloplumber'):
    try:
        result = subprocess.call(['git', 'clone', 'git://github.com/mtholder/phyloplumber.git'])
    except:
        sys.exit("""The attempt to pull down the latest version of phyloplumber using git failed.

If you do not have git installed, you can download it from http://git-scm.com
If you have installed git, make sure that it is on your path.""")
    if result != 0:
        sys.exit(1)


string_args = {'pp' : os.path.abspath(os.curdir) }
if not os.path.exists('phyloplumber_env.sh'):
    sys.stdout.write("Creating phyloplumber_env.sh bash script\n")
    o = open('phyloplumber_env.sh', 'w')
    o.write('''#!/bin/sh
export PHYLOPLUMBER_PARENT="%(pp)s"
export PHYLOPLUMBER_ROOT=${PHYLOPLUMBER_PARENT}/phyloplumber
source ${PHYLOPLUMBER_PARENT}/mydevenv/bin/activate
''' % string_args)
    o.close()

if os.path.exists('dendropy'):
    string_args['dd'] = 'dendropy'
else:
    string_args['dd'] = 'DendroPy'
    if not os.path.exists(dendropy_dir):
        try:
            result = subprocess.call(['git', 'clone', 'git clone git://github.com/jeetsukumaran/DendroPy.git'])
        except:
            sys.exit("""The attempt to pull down the latest version of dendropy using git failed.
    
    If you do not have git installed, you can download it from http://git-scm.com
    If you have installed git, make sure that it is on your path.""")
        if result != 0:
            sys.exit(1)
    
if sys.platform.upper().startswith('WIN'):
    sys.exit("""At this point you will need to execute the "%(pp)s/mydevenv/bin/activate.bat" script, then

    1. run "easy_install sphinx"
    
    2. change the working directory to phyloplumber and run "python setup.py develop"
    
    3. change the working directory to %(dd)s and run "python setup.py develop"

to finish the installation process.

You will need to execute the
"%(pp)s/mydevenv/bin/activate.bat"
script each time you launch the phyloplumber server.
""" % string_args)
else:
    fn = 'finish_phyloplumber_installation.sh'
    o = open(fn, 'w')
    o.write('''#!/bin/sh

source phyloplumber_env.sh  || exit 1

################################################################################
# Install sphinx to the devenv
################################################################################
easy_install sphinx

################################################################################
# Checkout dendropy and use "setup.py develop" command to install it the dev env
################################################################################

cd %(dd)s || exit 1
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
    ''')
    o.close()
    result = subprocess.call(['/bin/sh', fn])
    if result == 0:
        os.path.remove(fn)
    else:
        sys.exit(1)
