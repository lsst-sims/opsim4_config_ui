from PyQt4 import QtGui

from opsim4.widgets import ConfigurationTab
from opsim4.utilities import title

class ConfigurationTabWidget(QtGui.QTabWidget):
    def __init__(self, tab_name, config_dict, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)

        self.tab_name = tab_name
        self.config_dict = config_dict
        self.create_tabs()

    def create_tabs(self):
        for key, obj in self.config_dict.items():
            tab = ConfigurationTab(key, obj)
            self.addTab(tab, title(key))

    def _active_widget(self):
        return self.widget(self.currentIndex())

    def save(self, save_dir):
        for i in range(self.count()):
            tab = self.widget(i)
            tab.save(save_dir)

    def reset_all(self):
        for i in range(self.count()):
            tab = self.widget(i)
            tab.reset_all()

    def reset_active_tab(self):
        tab = self._active_widget()
        tab.reset_active_tab()

    def reset_active_field(self):
        tab = self._active_widget()
        tab.reset_active_field()

    def get_diff(self):
        dd = {}
        for i in range(self.count()):
            tab = self.widget(i)
            #print("A:", self.tab_name)
            rd = tab.get_diff(self.tab_name)
            dd.update(rd)
        return dd
