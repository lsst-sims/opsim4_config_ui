from lsst.sims.ocs.configuration import ObservingSite

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["ObservingSiteModel"]

class ObservingSiteModel(ModelHelper):
    """Model class for the observing site configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, ObservingSite())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            obs_site = ObservingSite()
            ModelHelper.load_config(obs_site, config_files)
            model = ModelHelper(obs_site)
            return model.params
