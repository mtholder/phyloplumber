Welcome to the phyloplumber project!

The goal of the project is to enable complex pipelines of phylogenetic analyses
	by making it easy to:
		1. interact with existing phylogenetic webservices,
		2. expose phylogenetic analyses as webservices,
		3. use powerful version control systems to track changes to a project,
		4. share a project between collaborators,
		5. provide a browser-based views on project and its history


Getting Started
===============
Prerequisites (you should be prompted for these as you run the 
	getting_started.sh script, but in case you want to know what they are from
	the start:
	
	1. python (version greater than or equal to 2.4 but less than 3.0)
	2. git 


Installing Prerequisites
========================
phyloplumber is built on the Pylons webframework (http://pylonshq.com). If you
	have not installed the tools yet, then you can use the getting_started.sh
	script to get up and running quickly. Just create a directory to work in, 
	move into that directory, and execute the getting_started.sh script:

Using wget to fetch the getting_started script
==============================================
	$ mkdir webservices
	$ cd webservices
	$ wget http://github.com/mtholder/phyloplumber/raw/master/getting_started.py
	$ python getting_started.py

Alternatively, if you have already downloaded phyloplumber source and have it
    stored in a directory called "phyloplumber" then you can cd to the directory
    that is the parent of phyloplumber and run:

python phyloplumber/getting_started.py ..

    to install the dependencies.    
	
	
Installation and Setup
======================
Phyloplumber is built on top of pylons which uses a system of configuration files
    to specify settings that are specific to your installation.  The file format
    is very simple: lines that start with # are comments.  Settings are expressed
    in a simple:
setting_name = setting value
    format.
    
Phyloplumber uses pylon's and virtualenv to install a "virtual" version 

Before running your server you should create a config.ini file and configure
it based on how you want to run phyloplumber:

    1. You can copy deployment.ini to a file called config.ini
    2. Open the file in a text editor
    3. Set the directories for "top_internal_dir" and "top_external_dir" to 
            locations on your filesystem where you would like phyloplumber
            to store files.

If you are installing an instance of phyloplumber that is going to be serving
    content to other machines (rather than binding to the "loop-back" address)
    then it is particularly important to take the following security precautions:
    1. Verify that you have remove the # before "set debug = false" so that The
        server does not launch in debug mode. This is very important because
        serving content in debug mode can allow people visiting your site to
        execute arbitrary code on your server.
    2. Change the setting of beaker.session.secret to some unique string
    3. Remove the # sign before "serves_projects = False" (unless you want your 
       projects to be publicly viewable)
    4. Change the "host" setting to either your server IP or domain name, or 
        0.0.0.0


Setting up the database
=======================
Before running the server the first time, you will need to use the paster command
"setup-app"  with your configuration file. To use the correct version of python
make sure that you have set up your environment. On Mac or Linux you do This
by "source"-ing the file in ${PHYLOPLUMBER_PARENT}/mydevenv/bin/activate where
PHYLOPLUMBER_PARENT is the directory that is the parent of the phyloplumber directory
if you used the getting_started scripts mentioned above.

On Windows you have to execute the activate.bat file in the corresponding directory.


After you have your environment configured then you should have paster and python
in ${PHYLOPLUMBER_PARENT}/mydevenv/bin as the front of our path ("which paster" on
Linux machines will let you check this).  Then you can run:

    paster setup-app config.ini
    
to create the (small) db that is needed for phyloplumber. 

Running phyloplumber
=======================
After you have run the "activate" script mentioned above, then 

    paster serve config.ini
    
will start the server.  Directing a web-browser to http://127.0.0.1:5000 should
then show you the startup page for phyloplumber. (if you have changed the "port"
setting in your config.ini file then the portion of the URL after the : will have
to be changed to agree with the port value in the configuration file).

		
