from opsim4.widgets import ConfigurationTab

__all__ = ["ParkWidget"]

class ParkWidget(ConfigurationTab):
    """Widget for the observatory park configuration information.
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
        """Create the UI form for the Park widget.
        """
        self.create_widget("Float", "telescope_altitude", qualifier=self.name)
        self.create_widget("Float", "telescope_azimuth", qualifier=self.name)
        self.create_widget("Float", "telescope_rotator", qualifier=self.name)
        self.create_widget("Float", "dome_altitude", qualifier=self.name)
        self.create_widget("Float", "dome_azimuth", qualifier=self.name)
        self.create_widget("Str", "filter_position", qualifier=self.name)
