Welcome to the phyloplumber project!

The goal of the project is to enable complex pipelines of phylogenetic analyses
	by making it easy to:
		1. interact with existing phylogenetic webservices,
		2. expose phylogenetic analyses as webservices,
		3. use powerful version control systems to track changes to a project,
		4. share a project between collaborators,
		5. provide a browser-based views on project and its history

################################################################################
Getting Started
################################################################################
Prerequisites (you should be prompted for these as you run the 
	getting_started.sh script, but in case you want to know what they are from
	the start:
	
	1. python (version greater than or equal to 2.4 but less than 3.0)
	2. git 

phyloplumber is built on the Pylons webframework (http://pylonshq.com). If you
	have not installed the tools yet, then you can use the getting_started.sh
	script to get up and running quickly. Just create a directory to work in, 
	move into that directory, and execute the getting_started.sh script:
	
	$ mkdir webservices
	$ cd webservices
	$ wget http://github.com/mtholder/phyloplumber/blob/master/getting_started.sh
	$ getting_started.sh
	
		
