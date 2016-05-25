from opsim4.controller import BaseController
from opsim4.model import ObservatoryModel
from opsim4.widgets import ConfigurationTabWidget

__all__ = ["ObservatoryController"]

class ObservatoryController(BaseController):

    def __init__(self, name):
        super(ObservatoryController, self).__init__(name)
        self.model = ObservatoryModel()
        params = self.model.make_parameter_dictionary()
        self.widget = ConfigurationTabWidget(self.name, params)
