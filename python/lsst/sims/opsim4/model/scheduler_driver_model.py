from lsst.sims.ocs.configuration import SchedulerDriver

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["SchedulerDriverModel"]

class SchedulerDriverModel(ModelHelper):
    """Model class for the scheduler driver configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, SchedulerDriver())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            sched_driver = SchedulerDriver()
            ModelHelper.load_config(sched_driver, config_files)
            model = ModelHelper(sched_driver)
            return model.params
