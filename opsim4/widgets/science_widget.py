from opsim4.widgets import ConfigurationTabWidget

__all__ = ["ScienceWidget"]

class ScienceWidget(ConfigurationTabWidget):

    def __init__(self, name, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        parent : QWidget
            The parent widget of this one.
        """
        ConfigurationTabWidget.__init__(self, parent)

    def create_tabs(self, params):
        """Create the individual proposal tabs.

        Parameters
        ----------
        params : dict{str : params}
            Set of configuration information.
        """
        ConfigurationTabWidget.create_tabs(self, "ProposalWidget", params)
