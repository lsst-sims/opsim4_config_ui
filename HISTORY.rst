.. :changelog:

History
-------

1.1.1 (2017-08-01)
~~~~~~~~~~~~~~~~~~

* New parameters for main UI tabs

  * propboost_weight for Scheduler Driver
  * max_visits_goal for Sequence proposals

* Added max_visits_goal to Sequence proposal in creation wizard
* Added SOCS version to About dialog

1.1.0 (2017-05-26)
~~~~~~~~~~~~~~~~~~

* Ability to apply a directory of override files onto the current default set of parameters

  * Changed parameters are flagged as usual
  * Any new proposals (``new_props``) available will be displayed
  * Override files for new proposals can also be displayed

* Fix for issue with list parameters having single entries when writing override and new proposal files 

1.0.3 (2017-05-02)
~~~~~~~~~~~~~~~~~~

* Fix issue with similarly named parameters getting masked during setup.

1.0.2 (2017-04-20)
~~~~~~~~~~~~~~~~~~

* Provide parameters for restarting lost and complete sequences for Sequence proposals

1.0.1 (2017-04-04)
~~~~~~~~~~~~~~~~~~

* Make save directory dialog start one directory up from last saved directory instead of always user home.

1.0 (2017-02-28)
~~~~~~~~~~~~~~~~~

This release will be the baseline interaction for configuring OpSim version 4. It will have access to all necessary parameters and has the capability to generate new proposals.
