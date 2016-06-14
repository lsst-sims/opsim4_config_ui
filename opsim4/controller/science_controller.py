from opsim4.controller import BaseController
from opsim4.model import ScienceModel
from opsim4.widgets import ConfigurationTabWidget

__all__ = ["ScienceController"]

class ScienceController(BaseController):

    def __init__(self, name):
        super(ScienceController, self).__init__(name)
        self.model = ScienceModel()
        params = self.model.make_parameter_dictionary()
        #print(params)
        self.widget = ConfigurationTabWidget(self.name, params)
