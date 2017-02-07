from PyQt5 import QtWidgets

from lsst.sims.opsim4.widgets.wizard import WizardPages

__all__ = ["SkyUserRegionsPage"]

class SkyUserRegionsPage(QtWidgets.QWizardPage):
    """Main class for setting the proposal's sky user regions.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.setTitle("Sky User Regions Selection")

        label = QtWidgets.QLabel("Set the sky user regions for the proposals. These are to "
                                 "be specified as field Ids from the survey fields database.")
        label.setWordWrap(True)

        sky_user_regions_le = QtWidgets.QLineEdit()
        self.registerField("sky_user_regions*", sky_user_regions_le)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(sky_user_regions_le)

        self.setLayout(layout)

    def nextId(self):
        """Move to next page.
        """
        return WizardPages.PageSequenceSkyExclusions
