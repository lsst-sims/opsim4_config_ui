from lsst.sims.ocs.configuration import Downtime

from opsim4.model import ModelHelper

__all__ = ["DowntimeModel"]

class DowntimeModel(ModelHelper):
    """Model class for the downtime configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Downtime())
