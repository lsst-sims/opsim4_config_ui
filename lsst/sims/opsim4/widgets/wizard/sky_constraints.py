from PyQt4 import QtGui

__all__ = ["SkyConstraintsPage"]

class SkyConstraintsPage(QtGui.QWizardPage):
    """Main class for setting the proposal's sky constraints.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtGui.QWizardPage.__init__(self, parent)
        self.setTitle("Sky Constraints")

        validator = QtGui.QDoubleValidator()

        label = QtGui.QLabel("Set the maxium airmass that is acceptable for any field "
                             "in the proposal.")
        label.setWordWrap(True)

        max_airmass_la = QtGui.QLabel("Maximum Airmass:")
        max_airmass_le = QtGui.QLineEdit("2.5")
        max_airmass_la.setBuddy(max_airmass_le)
        max_airmass_le.setValidator(validator)
        self.registerField("sky_constraints_max_airmass", max_airmass_le)
        max_airmass_un = QtGui.QLabel("degrees")

        layout = QtGui.QGridLayout()

        layout.addWidget(label, 0, 0, 1, 4)

        layout.addWidget(max_airmass_la, 1, 0)
        layout.addWidget(max_airmass_le, 1, 1, 1, 2)
        layout.addWidget(max_airmass_un, 1, 3)

        self.setLayout(layout)
