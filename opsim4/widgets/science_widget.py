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

    def active_tab(self):
        """Return the active tab.

        Returns
        -------
        :class:`.ProposalWidget`
        """
        return self.widget(self.currentIndex())

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

    def get_diff(self):
        """Get the changed parameters.

        Parameters
        ----------
        parent_name : str, optional
            The name of a parent tab.

        Returns
        -------
        dict{str: str}
            The set of changed parameters.
        """
        ddict = {}
        for i in xrange(self.count()):
            tab = self.widget(i)
            ddict.update(tab.get_diff())
        return ddict

    def is_changed(self, position, is_changed, home_tab=None):
        for i in xrange(self.count()):
            name = self.tabText(i)
            if name == home_tab:
                tab = self.widget(i)
                tab.is_changed(position, is_changed)

    def reset_active_tab(self):
        """Reset the current tab.
        """
        tab = self.active_tab()
        tab.reset_active_tab()

    def reset_all(self):
        """Reset all of the changed parameters.
        """
        for i in range(self.count()):
            tab = self.widget(i)
            tab.reset_all()

    def reset_field(self, position, param_value, home_tab=None):
        """Reset a specific parameter widget.

        Parameters
        ----------
        position : list[int]
            The position (usually row) of the widget to reset.
        param_value : str
            The string representation of the parameter value.
        """
        for i in xrange(self.count()):
            name = self.tabText(i)
            if name == home_tab:
                tab = self.widget(i)
                tab.reset_field(position, param_value)

    def reset_active_field(self):
        """Reset the active field.
        """
        tab = self.active_tab()
        print("Z:", tab.name)
        tab.reset_active_field()

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
