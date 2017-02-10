from lsst.sims.opsim4.widgets import ConfigurationTab

__all__ = ["EnvironmentWidget"]

class EnvironmentWidget(ConfigurationTab):
    """Widget for the enviornment configuration information.
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
        """Create the UI form for the Environment widget.
        """
        self.create_widget("File", "seeing_db")
        self.create_widget("File", "cloud_db")
        self.create_widget("Float", "telescope_seeing")
        self.create_widget("Float", "optical_design_seeing")
        self.create_widget("Float", "camera_seeing")
        self.create_widget("Float", "scale_to_eff")
        self.create_widget("Float", "geom_eff_factor")
