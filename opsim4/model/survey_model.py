from lsst.sims.ocs.configuration import Survey

from opsim4.model import ModelHelper

__all__ = ["SurveyModel"]

class SurveyModel(ModelHelper):
    def __init__(self):
        super(SurveyModel, self).__init__(Survey())
