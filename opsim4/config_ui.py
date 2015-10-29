import os

from PyQt4 import QtCore, QtGui

from lsst.sims.ocs.configuration.sim_config import SimulationConfig
from opsim4.config_tab import ConfigurationTab

class OpsimConfigDlg(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.save_directory = None

        self.tab_widget = QtGui.QTabWidget()
        self.create_tabs()

        self.buttonbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Cancel)
        self.connect(self.buttonbox, QtCore.SIGNAL("rejected()"), self, QtCore.SLOT("reject()"))
        self.connect(self.buttonbox, QtCore.SIGNAL("accepted()"), self.save_configurations)

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addWidget(self.buttonbox)
        self.setLayout(self.main_layout)

    def create_tabs(self):
        configuration = SimulationConfig()
        for key, obj in configuration.items():
            tab = ConfigurationTab(key, obj)
            self.tab_widget.addTab(tab, tab.title)

    def set_save_directory(self, save_dir):
        self.save_directory = save_dir

    @QtCore.pyqtSlot()
    def save_configurations(self):
        if self.save_directory is None:
                self.save_directory = os.curdir
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            tab.save(self.save_directory)

def run(opts):
    import sys
    app = QtGui.QApplication(sys.argv)
    form = OpsimConfigDlg()
    form.set_save_directory(opts.save_dir)
    form.show()
    app.exec_()
