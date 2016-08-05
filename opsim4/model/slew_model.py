from lsst.sims.ocs.configuration.instrument import Slew

from opsim4.model import ModelHelper

__all__ = ["SlewModel"]

class SlewModel(ModelHelper):
    """Model class for the slew configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Slew())
