from lsst.sims.ocs.configuration.instrument import Telescope

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["TelescopeModel"]

class TelescopeModel(ModelHelper):
    """Model class for the telescope configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Telescope())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            telescope = Telescope()
            ModelHelper.load_config(telescope, config_files)
            model = ModelHelper(telescope)
            return model
