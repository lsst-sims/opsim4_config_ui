from lsst.sims.opsim4.widgets import ConfigurationTab

__all__ = ["OpticsLoopCorrWidget"]

class OpticsLoopCorrWidget(ConfigurationTab):
    """Widget for the optics loop correction configuration information.
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
        """Create the UI form for the OpticsLoopCorr widget.
        """
        self.create_widget("Float", "tel_optics_ol_slope", qualifier=self.name)
        self.create_widget("FloatList", "tel_optics_cl_alt_limit", qualifier=self.name)
        self.create_widget("FloatList", "tel_optics_cl_delay", qualifier=self.name)
