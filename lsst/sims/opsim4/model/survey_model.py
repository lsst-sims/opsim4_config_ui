from lsst.sims.ocs.configuration import Survey

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["SurveyModel"]

class SurveyModel(ModelHelper):
    """Model class for the survey configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        survey = Survey()
        ModelHelper.__init__(self, survey)

        self.proposals = {"GEN": survey.general_proposals}

    def get_parameter(self, parameter_name):
        """Get a value for the given parameter.

        Parameters
        ----------
        parameter_name : str
            The name of the parameter to fetch the value of.

        Returns
        -------
        any
            The associated parameter value.
        """
        if "gen_proposals" in parameter_name:
            return list(self.proposals["GEN"])
        else:
            return ModelHelper.get_parameter(self, parameter_name)

    def is_proposal_active(self, pname):
        """Determine if proposal is active.

        Parameters
        ----------
        pname : str
            The proposal name to check.
        """
        is_active = False
        for props in self.proposals.values():
            if pname in props:
                is_active = True
                break
        return is_active
