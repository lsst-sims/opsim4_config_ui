from lsst.sims.ocs.configuration.instrument import Filters

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["FiltersModel"]

class FiltersModel(ModelHelper):
    """Model class for the Filters configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Filters())
