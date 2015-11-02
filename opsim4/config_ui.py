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

        self.buttonbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Close |
                                                QtGui.QDialogButtonBox.RestoreDefaults)

        reset_tab_button = QtGui.QPushButton("Reset Tab")
        reset_tab_button.setAutoDefault(False)
        self.buttonbox.addButton(reset_tab_button, QtGui.QDialogButtonBox.ResetRole)

        reset_field_button = QtGui.QPushButton("Reset Field")
        reset_field_button.setAutoDefault(False)
        self.buttonbox.addButton(reset_field_button, QtGui.QDialogButtonBox.ResetRole)

        self.buttonbox.rejected.connect(self.reject)
        self.buttonbox.accepted.connect(self.save_configurations)
        self.buttonbox.clicked.connect(self.check_buttonbox_clicked)

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

    def check_buttonbox_clicked(self, button):
        button_name = str(button.text())
        if "Restore Defaults" == button_name:
            self.reset_tabs()
        if "Reset Tab" == button_name:
            self.reset_active_tab()
        if "Reset Field" == button_name:
            self.reset_active_field()

    def reset_tabs(self):
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            tab.reset_all()

    def reset_active_tab(self):
        tab = self.tab_widget.widget(self.tab_widget.currentIndex())
        tab.reset_all()

    def reset_active_field(self):
        tab = self.tab_widget.widget(self.tab_widget.currentIndex())
        tab.reset_active_field()

def run(opts):
    import sys
    app = QtGui.QApplication(sys.argv)
    form = OpsimConfigDlg()
    form.set_save_directory(opts.save_dir)
    form.show()
    app.exec_()
