from PyQt4 import QtGui

__all__ = ["SkyNightlyBoundsPage"]

class SkyNightlyBoundsPage(QtGui.QWizardPage):
    """Main class for setting the proposal's sky nightly bounds.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtGui.QWizardPage.__init__(self, parent)
        self.setTitle("Sky Nightly Bounds")

        validator = QtGui.QDoubleValidator()

        label1 = QtGui.QLabel("Set the sun's altitude that corresponds to the acceptable start "
                              "of night for the proposal.")
        label1.setWordWrap(True)

        twilight_bound_la = QtGui.QLabel("Twilight Boundary:")
        twilight_bound_le = QtGui.QLineEdit("-12.0")
        twilight_bound_le.setValidator(validator)
        self.registerField("sky_nightly_bounds_twilight_boundary", twilight_bound_le)
        twilight_bound_un = QtGui.QLabel("degrees")

        label2 = QtGui.QLabel("The extra window on either side of the sunset (-) or sunrise (+) "
                              "LST in which the proposal will consider those fields for the night "
                              "along with those fields between sunset and sunrise LST.")
        label2.setWordWrap(True)

        delta_lst_la = QtGui.QLabel("Delta LST:")
        delta_lst_le = QtGui.QLineEdit("60.0")
        delta_lst_le.setValidator(validator)
        self.registerField("sky_nightly_bounds_delta_lst", delta_lst_le)
        delta_lst_un = QtGui.QLabel("degrees")

        layout = QtGui.QGridLayout()

        layout.addWidget(label1, 0, 0, 1, 4)

        layout.addWidget(twilight_bound_la, 1, 0)
        layout.addWidget(twilight_bound_le, 1, 1, 1, 2)
        layout.addWidget(twilight_bound_un, 1, 3)

        layout.addWidget(label2, 2, 0, 1, 4)

        layout.addWidget(delta_lst_la, 3, 0)
        layout.addWidget(delta_lst_le, 3, 1, 1, 2)
        layout.addWidget(delta_lst_un, 3, 3)

        self.setLayout(layout)
