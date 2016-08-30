from lsst.sims.ocs.configuration import ObservingSite

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["ObservingSiteModel"]

class ObservingSiteModel(ModelHelper):
    """Model class for the observing site configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, ObservingSite())
