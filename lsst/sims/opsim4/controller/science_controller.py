from PyQt5 import QtCore

from lsst.sims.opsim4.controller import BaseController
from lsst.sims.opsim4.model import ScienceModel
from lsst.sims.opsim4.widgets import ScienceWidget

__all__ = ["ScienceController"]

class ScienceController(BaseController):
    """The controller for the science proposal configuration.
    """

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            Tab name for the configuration view.
        """
        BaseController.__init__(self, name)
        self.model = ScienceModel()
        self.widget = ScienceWidget(name)

        self.widget.create_tabs(self.model.general_params)
        self.widget.set_information(self.model.general_params)
        self.widget.create_tabs(self.model.sequence_params)
        self.widget.set_information(self.model.sequence_params)

        for i in xrange(self.widget.count()):
            tab = self.widget.widget(i)
            tab.checkProperty.connect(self.check_property)
            tab.getProperty.connect(self.get_property)
            tab.saveConfiguration.connect(self.save_configuration)

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
        home_tab = str(param_name).split('/')[0]
        self.widget.is_changed(position, is_changed, home_tab=home_tab)

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
        home_tab = str(param_name).split('/')[0]
        self.widget.reset_field(position, pvalue, home_tab=home_tab)
