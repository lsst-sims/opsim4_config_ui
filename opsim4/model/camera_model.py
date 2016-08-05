from lsst.sims.ocs.configuration.instrument import Camera

from opsim4.model import ModelHelper

__all__ = ["CameraModel"]

class CameraModel(ModelHelper):
    """Model class for the camera configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Camera())
