import os

from PyQt4 import QtCore, QtGui

from lsst.sims.ocs.utilities.file_helpers import expand_path

from lsst.sims.opsim4 import __version__ as version
from lsst.sims.opsim4.controller import MainController
from lsst.sims.opsim4.utilities import title
from lsst.sims.opsim4.widgets import ReportDialog
from lsst.sims.opsim4.widgets.constants import CSS
from lsst.sims.opsim4.widgets.wizard import ProposalCreationWizard

class OpsimConfig(QtGui.QMainWindow):
    """Top-level UI.
    """
    RECENT_DIRECTORIES_TO_LIST = 9
    STATUS_BAR_TIMEOUT = 3000

    def __init__(self, parent=None):
        """Initialize the class.

        Parameters
        ----------
        parent : QWidget
            The parent widget of this one.
        """
        QtGui.QMainWindow.__init__(self, parent)
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
        file_clear_recent = self.create_action("Clear Recent List", self.clear_recent_list, "Ctrl+Alt+C",
                                               None, "Clear the list of recent directories.")

        file_save_configs = self.create_action("&Save Configuration", self.save_configurations,
                                               QtGui.QKeySequence.Save,
                                               None, "Save the configuration to files.")
        file_quit_action = self.create_action("&Quit", self.close, "Ctrl+Q", None,
                                              "Close the application,.")

        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu_actions = (file_set_save_dir, file_clear_recent, None,
                                  file_save_configs, file_quit_action)
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
        proposal_wizard = self.create_action("Proposal Creation", self.proposal_creation, "Ctrl+Alt+P", None,
                                             "Create a new proposal.")

        create_menu = self.menuBar().addMenu("Create")
        self.add_actions(create_menu, (diff_report, proposal_wizard))

    def create_help_menu(self):
        """Create the help menu for the UI.
        """
        help_about = self.create_action("&About", self.about, None, None,
                                        "About the OpSim Configuration UI program.")

        help_menu = self.menuBar().addMenu("&Help")
        self.add_actions(help_menu, (help_about,))

    def create_action(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        """Create menu actions.

        Parameters
        ----------
        text : str
            A label for the action.
        slot : QtCore.pyqtSlot, optional
            A callback function for the action.
        shortcut : str, optional
            A keyboard shortcut for the action.
        icon : str, optional
            An icon path for the action.
        tip : str, optional
            A tooltip string for the action.
        checkable : bool, optional
            Is the action checkable?
        signal : str, optional
            The signal associated with the action. Default: triggered()
        """
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
        """Add menu actions.

        Prameters
        ---------
        target : QMenuItem
            The menu item to add the action to.
        actions : list(QAction)
            THe set of actions to apply.
        """
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def clear_recent_list(self):
        """Clear out the list of recent directories.
        """
        self.recent_directories.clear()
        self.update_file_menu()

    def create_tabs(self):
        """Create all the configuration tabs.
        """
        tab_dict = self.main_controller.get_tabs()
        for key, tab in tab_dict.items():
            self.tab_widget.addTab(tab, title(key))

    @QtCore.pyqtSlot()
    def save_configurations(self):
        """Save the current differences to configuration files.
        """
        if self.save_directory is None:
                self.save_directory = os.curdir
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            tab.save(expand_path(str(self.save_directory)))
        self.statusBar().showMessage("Finished saving configuration.", self.STATUS_BAR_TIMEOUT)

    def reset_tabs(self):
        """Reset all fields in all tabs.
        """
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            tab.reset_all()
        self.statusBar().showMessage("Reset complete.", self.STATUS_BAR_TIMEOUT)

    def reset_active_tab(self):
        """Reser all fields in the active tab.
        """
        tab = self.tab_widget.widget(self.tab_widget.currentIndex())
        tab.reset_active_tab()
        self.statusBar().showMessage("Reset complete.", self.STATUS_BAR_TIMEOUT)

    def reset_active_field(self):
        """Reset the active field in the current tab.
        """
        tab = self.tab_widget.widget(self.tab_widget.currentIndex())
        tab.reset_active_field()
        self.statusBar().showMessage("Reset complete.", self.STATUS_BAR_TIMEOUT)

    def closeEvent(self, event):
        """Handle close events.

        This function mainly saves out the current settings before the program
        is shutdown.

        Parameters
        ----------
        event : QEvent
            The event to process.
        """
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
        """Add a new saved directory into the File menu list.
        """
        self.file_menu.clear()
        self.add_actions(self.file_menu, self.file_menu_actions[:-2])
        current = QtCore.QString(self.save_directory) if self.save_directory is not None else None

        recent_directories = []
        if current is not None:
            self.file_menu.addAction(QtGui.QAction("Current:", self))
            self.file_menu.addAction(QtGui.QAction(str(current), self))
        self.file_menu.addSeparator()

        for rdir in self.recent_directories:
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
        """Placeholder function until events can be processed correctly.
        """
        return True

    def set_internal_save_directory(self):
        action = self.sender()
        if isinstance(action, QtGui.QAction):
            self.save_directory = action.data().toString()
            self.update_file_menu()

    def set_save_directory(self):
        """Add a save directory to the internals of the program.
        """
        old_save_directory = self.save_directory
        self.save_directory = QtGui.QFileDialog.getExistingDirectory(self, "Set Save Directory",
                                                                     os.path.expanduser("~/"))

        if self.save_directory == "":
            self.save_directory = old_save_directory
            return

        if old_save_directory not in self.recent_directories:
            self.recent_directories.prepend(old_save_directory)
            while self.recent_directories.count() > self.RECENT_DIRECTORIES_TO_LIST:
                self.recent_directories.takeLast()
        self.update_file_menu()

    def get_diff_dict(self):
        """Get the dictionary of current differences.

        Returns
        -------
        dict
        """
        return self.main_controller.get_diff()

    def diff_report(self):
        """Show the current difference report.
        """
        dlg = ReportDialog()
        dlg.make_report(self.get_diff_dict())
        dlg.exec_()

    def proposal_creation(self):
        """Show the proposal creation wizard.
        """
        wizard = ProposalCreationWizard()
        wizard.set_save_directory(self.save_directory)
        wizard.resize(600, 500)
        wizard.exec_()

    def about(self):
        """Show information about the program.
        """
        QtGui.QMessageBox.about(self, "About OpSim Configuration UI",
                                """
                                <b>Operations Simulator Configuration UI</b> v{}
                                <p>This application is used to create override files and new
                                proposals to modify the running of the Operations Simulator
                                from the baseline configuration.
                                <br><br>
                                Copyright 2016 LSST Simulations
                                """.format(version))

def run(opts):
    """Run the program.

    Parameters
    ----------
    opts : Namespace
        Command-line options.
    """
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(CSS)
    app.setOrganizationName("LSST-Simulations")
    app.setOrganizationDomain("lsst.org")
    app.setApplicationName("Operations-Simulator-Configuration-UI")
    form = OpsimConfig()
    form.resize(600, 500)
    form.show()
    app.exec_()
