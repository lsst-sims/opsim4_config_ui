from lsst.sims.ocs.configuration import SchedulerDriver

from opsim4.model import ModelHelper

__all__ = ["SchedulerDriverModel"]

class SchedulerDriverModel(ModelHelper):
    """Model class for the scheduler driver configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, SchedulerDriver())
