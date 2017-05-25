from lsst.sims.ocs.configuration import Downtime

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["DowntimeModel"]

class DowntimeModel(ModelHelper):
    """Model class for the downtime configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Downtime())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            downtime = Downtime()
            ModelHelper.load_config(downtime, config_files)
            model = ModelHelper(downtime)
            return model.params
