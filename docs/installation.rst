============
Installation
============

.. warning::

	The current installation requires multiple repositories and a mixture of environments. It also only works on a Linux environment. It has been tested on a RHEL 7 type environment.

General Installation Notes
--------------------------

Due to the heavy use of repositories for this installation, the instructions will assume you have created a ``git`` directory in your ``$HOME`` directory. This will be referenced as ``gitdir``. The individual repository installation instructions will give further advice on directory names. This is intended to make the usage "easier". Also, all instructions are based around using the code, not developing it.

Prerequisite Installation
-------------------------

The configuration UI requires the Simulated OCS (SOCS) package as it contains the configuration for the reference survey. The setup instructions can be found `here <https://lsst-sims.github.io/sims_ocs/installation.html>`_. 

Installation and Setup
----------------------

Once the above is complete, go to ``gitdir/lsst-sims`` and run the following::

	git clone https://github.com/lsst-sims/opsim4_config_ui.git

Using the conda environment that was created during the prerequisite installation process, activate that environment and then run::

	cd opsim4_config_ui
	source eups-setups.sh
	eups declare opsim4_config_ui git -r . -c
	setup opsim4_config_ui
	python setup.py develop
	python setup.py build_rcc

The last two steps are important as they create the version information for the program and the image resource file.

Start the Program
-----------------

To bring up the configuration UI, run::

	opsim4_config_ui

The next section will detail use of the program.


