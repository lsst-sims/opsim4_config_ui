from opsim4.widgets import ConfigurationTab

__all__ = ["DomeWidget"]

class DomeWidget(ConfigurationTab):
    """Widget for the dome configuration information.
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
        """Create the UI form for the Dome widget.
        """
        self.create_widget("Float", "altitude_maxspeed", qualifier=self.name)
        self.create_widget("Float", "altitude_accel", qualifier=self.name)
        self.create_widget("Float", "altitude_decel", qualifier=self.name)
        self.create_widget("Float", "azimuth_maxspeed", qualifier=self.name)
        self.create_widget("Float", "azimuth_accel", qualifier=self.name)
        self.create_widget("Float", "azimuth_decel", qualifier=self.name)
        self.create_widget("Float", "settle_time", qualifier=self.name)
