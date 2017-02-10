from lsst.sims.ocs.configuration.instrument import Park

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["ParkModel"]

class ParkModel(ModelHelper):
    """Model class for the park configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Park())
