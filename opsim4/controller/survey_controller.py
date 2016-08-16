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
