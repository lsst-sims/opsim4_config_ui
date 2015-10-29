from PyQt4 import QtCore, QtGui

from lsst.sims.ocs.configuration.sim_config import SimulationConfig
from opsim4.config_tab import ConfigurationTab

class OpsimConfigDlg(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)

        self.tab_widget = QtGui.QTabWidget()
        self.create_tabs()

        self.buttonbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Cancel)
        self.connect(self.buttonbox, QtCore.SIGNAL("rejected()"), self, QtCore.SLOT("reject()"))

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addWidget(self.buttonbox)
        self.setLayout(self.main_layout)

    def create_tabs(self):
        configuration = SimulationConfig()
        for key, obj in configuration.items():
            tab = ConfigurationTab(key, obj)
            self.tab_widget.addTab(tab, tab.title)

def run():
    import sys
    app = QtGui.QApplication(sys.argv)
    form = OpsimConfigDlg()
    form.show()
    app.exec_()
