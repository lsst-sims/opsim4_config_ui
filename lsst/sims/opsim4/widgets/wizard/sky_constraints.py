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

        label = QtGui.QLabel("Set the maxium airmass that is acceptable for any field "
                             "in the proposal.")
        label.setWordWrap(True)

        max_airmass_la = QtGui.QLabel("Maximum Airmass:")
        max_airmass_le = QtGui.QLineEdit("2.5")
        max_airmass_la.setBuddy(max_airmass_le)
        max_airmass_validator = QtGui.QDoubleValidator()
        max_airmass_validator.setBottom(1.0)
        max_airmass_le.setValidator(max_airmass_validator)
        self.registerField("sky_constraints_max_airmass", max_airmass_le)

        label2 = QtGui.QLabel("Set the maximum fraction of clouds that is acceptable for "
                              "any field in the proposal.")
        label2.setWordWrap(True)

        max_cloud_la = QtGui.QLabel("Maximum Cloud:")
        max_cloud_le = QtGui.QLineEdit("0.7")
        max_cloud_la.setBuddy(max_cloud_le)
        max_cloud_validator = QtGui.QDoubleValidator()
        max_cloud_validator.setBottom(0.0)
        max_cloud_le.setValidator(max_cloud_validator)
        self.registerField("sky_constraints_max_cloud", max_cloud_le)

        layout = QtGui.QGridLayout()

        layout.addWidget(label, 0, 0, 1, 4)

        layout.addWidget(max_airmass_la, 1, 0)
        layout.addWidget(max_airmass_le, 1, 1, 1, 2)

        layout.addWidget(label2, 2, 0, 1, 4)

        layout.addWidget(max_cloud_la, 3, 0)
        layout.addWidget(max_cloud_le, 3, 1, 1, 2)

        self.setLayout(layout)
