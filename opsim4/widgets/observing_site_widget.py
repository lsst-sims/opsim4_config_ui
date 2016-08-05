from opsim4.widgets import ConfigurationTab

__all__ = ["ObservingSiteWidget"]

class ObservingSiteWidget(ConfigurationTab):
    """Widget for the observing site configuration information.
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
        ConfigurationTab.__init__(self, name, parent=parent)

    def create_form(self):
        """Create the UI form for the ObservingSite widget.
        """
        self.create_widget("Str", "name")
        self.create_widget("Float", "latitude")
        self.create_widget("Float", "longitude")
        self.create_widget("Float", "height")
        self.create_widget("Float", "pressure")
        self.create_widget("Float", "temperature")
        self.create_widget("Float", "relative_humidity")
