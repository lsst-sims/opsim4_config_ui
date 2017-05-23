from lsst.sims.ocs.configuration.instrument import Rotator

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["RotatorModel"]

class RotatorModel(ModelHelper):
    """Model class for the rotator configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Rotator())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            rotator = Rotator()
            ModelHelper.load_config(rotator, config_files)
            model = ModelHelper(rotator)
            return model
