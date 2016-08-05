from opsim4.widgets import ConfigurationTab

__all__ = ["RotatorWidget"]

class RotatorWidget(ConfigurationTab):
    """Widget for the rotator configuration information.
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
        """Create the UI form for the Rotator widget.
        """
        self.create_widget("Float", "minpos", qualifier=self.name)
        self.create_widget("Float", "maxpos", qualifier=self.name)
        self.create_widget("Float", "filter_change_pos", qualifier=self.name)
        self.create_widget("Bool", "follow_sky", qualifier=self.name)
        self.create_widget("Bool", "resume_angle", qualifier=self.name)
        self.create_widget("Float", "maxspeed", qualifier=self.name)
        self.create_widget("Float", "accel", qualifier=self.name)
        self.create_widget("Float", "decel", qualifier=self.name)
