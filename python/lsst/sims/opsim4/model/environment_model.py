from lsst.sims.ocs.configuration import Environment

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["EnvironmentModel"]

class EnvironmentModel(ModelHelper):
    """Model class for the environment configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Environment())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            environment = Environment()
            ModelHelper.load_config(environment, config_files)
            model = ModelHelper(environment)
            return model.params
