from lsst.sims.opsim4.widgets import ConfigurationTabWidget, ProposalWidget

__all__ = ["ScienceWidget"]

class ScienceWidget(ConfigurationTabWidget):
    """Widget containing the widgets for science proposal configuration.
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
        ConfigurationTabWidget.__init__(self, name, parent)

    def create_tabs(self, params):
        """Create the individual proposal tabs.

        Parameters
        ----------
        params : dict(str: params)
            Set of configuration information.
        """
        for name, values in params.items():
            tab = ProposalWidget(name, values)
            self.addTab(tab, name)
