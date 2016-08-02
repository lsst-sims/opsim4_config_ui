from lsst.sims.ocs.configuration.instrument import Dome

from opsim4.model import ModelHelper

__all__ = ["DomeModel"]

class DomeModel(ModelHelper):
    """Model class for the dome configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Dome())
