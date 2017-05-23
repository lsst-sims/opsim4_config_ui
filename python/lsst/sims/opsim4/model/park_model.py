from lsst.sims.ocs.configuration.instrument import Park

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["ParkModel"]

class ParkModel(ModelHelper):
    """Model class for the park configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Park())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            park = Park()
            ModelHelper.load_config(park, config_files)
            model = ModelHelper(park)
            return model
