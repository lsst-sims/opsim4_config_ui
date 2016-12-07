from PyQt5 import QtGui, QtWidgets

__all__ = ["SchedulingPage"]

class SchedulingPage(QtWidgets.QWizardPage):
    """Main class for setting the proposal's scheduling information.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.setTitle("Scheduling Setup")

        label1 = QtWidgets.QLabel("Set the maximum number of targets to be sent to the scheduler "
                                  "driver for final target consideration")
        label1.setWordWrap(True)

        max_num_targets_la = QtWidgets.QLabel("Max Number of Targets:")
        max_num_targets_le = QtWidgets.QLineEdit("100")
        max_num_targets_la.setBuddy(max_num_targets_le)
        int_validator = QtGui.QIntValidator()
        max_num_targets_le.setValidator(int_validator)
        self.registerField("scheduling_max_num_targets", max_num_targets_le)

        label2 = QtWidgets.QLabel("Set the checkbox to accept observed targets (field/filter) that "
                                  "were not in the proposal's list of winners that were sent to the "
                                  "scheduler driver.")
        label2.setWordWrap(True)

        accept_serendipity_la = QtWidgets.QLabel("Accept Serendipity:")
        accept_serendipity_cb = QtWidgets.QCheckBox()
        accept_serendipity_la.setBuddy(accept_serendipity_cb)
        self.registerField("scheduling_accept_serendipity", accept_serendipity_cb)

        label3 = QtWidgets.QLabel("Set the checkbox to accept back-to-back visits of the "
                                  "same target (field/filter).")
        label3.setWordWrap(True)

        accept_consecutive_visits_la = QtWidgets.QLabel("Accept Consecutive Visits:")
        accept_consecutive_visits_cb = QtWidgets.QCheckBox()
        accept_consecutive_visits_la.setBuddy(accept_consecutive_visits_cb)
        self.registerField("scheduling_accept_consecutive_visits", accept_consecutive_visits_cb)

        label4 = QtWidgets.QLabel("Set the airmass bonus for ranking requested fields.")
        label4.setWordWrap(True)

        airmass_bonus_la = QtWidgets.QLabel("Airmass Bonus:")
        airmass_bonus_le = QtWidgets.QLineEdit("0.5")
        airmass_bonus_la.setBuddy(airmass_bonus_le)
        airmass_bonus_le.setValidator(QtGui.QDoubleValidator())
        self.registerField("scheduling_airmass_bonus", airmass_bonus_le)

        label5 = QtWidgets.QLabel("Set the checkbox to restrict the number of visits in a night of the "
                                  "same target (field/filter).")
        label5.setWordWrap(True)

        restrict_grouped_visits_la = QtWidgets.QLabel("Restrict Grouped Visits:")
        restrict_grouped_visits_cb = QtWidgets.QCheckBox()
        restrict_grouped_visits_la.setBuddy(restrict_grouped_visits_cb)
        self.registerField("scheduling_restrict_grouped_visits", restrict_grouped_visits_cb)

        label6 = QtWidgets.QLabel("Set the time interval for subsequent revisits of the same target "
                                  "(field/filter) in a night. Leave zero if all filters only require a "
                                  "single target visit.")
        label6.setWordWrap(True)

        time_interval_la = QtWidgets.QLabel("Time Interval:")
        time_interval_le = QtWidgets.QLineEdit("0.0")
        time_interval_la.setBuddy(time_interval_le)
        time_interval_le.setValidator(QtGui.QDoubleValidator())
        time_interval_un = QtWidgets.QLabel("seconds")
        self.registerField("scheduling_time_interval", time_interval_le)

        label7 = QtWidgets.QLabel("Set the relative time where the ranking priority for a target starts "
                                  "increasing linearly.")
        label7.setWordWrap(True)

        time_window_start_la = QtWidgets.QLabel("Time Window Start:")
        time_window_start_le = QtWidgets.QLineEdit("0.0")
        time_window_start_la.setBuddy(time_window_start_le)
        time_window_start_le.setValidator(QtGui.QDoubleValidator())
        self.registerField("scheduling_time_window_start", time_window_start_le)

        label8 = QtWidgets.QLabel("Set the relative time where the ranking priority for a target reaches "
                                  "maximum.")
        label8.setWordWrap(True)

        time_window_max_la = QtWidgets.QLabel("Time Window Max:")
        time_window_max_le = QtWidgets.QLineEdit("0.0")
        time_window_max_la.setBuddy(time_window_max_le)
        time_window_max_le.setValidator(QtGui.QDoubleValidator())
        self.registerField("scheduling_time_window_max", time_window_max_le)

        label9 = QtWidgets.QLabel("Set the relative time where the ranking priority for a target drops to "
                                  "zero.")
        label9.setWordWrap(True)

        time_window_end_la = QtWidgets.QLabel("Time Window End:")
        time_window_end_le = QtWidgets.QLineEdit("0.0")
        time_window_end_la.setBuddy(time_window_end_le)
        time_window_end_le.setValidator(QtGui.QDoubleValidator())
        self.registerField("scheduling_time_window_end", time_window_end_le)

        scroll_area_widget = QtWidgets.QWidget()
        scroll_area_widget_layout = QtWidgets.QGridLayout()

        scroll_area_widget_layout.addWidget(label1, 0, 0, 1, 3)
        scroll_area_widget_layout.addWidget(max_num_targets_la, 1, 0)
        scroll_area_widget_layout.addWidget(max_num_targets_le, 1, 1)
        scroll_area_widget_layout.addWidget(label2, 2, 0, 1, 3)
        scroll_area_widget_layout.addWidget(accept_serendipity_la, 3, 0)
        scroll_area_widget_layout.addWidget(accept_serendipity_cb, 3, 1)
        scroll_area_widget_layout.addWidget(label3, 4, 0, 1, 3)
        scroll_area_widget_layout.addWidget(accept_consecutive_visits_la, 5, 0)
        scroll_area_widget_layout.addWidget(accept_consecutive_visits_cb, 5, 1)
        scroll_area_widget_layout.addWidget(label4, 6, 0, 1, 3)
        scroll_area_widget_layout.addWidget(airmass_bonus_la, 7, 0)
        scroll_area_widget_layout.addWidget(airmass_bonus_le, 7, 1)
        scroll_area_widget_layout.addWidget(label5, 8, 0, 1, 3)
        scroll_area_widget_layout.addWidget(restrict_grouped_visits_la, 9, 0)
        scroll_area_widget_layout.addWidget(restrict_grouped_visits_cb, 9, 1)
        scroll_area_widget_layout.addWidget(label6, 10, 0, 1, 3)
        scroll_area_widget_layout.addWidget(time_interval_la, 11, 0)
        scroll_area_widget_layout.addWidget(time_interval_le, 11, 1)
        scroll_area_widget_layout.addWidget(time_interval_un, 11, 2)
        scroll_area_widget_layout.addWidget(label7, 12, 0, 1, 3)
        scroll_area_widget_layout.addWidget(time_window_start_la, 13, 0)
        scroll_area_widget_layout.addWidget(time_window_start_le, 13, 1)
        scroll_area_widget_layout.addWidget(label8, 14, 0, 1, 3)
        scroll_area_widget_layout.addWidget(time_window_max_la, 15, 0)
        scroll_area_widget_layout.addWidget(time_window_max_le, 15, 1)
        scroll_area_widget_layout.addWidget(label9, 16, 0, 1, 3)
        scroll_area_widget_layout.addWidget(time_window_end_la, 17, 0)
        scroll_area_widget_layout.addWidget(time_window_end_le, 17, 1)

        scroll_area_widget.setLayout(scroll_area_widget_layout)

        scrollable = QtWidgets.QScrollArea()
        scrollable.setWidgetResizable(True)
        scrollable.setWidget(scroll_area_widget)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(scrollable)
        self.setLayout(main_layout)
