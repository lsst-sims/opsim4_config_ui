from PyQt5 import QtWidgets

__all__ = ["ConfigurationTabWidget"]

class ConfigurationTabWidget(QtWidgets.QTabWidget):
    """Configuration widget that holds configuration sub-tabs.
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
        QtWidgets.QTabWidget.__init__(self, parent)
        self.tab_name = name

    def active_tab(self):
        """Return the active tab.

        Returns
        -------
        QWidget
        """
        return self.widget(self.currentIndex())

    def create_tabs(self, params):
        """Create the individual proposal tabs.

        Parameters
        ----------
        params : dict{str : params}
            Set of configuration information.
        """
        raise NotImplementedError("Classes must override this!")

    def get_diff(self):
        """Get the changed parameters.

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
        """Determine if parameter has changed.

        This function is the result of checking that a parameter
        has changed. It passes control to the underlying parameter
        widget.

        Parameters
        ----------
        position : list(int)
            The position (usually row) of the widget to reset.
        is_changed : bool
            Flag to declaring value at position has changed.
        home_tab : str, optional
            The name of the tab to search.
        """
        for i in xrange(self.count()):
            tab = self.widget(i)
            if home_tab == tab.name:
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
        position : list(int)
            The position (usually row) of the widget to reset.
        param_value : str
            The string representation of the parameter value.
        home_tab : str, optional
            The name of the tab to search.
        """
        for i in xrange(self.count()):
            tab = self.widget(i)
            if home_tab == tab.name:
                tab.reset_field(position, param_value)

    def reset_active_field(self):
        """Reset the active field.
        """
        tab = self.active_tab()
        tab.reset_active_field()

    def save(self, save_dir):
        """Get the changed parameters for saving.

        Parameters
        ----------
        save_dir : str
            The directory for saving the configuration in.
        """
        for i in xrange(self.count()):
            tab = self.widget(i)
            tab.save(save_dir)

    def set_information(self, param_dict):
        """Set information for the configuration tabs.

        Parameters
        ----------
        param_dict : dict
            The set of information for the configuration
        """
        for i in xrange(self.count()):
            tab = self.widget(i)
            tab.set_information(param_dict[tab.name])
