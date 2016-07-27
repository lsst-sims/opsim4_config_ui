from PyQt4 import QtCore

from opsim4.controller import BaseController
from opsim4.model import ScienceModel
from opsim4.widgets import ScienceWidget

__all__ = ["ScienceController"]

class ScienceController(BaseController):

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

        self.widget.create_tabs(self.model.ad_params)
        self.widget.set_information(self.model.ad_params)

        for i in xrange(self.widget.count()):
            tab = self.widget.widget(i)
            tab.checkProperty.connect(self.check_property)
            tab.getProperty.connect(self.get_property)
            tab.saveConfiguration.connect(self.save_configuration)
            #print("A:", tab.signal_mapper.mapping(0))

    @QtCore.pyqtSlot('QString', 'QString', list)
    def check_property(self, param_name, param_value, position):
        """Check the stored value of the parameter name against input.

        Parameters
        ----------
        param_name : QtCore.QString
            The parameter name to retrieve the stored value of.
        param_value : any
            The value of the parameter to check against the stored one.
        position : list[int]
            The widget position that requested this check.
        """
        print("Help2!", position)
        is_changed = self.model.check_parameter(str(param_name), param_value)
        print("AA:", param_name, param_value, is_changed)
        home_tab = str(param_name).split('/')[0]
        self.widget.is_changed(position, is_changed, home_tab=home_tab)
