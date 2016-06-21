from PyQt4 import QtCore

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
        super(SurveyController, self).__init__(name)
        self.model = SurveyModel()
        self.widget = SurveyWidget(name)

        for key, value in self.model.params.items():
            self.widget.set_information(key, value)

        self.widget.checkProperty.connect(self.check_property)
