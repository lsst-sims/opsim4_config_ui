from lsst.sims.ocs.configuration.instrument import OpticsLoopCorr

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["OpticsLoopCorrModel"]

class OpticsLoopCorrModel(ModelHelper):
    """Model class for the optics loop correction configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, OpticsLoopCorr())
