from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = ["ProposalTypePage"]

class ProposalTypePage(QtWidgets.QWizardPage):
    """Main class for deciding the proposal type to create.
    """

    def __init__(self, parent=None):
        """Initialize class.

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.setTitle("Proposal Type Choice")

        label = QtWidgets.QLabel("Choose a proposal type to create.")

        group_box = QtWidgets.QGroupBox("Proposal Type")

        general_radio = QtWidgets.QRadioButton("General (Area, Hybrid, Time-Domain)")
        sequence_radio = QtWidgets.QRadioButton("Sequence (Deep Drilling, Nested Subsequences)")
        general_radio.setChecked(True)

        self.registerField("general_choice", general_radio)
        self.registerField("sequence_choice", sequence_radio)

        gb_layout = QtWidgets.QVBoxLayout()
        gb_layout.addWidget(general_radio)
        gb_layout.addWidget(sequence_radio)
        gb_layout.addStretch(1)

        group_box.setLayout(gb_layout)

        name_label = QtWidgets.QLabel("Provide a name for the proposal with a leading capital letter."
                                      " Please do not use spaces in the name.")
        name_label.setWordWrap(True)

        name_le = QtWidgets.QLineEdit()
        name_le.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'[A-Z]\w+')))
        self.registerField("proposal_name*", name_le)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(group_box)
        layout.addWidget(name_label)
        layout.addWidget(name_le)

        self.setLayout(layout)
