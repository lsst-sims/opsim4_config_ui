from PyQt4 import QtGui

from opsim4.config_tab import ConfigurationTab
from utilities import load_class, title

class ConfigurationTabWidget(QtGui.QTabWidget):
    def __init__(self, tab_name, config_obj, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)

        self.tab_name = tab_name
        self.config_obj = config_obj
        self.config_cls = load_class(self.config_obj)
        self.create_tabs()

    def create_tabs(self):
        for key, obj in self.config_obj.items():
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
