import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from lsst.sims.ocs.utilities.file_helpers import expand_path
from lsst.sims.ocs.version import __version__ as socs_version

from lsst.sims.opsim4 import __version__ as version
from lsst.sims.opsim4.controller import MainController
from lsst.sims.opsim4.utilities import NEW_PROPS_DIR, title
from lsst.sims.opsim4.widgets import ReportDialog
from lsst.sims.opsim4.widgets.constants import CSS
from lsst.sims.opsim4.widgets.wizard import ProposalCreationWizard

class OpsimConfig(QtWidgets.QMainWindow):
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
        QtWidgets.QMainWindow.__init__(self, parent)
        self.save_directory = None
        self.file_menu_offset = -3
        self.extra_props_dir = None

        self.create_file_menu()
        self.create_reset_menu()
        self.create_create_menu()
        self.create_help_menu()

        self.tab_widget = QtWidgets.QTabWidget()
        self.main_controller = MainController()
        self.create_tabs()

        self.setCentralWidget(self.tab_widget)

        settings = QtCore.QSettings()
        self.recent_directories = settings.value("RecentDirectories")
        setting_save_dir = str(settings.value("LastDirectory"))
        if setting_save_dir != "":
            self.save_directory = setting_save_dir
        self.update_file_menu()

    def create_file_menu(self):
        """Create the file menu for the UI.
        """
        file_set_save_dir = self.create_action("Save Directory", self.set_save_directory, "Ctrl+D",
                                               "folder_open.svg",
                                               "Set the directory where the configurations will be saved.")
        file_clear_recent = self.create_action("Clear Recent List", self.clear_recent_list, "Ctrl+Alt+C",
                                               "clear.svg", "Clear the list of recent directories.")
        file_apply_overrides = self.create_action("Apply Overrides", self.apply_overrides, "Ctrl+Alt+O",
                                                  "bottom.svg",
                                                  "Apply override files to current configuration.")
        file_save_configs = self.create_action("&Save Configuration", self.save_configurations,
                                               QtGui.QKeySequence.Save,
                                               "filesave.svg", "Save the configuration to files.")
        file_quit_action = self.create_action("&Quit", self.close, "Ctrl+Q", "exit.svg",
                                              "Close the application.")

        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu_actions = (file_set_save_dir, file_clear_recent, None,
                                  file_apply_overrides, file_save_configs,
                                  file_quit_action)
        self.file_menu.aboutToShow.connect(self.update_file_menu)

    def create_reset_menu(self):
        """Create the reset menu for the UI.
        """
        reset_all_defaults = self.create_action("All Defaults", self.reset_tabs, "Ctrl+R", "undo.svg",
                                                "Reset all values to defaults.")
        reset_active_tab_defaults = self.create_action("Active Tab Defaults", self.reset_active_tab, "Ctrl+T",
                                                       "undo_tab.svg",
                                                       "Reset all values in the active tab.")
        reset_active_field_default = self.create_action("Active Field Default", self.reset_active_field,
                                                        "Ctrl+Alt+F", "undo_field.svg",
                                                        "Reset value of the active field.")
        reset_overrides = self.create_action("Overrides", self.reset_overrides, "Ctrl+Alt+Shift+O",
                                             "undo_override.svg",
                                             "Reset overrides including new proposals.")

        reset_menu = self.menuBar().addMenu("Reset")
        self.add_actions(reset_menu, (reset_all_defaults, reset_active_tab_defaults,
                                      reset_active_field_default, reset_overrides))

    def create_create_menu(self):
        """ Create the create menu for the UI.
        """
        diff_report = self.create_action("Diff Report", self.diff_report, "Ctrl+Alt+R", "snavigator.svg",
                                         "Generate a difference report.")
        proposal_wizard = self.create_action("Proposal Creation", self.proposal_creation, "Ctrl+Alt+P",
                                             "document_new.svg",
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
                      signal_name="triggered"):
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
        signal_name : str, optional
            The signal associated with the action. Default: triggered
        """
        action = QtWidgets.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(QtGui.QPixmap(":/{}".format(icon))))
            action.setIconVisibleInMenu(True)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            signal = getattr(action, signal_name)
            signal.connect(slot)
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
        self.recent_directories = []
        self.update_file_menu()

    def create_tabs(self):
        """Create all the configuration tabs.
        """
        tab_dict = self.main_controller.get_tabs()
        for key, tab in tab_dict.items():
            self.tab_widget.addTab(tab, title(key))

    def apply_overrides(self):
        """Apply override configuration files to current configuration.
        """
        old_save_directory = self.save_directory
        if old_save_directory == 'None':
            open_dir = os.path.expanduser("~/")
        else:
            open_dir = os.path.dirname(old_save_directory)
        override_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Override Directory",
                                                                  open_dir)
        if override_dir == "":
            return

        config_files = []
        for item in os.listdir(override_dir):
            ifile = os.path.join(override_dir, item)
            if os.path.isfile(ifile):
                config_files.append(ifile)

        extra_props = None
        alt_prop_dir = os.path.join(override_dir, NEW_PROPS_DIR)
        if os.path.exists(alt_prop_dir):
            extra_props = alt_prop_dir
            sys.path.insert(0, extra_props)
            self.extra_props_dir = extra_props

        if len(config_files) or extra_props is not None:
            self.main_controller.apply_overrides(config_files, extra_props)

    @QtCore.pyqtSlot()
    def save_configurations(self):
        """Save the current differences to configuration files.
        """
        message = "Finished saving configuration"
        if self.save_directory is None:
            self.save_directory = os.curdir
            message += " in current working directory."
        else:
            message += "."
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            tab.save(expand_path(str(self.save_directory)))
        self.statusBar().showMessage(message, self.STATUS_BAR_TIMEOUT)
        if self.save_directory == os.curdir:
            self.save_directory = None

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

    def reset_overrides(self):
        """Reset all values from overrides including new proposals.
        """
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            tab.reset_all()

        if self.extra_props_dir is not None:
            sys.path.remove(self.extra_props_dir)
            self.main_controller.remove_extra_proposals()
            self.extra_props_dir = None
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
            save_directory = QtCore.QVariant(self.save_directory) \
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
        self.add_actions(self.file_menu, self.file_menu_actions[:self.file_menu_offset])
        current = self.save_directory if self.save_directory is not None else None

        recent_directories = []
        if current is not None:
            self.file_menu.addAction(QtWidgets.QAction("Current:", self))
            self.file_menu.addAction(QtWidgets.QAction(str(current), self))
        self.file_menu.addSeparator()

        if self.recent_directories is not None:
            for rdir in self.recent_directories:
                if rdir != current and QtCore.QDir.exists(QtCore.QDir(rdir)):
                    recent_directories.append(rdir)
            if len(recent_directories) != 0:
                self.file_menu.addSeparator()
                self.file_menu.addAction(QtWidgets.QAction("Recent:", self))
                for i, rdir in enumerate(recent_directories):
                    action = QtWidgets.QAction("&{} {}".format(i + 1, rdir), self)
                    action.setData(QtCore.QVariant(rdir))
                    action.triggered.connect(self.set_internal_save_directory)
                    self.file_menu.addAction(action)
        else:
            self.recent_directories = []
        self.file_menu.addSeparator()
        self.add_actions(self.file_menu, self.file_menu_actions[self.file_menu_offset:])

    def ok_to_continue(self):
        """Placeholder function until events can be processed correctly.
        """
        return True

    def set_internal_save_directory(self):
        action = self.sender()
        if isinstance(action, QtWidgets.QAction):
            old_save_directory = self.save_directory
            self.save_directory = action.data()
            if self.save_directory in self.recent_directories:
                try:
                    self.recent_directories.remove(self.save_directory)
                except ValueError:
                    pass
            self.recent_directories.insert(0, old_save_directory)
            self.update_file_menu()

    def set_save_directory(self):
        """Add a save directory to the internals of the program.
        """
        old_save_directory = self.save_directory
        if old_save_directory == 'None':
            open_dir = os.path.expanduser("~/")
        else:
            open_dir = os.path.dirname(old_save_directory)
        self.save_directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Set Save Directory",
                                                                         open_dir)

        if self.save_directory == "":
            self.save_directory = old_save_directory
            return

        if old_save_directory is None:
            return

        if old_save_directory not in self.recent_directories:
            self.recent_directories.insert(0, old_save_directory)
            while len(self.recent_directories) > self.RECENT_DIRECTORIES_TO_LIST:
                self.recent_directories.pop()
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
        self.statusBar().showMessage("Proposal saved.", self.STATUS_BAR_TIMEOUT)

    def about(self):
        """Show information about the program.
        """
        about = QtWidgets.QMessageBox()
        about.setIconPixmap(QtGui.QPixmap(":/socs_logo.png"))
        about.setWindowTitle("About OpSim4 Configuration UI")
        about.setStandardButtons(QtWidgets.QMessageBox.Ok)
        about.setInformativeText("""
                                 <b>Operations Simulator Configuration UI</b>
                                 <p>Version {}</p>
                                 <p>SOCS Version: {}</p>
                                 <p>This application is used to create override files and new
                                 proposals to modify the running of the Operations Simulator
                                 from the baseline configuration.
                                 <br><br>
                                 Copyright 2016-2017 LSST Simulations
                                 """.format(version, socs_version))

        about.exec_()

def run(opts):
    """Run the program.

    Parameters
    ----------
    opts : Namespace
        Command-line options.
    """
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(CSS)
    app.setOrganizationName("LSST-Simulations")
    app.setOrganizationDomain("lsst.org")
    app.setApplicationName("Operations-Simulator-Configuration-UI")
    form = OpsimConfig()
    form.resize(800, 500)
    form.show()
    app.exec_()
