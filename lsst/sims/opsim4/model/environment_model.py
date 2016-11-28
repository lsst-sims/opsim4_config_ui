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
