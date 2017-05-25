from lsst.sims.ocs.configuration.instrument import OpticsLoopCorr

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["OpticsLoopCorrModel"]

class OpticsLoopCorrModel(ModelHelper):
    """Model class for the optics loop correction configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, OpticsLoopCorr())

    def apply_overrides(self, config_files):
            """Apply configuration overrides.

            Parameters
            ----------
            config_files : list
                The list of configuration file paths.
            """
            optics_loop_corr = OpticsLoopCorr()
            ModelHelper.load_config(optics_loop_corr, config_files)
            model = ModelHelper(optics_loop_corr)
            return model
