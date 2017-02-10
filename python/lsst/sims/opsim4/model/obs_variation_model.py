from lsst.sims.ocs.configuration.instrument import ObservatoryVariation

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["ObservatoryVariationModel"]

class ObservatoryVariationModel(ModelHelper):
    """Model class for the observatory variation configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, ObservatoryVariation())
