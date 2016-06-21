from PyQt4 import QtCore

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

    @QtCore.pyqtSlot('QString', 'QString', int)
    def check_property(self, param_name, param_value, position):
        """Check the stored value of the parameter name against input.

        Parameters
        ----------
        param_name : QtCore.QString
            The parameter name to retrieve the stored value of.
        param_value : any
            The value of the parameter to check against the stored one.
        position : int
            The widget position that requested this check.
        """
        print("Help!")
        is_changed = self.model.check_parameter(str(param_name), param_value)
        print("A:", param_name, param_value, is_changed)
        self.widget.is_changed(position, is_changed)

    @QtCore.pyqtSlot('QString', int)
    def get_property(self, param_name, position):
        """Get the property value for the requested name.

        Parameters
        ----------
        param_name : QtCore.QString
            The parameter name to retrieve the stored value of.
        position : int
            The widget position that requested this check.
        """
        pvalue = str(self.model.get_parameter(str(param_name)))
        print("Resetting:", param_name, pvalue)
        self.widget.reset_field(position, pvalue)

    def get_tab(self):
        """Return the view controller's widget.
        """
        return self.widget

    @QtCore.pyqtSlot('QString', str, list)
    def save_configuration(self, save_dir, name, changed_params):
        """Delegate configuration saving to model.
        """
        self.model.save_configuration(str(save_dir), name, changed_params)
