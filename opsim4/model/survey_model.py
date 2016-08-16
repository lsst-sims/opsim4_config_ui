from lsst.sims.ocs.configuration import Survey

from opsim4.model import ModelHelper

__all__ = ["SurveyModel"]

class SurveyModel(ModelHelper):
    """Model class for the survey configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        survey = Survey()
        ModelHelper.__init__(self, survey)

        self.proposals = {"AD": survey.ad_proposals.split(',')}
