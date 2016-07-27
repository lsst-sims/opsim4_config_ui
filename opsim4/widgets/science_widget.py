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

    def create_tabs(self, params):
        """Create the individual proposal tabs.

        Parameters
        ----------
        names : list[str]
            The names for the configuration tabs.
        """
        #for name in names:
        for name, values in params.items():
            tab = ProposalWidget(name, values)
            self.addTab(tab, name)

    def is_changed(self, position, is_changed, home_tab=None):
        for i in xrange(self.count()):
            name = self.tabText(i)
            if name == home_tab:
                tab = self.widget(i)
                tab.is_changed(position, is_changed)

    def set_information(self, param_dict):
        """Set information for the configuration tabs.

        Parameters
        ----------
        param_dict : dict
            The set of information for the configuration
        """
        for key, value in param_dict.items():
            for i in xrange(self.count()):
                name = self.tabText(i)
                if name == key:
                    tab = self.widget(i)
                    tab.set_information(value)
