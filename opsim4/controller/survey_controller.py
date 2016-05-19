from opsim4.controller import BaseController
from opsim4.model import SurveyModel
from opsim4.widgets import ConfigurationTab

__all__ = ["SurveyController"]

class SurveyController(BaseController):

    def __init__(self, name):
        super(SurveyController, self).__init__(name)
        self.model = SurveyModel()
        params = self.model.make_parameter_dictionary()
        self.widget = ConfigurationTab(self.name, params)
