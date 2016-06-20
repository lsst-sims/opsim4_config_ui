from PyQt4 import QtCore, QtGui

from opsim4.widgets import ConfigurationTab

__all__ = ["SurveyWidget"]

class SurveyWidget(ConfigurationTab):
    """Widget for the survey configuration information.
    """

    def __init__(self, name, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        """
        super(SurveyWidget, self).__init__(name, parent)

    def create_form(self):
        print("in create form")
        self.create_widget("Float", "duration")
        self.create_widget("Str", "start_date")
        self.create_widget("Float", "idle_delay")
