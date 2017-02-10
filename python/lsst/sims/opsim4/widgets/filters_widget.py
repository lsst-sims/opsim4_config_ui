from lsst.sims.opsim4.widgets import ConfigurationTab

__all__ = ["FiltersWidget"]

class FiltersWidget(ConfigurationTab):
    """Widget for the Filters configuration information.
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
        """Create the UI form for the Filters widget.
        """
        filters = "u,g,r,i,z,y"
        for ifilter in filters.split(','):
            self.create_widget("Float",
                               "{}_effective_wavelength".format(ifilter),
                               self.name)
