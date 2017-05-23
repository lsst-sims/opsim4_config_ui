from lsst.sims.ocs.configuration.instrument import Dome

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["DomeModel"]

class DomeModel(ModelHelper):
    """Model class for the dome configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Dome())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            dome = Dome()
            ModelHelper.load_config(dome, config_files)
            model = ModelHelper(dome)
            return model
