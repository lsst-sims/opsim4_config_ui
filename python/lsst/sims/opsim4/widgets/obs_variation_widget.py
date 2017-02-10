from lsst.sims.opsim4.widgets import ConfigurationTab

__all__ = ["ObservatoryVariationWidget"]

class ObservatoryVariationWidget(ConfigurationTab):
    """Widget for the observatory variation configuration information.
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
        """Create the UI form for the ObservatoryVariation widget.
        """
        self.create_widget("Bool", "apply_variation", qualifier=self.name)
        self.create_widget("Float", "telescope_change", qualifier=self.name)
        self.create_widget("Float", "dome_change", qualifier=self.name)
