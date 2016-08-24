from opsim4.controller import BaseController
from opsim4.model import SurveyModel
from opsim4.widgets import SurveyWidget

__all__ = ["SurveyController"]

class SurveyController(BaseController):
    """The controller for the survey configuration.
    """

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The tab name for the configuration view.
        """
        BaseController.__init__(self, name)
        self.model = SurveyModel()
        self.widget = SurveyWidget(name, self.model.proposals)

        for key, value in self.model.params.items():
            self.widget.set_information(key, value)

        self.widget.checkProperty.connect(self.check_property)
        self.widget.getProperty.connect(self.get_property)
        self.widget.saveConfiguration.connect(self.save_configuration)

    def check_property(self, param_name, param_value, position):
        """Check the stored value of the parameter name against input.

        Parameters
        ----------
        param_name : QString
            The parameter name to retrieve the stored value of.
        param_value : any
            The value of the parameter to check against the stored one.
        position : list(int)
            The widget position that requested this check.
        """
        pname = str(param_name)
        pvalue = str(param_value)
        if "ad_proposals" in pname:
            prop_name = pname.split('/')[-1]
            if pvalue == "True":
                is_changed = self.model.is_proposal_active(prop_name)
            else:
                is_changed = False
            self.widget.is_changed(position, is_changed)
        else:
            BaseController.check_property(self, param_name, param_value, position)

    def get_property(self, param_name, position):
        """Get the property value for the requested name.

        Parameters
        ----------
        param_name : QString
            The parameter name to retrieve the stored value of.
        position : list(int)
            The widget position that requested this check.
        """
        pname = str(param_name)
        if "ad_proposals" in pname:
            prop_name = pname.split('/')[-1]
            print("Help")
            pass
        else:
            BaseController.get_property(self, param_name, position)
