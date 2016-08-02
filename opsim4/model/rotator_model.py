from lsst.sims.ocs.configuration.instrument import Rotator

from opsim4.model import ModelHelper

__all__ = ["RotatorModel"]

class RotatorModel(ModelHelper):
    """Model class for the rotator configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Rotator())
