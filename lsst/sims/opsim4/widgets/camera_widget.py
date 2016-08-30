from lsst.sims.opsim4.widgets import ConfigurationTab

__all__ = ["CameraWidget"]

class CameraWidget(ConfigurationTab):
    """Widget for the camera configuration information.
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
        """Create the UI form for the Camera widget.
        """
        self.create_widget("Float", "readout_time", qualifier=self.name)
        self.create_widget("Float", "shutter_time", qualifier=self.name)
        self.create_widget("Float", "filter_mount_time", qualifier=self.name)
        self.create_widget("Float", "filter_change_time", qualifier=self.name)
        self.create_widget("Int", "filter_max_changes_burst_num", qualifier=self.name)
        self.create_widget("Float", "filter_max_changes_burst_time", qualifier=self.name)
        self.create_widget("Int", "filter_max_changes_avg_num", qualifier=self.name)
        self.create_widget("Float", "filter_max_changes_avg_time", qualifier=self.name)
        self.create_widget("StringList", "filter_mounted", qualifier=self.name)
        self.create_widget("Str", "filter_pos", qualifier=self.name)
        self.create_widget("StringList", "filter_removable", qualifier=self.name)
        self.create_widget("StringList", "filter_unmounted", qualifier=self.name)
