from opsim4.widgets import ConfigurationTab

__all__ = ["SurveyWidget"]

class SurveyWidget(ConfigurationTab):
    """Widget for the survey configuration information.
    """

    def __init__(self, name, proposals, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        proposals : dict
            The default set of proposals.
        parent : QWidget
            The parent widget of this one.
        """
        ConfigurationTab.__init__(self, name, parent=parent)

    def create_form(self):
        """Create the UI form for the Survey widget.
        """
        self.create_widget("Float", "duration")
        self.create_widget("Str", "start_date")
        self.create_widget("Float", "idle_delay")
