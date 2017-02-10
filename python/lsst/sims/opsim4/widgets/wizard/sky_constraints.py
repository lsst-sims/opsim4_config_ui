from PyQt5 import QtGui, QtWidgets

from lsst.sims.opsim4.widgets.wizard import WizardPages

__all__ = ["SkyConstraintsPage"]

class SkyConstraintsPage(QtWidgets.QWizardPage):
    """Main class for setting the proposal's sky constraints.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.setTitle("Sky Constraints")

        label = QtWidgets.QLabel("Set the maxium airmass that is acceptable for any field "
                                 "in the proposal.")
        label.setWordWrap(True)

        max_airmass_la = QtWidgets.QLabel("Maximum Airmass:")
        max_airmass_le = QtWidgets.QLineEdit("2.5")
        max_airmass_la.setBuddy(max_airmass_le)
        max_airmass_validator = QtGui.QDoubleValidator()
        max_airmass_validator.setBottom(1.0)
        max_airmass_le.setValidator(max_airmass_validator)
        self.registerField("sky_constraints_max_airmass", max_airmass_le)

        label2 = QtWidgets.QLabel("Set the maximum fraction of clouds that is acceptable for "
                                  "any field in the proposal.")
        label2.setWordWrap(True)

        max_cloud_la = QtWidgets.QLabel("Maximum Cloud:")
        max_cloud_le = QtWidgets.QLineEdit("0.7")
        max_cloud_la.setBuddy(max_cloud_le)
        max_cloud_validator = QtGui.QDoubleValidator()
        max_cloud_validator.setBottom(0.0)
        max_cloud_le.setValidator(max_cloud_validator)
        self.registerField("sky_constraints_max_cloud", max_cloud_le)

        label3 = QtWidgets.QLabel("Set the minimum distance to the moon that a field can have "
                                  "in the proposal.")
        label3.setWordWrap(True)

        min_distance_moon_la = QtWidgets.QLabel("Minimum Distance to Moon:")
        min_distance_moon_le = QtWidgets.QLineEdit("30.0")
        min_distance_moon_la.setBuddy(min_distance_moon_le)
        min_distance_moon_validator = QtGui.QDoubleValidator()
        min_distance_moon_validator.setBottom(0.0)
        min_distance_moon_le.setValidator(min_distance_moon_validator)
        min_distance_moon_un = QtWidgets.QLabel("degrees")
        self.registerField("sky_constraints_min_distance_moon", min_distance_moon_le)

        label4 = QtWidgets.QLabel("Set checkbox to use 2 degrees exclusion around bright planets.")
        label4.setWordWrap(True)

        exclude_planets_la = QtWidgets.QLabel("Exclude Planets:")
        exclude_planets_cb = QtWidgets.QCheckBox()
        exclude_planets_la.setBuddy(exclude_planets_cb)
        self.registerField("sky_constraints_exclude_planets", exclude_planets_cb)

        layout = QtWidgets.QGridLayout()

        layout.addWidget(label, 0, 0, 1, 4)

        layout.addWidget(max_airmass_la, 1, 0)
        layout.addWidget(max_airmass_le, 1, 1, 1, 2)

        layout.addWidget(label2, 2, 0, 1, 4)

        layout.addWidget(max_cloud_la, 3, 0)
        layout.addWidget(max_cloud_le, 3, 1, 1, 2)

        layout.addWidget(label3, 4, 0, 1, 4)

        layout.addWidget(min_distance_moon_la, 5, 0)
        layout.addWidget(min_distance_moon_le, 5, 1, 1, 2)
        layout.addWidget(min_distance_moon_un, 5, 3)

        layout.addWidget(label4, 6, 0, 1, 4)

        layout.addWidget(exclude_planets_la, 7, 0)
        layout.addWidget(exclude_planets_cb, 7, 1, 1, 2)

        self.setLayout(layout)

    def nextId(self):
        """Move to next page.
        """
        if self.wizard().hasVisitedPage(WizardPages.PageSkyRegions):
            return WizardPages.PageGeneralScheduling
        else:
            return WizardPages.PageSubSequences
