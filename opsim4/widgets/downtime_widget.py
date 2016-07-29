from opsim4.widgets import ConfigurationTab

__all__ = ["DowntimeWidget"]

class DowntimeWidget(ConfigurationTab):
    """Widget for the downtime configuration information.
    """

    def __init__(self, name, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        parent : QWidget
            The parent widget of this one.
        """
        ConfigurationTab.__init__(self, name, parent)

    def create_form(self):
        """Create the UI form for the Downtime widget.
        """
        self.create_widget("Str", "scheduled_downtime_db")
        self.create_widget("Bool", "unscheduled_downtime_use_random_seed")
        self.create_widget("Int", "unscheduled_downtime_random_seed")
