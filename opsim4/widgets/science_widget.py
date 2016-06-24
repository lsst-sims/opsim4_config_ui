from PyQt4 import QtGui

from opsim4.widgets import ProposalWidget

__all__ = ["ScienceWidget"]

class ScienceWidget(QtGui.QTabWidget):

    def __init__(self, name, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        parent : QWidget
            The parent widget of this one.
        """
        QtGui.QTabWidget.__init__(self, parent)
        self.tab_name = name

    def create_tabs(self, names):
        """Create the individual proposal tabs.

        Parameters
        ----------
        names : list[str]
            The names for the configuration tabs.
        """
        for name in names:
            tab = ProposalWidget(name)
            self.addTab(tab, name)
