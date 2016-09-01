from PyQt4 import QtGui

__all__ = ["SchedulingPage"]

class SchedulingPage(QtGui.QWizardPage):
    """Main class for setting the proposal's scheduling information.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtGui.QWizardPage.__init__(self, parent)
        self.setTitle("Scheduling Setup")

        label1 = QtGui.QLabel("Set the maximum number of targets to be sent to the scheduler "
                              "driver for final target consideration")
        label1.setWordWrap(True)

        max_num_targets_la = QtGui.QLabel("Max Number of Targets:")
        max_num_targets_le = QtGui.QLineEdit("100")
        max_num_targets_la.setBuddy(max_num_targets_le)
        int_validator = QtGui.QIntValidator()
        max_num_targets_le.setValidator(int_validator)
        self.registerField("scheduling_max_num_targets", max_num_targets_le)

        label2 = QtGui.QLabel("Set the checkbox to accept observed targets (field/filter) that "
                              "were not in the proposal's list of winners that were sent to the "
                              "scheduler driver.")
        label2.setWordWrap(True)

        accept_serendipity_la = QtGui.QLabel("Accept Serendipity:")
        accept_serendipity_cb = QtGui.QCheckBox()
        accept_serendipity_la.setBuddy(accept_serendipity_cb)
        self.registerField("scheduling_accept_serendipity", accept_serendipity_cb)

        label3 = QtGui.QLabel("Set the checkbox to accept back-to-back visits of the "
                              "same target (field/filter).")
        label3.setWordWrap(True)

        accept_consecutive_visits_la = QtGui.QLabel("Accept Consecutive Visits:")
        accept_consecutive_visits_cb = QtGui.QCheckBox()
        accept_consecutive_visits_la.setBuddy(accept_consecutive_visits_cb)
        self.registerField("scheduling_accept_consecutive_visits", accept_consecutive_visits_cb)

        layout = QtGui.QGridLayout()

        layout.addWidget(label1, 0, 0, 1, 2)
        layout.addWidget(max_num_targets_la, 1, 0)
        layout.addWidget(max_num_targets_le, 1, 1)
        layout.addWidget(label2, 2, 0, 1, 2)
        layout.addWidget(accept_serendipity_la, 3, 0)
        layout.addWidget(accept_serendipity_cb, 3, 1)
        layout.addWidget(label3, 4, 0, 1, 2)
        layout.addWidget(accept_consecutive_visits_la, 5, 0)
        layout.addWidget(accept_consecutive_visits_cb, 5, 1)

        self.setLayout(layout)
