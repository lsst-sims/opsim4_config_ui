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

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            obs_var = ObservatoryVariation()
            ModelHelper.load_config(obs_var, config_files)
            model = ModelHelper(obs_var)
            return model
