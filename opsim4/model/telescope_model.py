from lsst.sims.ocs.configuration.instrument import Telescope

from opsim4.model import ModelHelper

__all__ = ["TelescopeModel"]

class TelescopeModel(ModelHelper):
    """Model class for the telescope configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Telescope())
