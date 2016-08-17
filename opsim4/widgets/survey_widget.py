from PyQt4 import QtCore, QtGui

from opsim4.widgets import ConfigurationTab
from opsim4.widgets.constants import CSS_GROUPBOX

__all__ = ["SurveyWidget"]

class SurveyWidget(ConfigurationTab):
    """Widget for the survey configuration information.
    """

    def __init__(self, name, proposals, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        proposals : dict
            The default set of proposals.
        parent : QWidget
            The parent widget of this one.
        """
        self.proposals = proposals
        ConfigurationTab.__init__(self, name, parent=parent)

    def create_form(self):
        """Create the UI form for the Survey widget.
        """
        self.create_widget("Float", "duration")
        self.create_widget("Str", "start_date")
        self.create_widget("Float", "idle_delay")

        ad_group_box = QtGui.QGroupBox("Area Distribution Proposals")
        ad_group_box.setStyleSheet(CSS_GROUPBOX)
        glayout = QtGui.QGridLayout()

        for i, prop_name in enumerate(self.proposals["AD"]):
            self.create_widget("Bool", prop_name, layout=glayout, rows=i)
            # prop_label = QtGui.QLabel(prop_name)
            # check_box = QtGui.QCheckBox()
            # prop_label.setBuddy(check_box)
            # check_box.setChecked(True)
            # check_box.stateChanged.connect(self.check_prop)
            # glayout.addWidget(prop_label, i, 0)
            # glayout.addWidget(check_box, i, 1)

        ad_group_box.setLayout(glayout)

        self.layout.addWidget(ad_group_box, 3, 0, 1, 3)

    # def check_prop(self, state):
    #     """Check state changes from the proposal checkboxes.

    #     Parameters
    #     ----------
    #     state : int
    #         The current state of the proposal checkbox.
    #     """
    #     cb = self.sender()
    #     if state == QtCore.Qt.Unchecked:
    #         cb.setText(str(cb.text()) + self.CHANGED_PARAMETER)
    #         self.change_label_color(cb, QtCore.Qt.red)
    #     if state == QtCore.Qt.Checked:
    #         cb.setText(str(cb.text()).strip(self.CHANGED_PARAMETER))
    #         self.change_label_color(cb, QtCore.Qt.black)

