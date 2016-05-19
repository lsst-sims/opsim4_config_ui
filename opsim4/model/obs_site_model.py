from lsst.sims.ocs.configuration import ObservingSite

from opsim4.model import ModelHelper

__all__ = ["ObservingSiteModel"]

class ObservingSiteModel(ModelHelper):

    def __init__(self):
        super(ObservingSiteModel, self).__init__(ObservingSite())
