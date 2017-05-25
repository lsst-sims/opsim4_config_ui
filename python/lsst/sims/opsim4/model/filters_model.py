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

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            filters = Filters()
            ModelHelper.load_config(filters, config_files)
            model = ModelHelper(filters)
            return model
