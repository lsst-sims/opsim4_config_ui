Docker Installation
+++++++++++++++++++

The Docker image that handles the Operations Simulator also contains the configuration UI. The setup instructions can be found `here <https://lsst-sims.github.io/sims_ocs/installation.html>`_. Make sure to follow the Docker installation.

The UI is graphical program and requires a special setup outside the Docker container in order to function. The ``socat`` command is required for this use. It can be installed via any Mac packaging system (brew, fink, etc.). The ``run_opsim4`` script suggested by the OpSim4 installation instructions needs the IP address for the host system, so ensure that the correct one is used. This is linked to the ``DISPLAY`` variable that the ``socat`` command uses. Before executing the configuration UI from within the container, the following command needs to be run in terminal outside the container::

	socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"

You will need to have XQuartz_ installed as well. To run the configuration UI, enter or startup a container and execute the following::

	setup opsim4_config_ui
	opsim4_config_ui

.. _XQuartz: https://www.xquartz.org/