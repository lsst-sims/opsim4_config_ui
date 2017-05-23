from PyQt5 import QtCore

__all__ = ["BaseController"]

class BaseController(QtCore.QObject):
    """This class handles the basic set of information for the view controllers.
    """

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name of tab the controller is responsible for.
        """
        QtCore.QObject.__init__(self)
        self.name = name
        self.model = None
        self.widget = None

    def apply_overrides(self, config_files):
        """Apply configuration overrides.

        Parameters
        ----------
        config_files : list
            The list of configuration file paths.
        """
        params = self.model.apply_overrides(config_files)
        for key, value in params.items():
            self.widget.set_information(key, value, full_check=True)
        self.widget.full_check = False

    @QtCore.pyqtSlot(str, str, list)
    def check_property(self, param_name, param_value, position):
        """Check the stored value of the parameter name against input.

        Parameters
        ----------
        param_name : str
            The parameter name to retrieve the stored value of.
        param_value : any
            The value of the parameter to check against the stored one.
        position : list(int)
            The widget position that requested this check.
        """
        is_changed = self.model.check_parameter(str(param_name), param_value)
        self.widget.is_changed(position, is_changed)

    @QtCore.pyqtSlot(str, list)
    def get_property(self, param_name, position):
        """Get the property value for the requested name.

        Parameters
        ----------
        param_name : str
            The parameter name to retrieve the stored value of.
        position : list(int)
            The widget position that requested this check.
        """
        pvalue = str(self.model.get_parameter(str(param_name)))
        self.widget.reset_field(position, pvalue)

    def get_diff(self):
        """Get the changed parameters and associated defaults.

        Returns
        -------
        dict
            Set of changed parameters and their associated defaults.
        """
        diff_dict = self.widget.get_diff()
        for top_prop, prop in diff_dict.items():
            for prop_name in prop:
                if "/" in top_prop:
                    property_name = "{}/{}".format(top_prop, prop_name)
                else:
                    property_name = prop_name
                default_value = self.model.get_parameter(property_name)
                if isinstance(default_value, list):
                    default_value = ",".join([str(x) for x in default_value])
                else:
                    default_value = str(default_value)
                prop[prop_name].append(default_value)
        return diff_dict

    def get_tab(self):
        """Return the view controller's widget.

        Returns
        -------
        QWidget
        """
        return self.widget

    @QtCore.pyqtSlot(str, str, list)
    def save_configuration(self, save_dir, name, changed_params):
        """Delegate configuration saving to model.

        Parameters
        ----------
        save_dir : str
            The directory to save the configuration information to.
        name : str
            Name of the configuration to save.
        changed_params : dict
            The set of changed information.
        """
        self.model.save_configuration(save_dir, name, changed_params)
