from PyQt4 import QtGui

from opsim4.widgets.constants import CSS_GROUPBOX

__all__ = ["ProposalTypePage"]

class ProposalTypePage(QtGui.QWizardPage):
    """Main class for deciding the proposal type to create.
    """

    def __init__(self, parent=None):
        """Initialize class.

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtGui.QWizardPage.__init__(self, parent)
        self.setTitle("Proposal Type Choice")

        label = QtGui.QLabel("Choose a proposal type to create.")

        group_box = QtGui.QGroupBox("Proposal Type")
        group_box.setStyleSheet(CSS_GROUPBOX)

        ad_radio = QtGui.QRadioButton("Area Distribution")
        td_radio = QtGui.QRadioButton("Time Dependent")
        ad_radio.setChecked(True)

        self.registerField("area_dist_choice", ad_radio)
        self.registerField("time_dep_choice", td_radio)

        gb_layout = QtGui.QVBoxLayout()
        gb_layout.addWidget(ad_radio)
        gb_layout.addWidget(td_radio)
        gb_layout.addStretch(1)

        group_box.setLayout(gb_layout)

        name_label = QtGui.QLabel("Provide a name for the proposal. Please do not use "
                                  "spaces in the name.")
        name_label.setWordWrap(True)

        name_le = QtGui.QLineEdit()
        self.registerField("proposal_name*", name_le)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(group_box)
        layout.addWidget(name_label)
        layout.addWidget(name_le)

        self.setLayout(layout)
