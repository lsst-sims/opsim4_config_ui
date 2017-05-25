from lsst.sims.ocs.configuration.instrument import Camera

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["CameraModel"]

class CameraModel(ModelHelper):
    """Model class for the camera configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Camera())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            camera = Camera()
            ModelHelper.load_config(camera, config_files)
            model = ModelHelper(camera)
            return model
