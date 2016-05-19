from opsim4.controller import BaseController
from opsim4.model import ObservingSiteModel
from opsim4.widgets import ConfigurationTab

__all__ = ["ObservingSiteController"]

class ObservingSiteController(BaseController):

    def __init__(self, name):
        super(ObservingSiteController, self).__init__(name)
        self.model = ObservingSiteModel()
        params = self.model.make_parameter_dictionary()
        self.widget = ConfigurationTab(self.name, params)
