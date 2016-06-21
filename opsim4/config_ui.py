import os

from PyQt4 import QtCore, QtGui

from lsst.sims.ocs.utilities.file_helpers import expand_path
from opsim4.controller import MainController
from .report_dlg import ReportDialog
from .utilities import title
from . import version

class OpsimConfig(QtGui.QMainWindow):
    """Top-level UI.
    """
    RECENT_DIRECTORIES_TO_LIST = 9
    STATUS_BAR_TIMEOUT = 3000

    def __init__(self, parent=None):
        """Initialize the class.
        """
        super(OpsimConfig, self).__init__(parent)
        self.save_directory = None

        self.create_file_menu()
        self.create_reset_menu()
        self.create_create_menu()
        self.create_help_menu()

        self.tab_widget = QtGui.QTabWidget()
        self.main_controller = MainController()
        self.create_tabs()

        self.setCentralWidget(self.tab_widget)

        settings = QtCore.QSettings()
        self.recent_directories = settings.value("RecentDirectories").toStringList()
        self.save_directory = str(settings.value("LastDirectory").toString())
        self.update_file_menu()

    def create_file_menu(self):
        """Create the file menu for the UI.
        """
        file_set_save_dir = self.create_action("Save Directory", self.set_save_directory, "Ctrl+D", None,
                                               "Set the directory where the configurations will be saved.")
        file_save_configs = self.create_action("&Save Configuration", self.save_configurations,
                                               QtGui.QKeySequence.Save,
                                               None, "Save the configuration to files.")
        file_quit_action = self.create_action("&Quit", self.close, "Ctrl+Q", None,
                                              "Close the application,.")

        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu_actions = (file_set_save_dir, None, file_save_configs, file_quit_action)
        self.file_menu.aboutToShow.connect(self.update_file_menu)

    def create_reset_menu(self):
        """Create the reset menu for the UI.
        """
        reset_all_defaults = self.create_action("All Defaults", self.reset_tabs, "Ctrl+R", None,
                                                "Reset all values to defaults.")
        reset_active_tab_defaults = self.create_action("Active Tab Defaults", self.reset_active_tab, "Ctrl+T",
                                                       None,
                                                       "Reset all values in the active tab.")
        reset_active_field_default = self.create_action("Active Field Default", self.reset_active_field,
                                                        "Ctrl+Alt+F", None,
                                                        "Reset value of the active field.")

        reset_menu = self.menuBar().addMenu("Reset")
        self.add_actions(reset_menu, (reset_all_defaults, reset_active_tab_defaults,
                                      reset_active_field_default))

    def create_create_menu(self):
        """ Create the create menu for the UI.
        """
        diff_report = self.create_action("Diff Report", self.diff_report, "Ctrl+Alt+R", None,
                                         "Generate a difference report.")

        create_menu = self.menuBar().addMenu("Create")
        self.add_actions(create_menu, (diff_report,))

    def create_help_menu(self):
        """Create the help menu for the UI.
        """
        help_about = self.create_action("&About", self.about, None, None,
                                        "About the OpSim Configuration UI program.")

        help_menu = self.menuBar().addMenu("&Help")
        self.add_actions(help_menu, (help_about,))

    def create_action(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/{}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_tabs(self):
        """Create all the configuration tabs.
        """
        tab_dict = self.main_controller.get_tabs()
        for key, tab in tab_dict.items():
            self.tab_widget.addTab(tab, title(key))

    @QtCore.pyqtSlot()
    def save_configurations(self):
        if self.save_directory is None:
                self.save_directory = os.curdir
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            tab.save(expand_path(str(self.save_directory)))
        self.statusBar().showMessage("Finished saving configuration.", self.STATUS_BAR_TIMEOUT)

    def reset_tabs(self):
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            tab.reset_all()
        self.statusBar().showMessage("Reset complete.", self.STATUS_BAR_TIMEOUT)

    def reset_active_tab(self):
        tab = self.tab_widget.widget(self.tab_widget.currentIndex())
        tab.reset_active_tab()
        self.statusBar().showMessage("Reset complete.", self.STATUS_BAR_TIMEOUT)

    def reset_active_field(self):
        tab = self.tab_widget.widget(self.tab_widget.currentIndex())
        tab.reset_active_field()
        self.statusBar().showMessage("Reset complete.", self.STATUS_BAR_TIMEOUT)

    def closeEvent(self, event):
        if self.ok_to_continue():
            settings = QtCore.QSettings()
            save_directory = QtCore.QVariant(QtCore.QString(self.save_directory)) \
                if self.save_directory is not None else QtCore.QVariant()
            settings.setValue("LastDirectory", save_directory)
            recent_directories = QtCore.QVariant(self.recent_directories) \
                if self.recent_directories else QtCore.QVariant()
            settings.setValue("RecentDirectories", recent_directories)
        else:
            event.ignore()

    def update_file_menu(self):
        #print("Update menu")
        self.file_menu.clear()
        self.add_actions(self.file_menu, self.file_menu_actions[:-2])
        current = QtCore.QString(self.save_directory) if self.save_directory is not None else None
        #print(current)
        recent_directories = []
        if current is not None:
            self.file_menu.addAction(QtGui.QAction("Current:", self))
            self.file_menu.addAction(QtGui.QAction(str(current), self))
        self.file_menu.addSeparator()
        #print("C:", self.recent_directories.count())
        for rdir in self.recent_directories:
            #print("A:", rdir)
            if rdir != current and QtCore.QDir.exists(QtCore.QDir(rdir)):
                recent_directories.append(rdir)
        if len(recent_directories) != 0:
            self.file_menu.addSeparator()
            self.file_menu.addAction(QtGui.QAction("Recent:", self))
            for i, rdir in enumerate(recent_directories):
                action = QtGui.QAction("&{} {}".format(i + 1, rdir), self)
                action.setData(QtCore.QVariant(rdir))
                action.triggered.connect(self.set_internal_save_directory)
                self.file_menu.addAction(action)
        self.file_menu.addSeparator()
        self.add_actions(self.file_menu, self.file_menu_actions[-2:])

    def ok_to_continue(self):
        return True

    def set_internal_save_directory(self):
        action = self.sender()
        if isinstance(action, QtGui.QAction):
            self.save_directory = action.data().toString()
            self.update_file_menu()

    def set_save_directory(self):
        self.save_directory = QtGui.QFileDialog.getExistingDirectory(self, "Set Save Directory",
                                                                     os.path.expanduser("~/"))

        if self.save_directory not in self.recent_directories:
            #print("Not here")
            self.recent_directories.prepend(self.save_directory)
            #print(self.recent_directories.count())
            while self.recent_directories.count() > self.RECENT_DIRECTORIES_TO_LIST:
                self.recent_directories.takeLast()
        self.update_file_menu()

    def get_diff_dict(self):
        # diff_dict = {}
        # for i in range(self.tab_widget.count()):
        #     tab = self.tab_widget.widget(i)
        #     rd = tab.get_diff()
        #     diff_dict.update(rd)
        # return diff_dict
        return self.main_controller.get_diff()

    def diff_report(self):
        dlg = ReportDialog()
        dlg.make_report(self.get_diff_dict())
        dlg.exec_()

    def about(self):
        QtGui.QMessageBox.about(self, "About OpSim Configuration UI",
                                """
                                <b>Operations Simulator Configuration UI</b> v{}
                                <p>This application is used to create override files to
                                modify the running of the Operations Simulator from the baseline
                                configuration.
                                <br><br>
                                Copyright 2016 LSST Simulations
                                """.format(version.version))

def run(opts):
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("LSST-Simulations")
    app.setOrganizationDomain("lsst.org")
    app.setApplicationName("Operations-Simulator-Configuration-UI")
    form = OpsimConfig()
    form.show()
    app.exec_()
