from PyQt5 import QtGui, QtWidgets

from lsst.sims.opsim4.widgets.wizard import WizardPages

__all__ = ["SchedulingPage"]

class SchedulingPage(QtWidgets.QWizardPage):
    """Main class for setting the proposal's scheduling information.
    """

    def __init__(self, parent=None, is_general=True):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.setTitle("Scheduling Setup")
        self.is_general = is_general
        if self.is_general:
            self.param_tag = "general"
        else:
            self.param_tag = "sequence"

        label1 = QtWidgets.QLabel("Set the maximum number of targets to be sent to the scheduler "
                                  "driver for final target consideration")
        label1.setWordWrap(True)

        max_num_targets_la = QtWidgets.QLabel("Max Number of Targets:")
        max_num_targets_le = QtWidgets.QLineEdit("100")
        max_num_targets_la.setBuddy(max_num_targets_le)
        int_validator = QtGui.QIntValidator()
        max_num_targets_le.setValidator(int_validator)
        self.registerField("{}_scheduling_max_num_targets".format(self.param_tag), max_num_targets_le)

        label2 = QtWidgets.QLabel("Set the checkbox to accept observed targets (field/filter) that "
                                  "were not in the proposal's list of winners that were sent to the "
                                  "scheduler driver.")
        label2.setWordWrap(True)

        accept_serendipity_la = QtWidgets.QLabel("Accept Serendipity:")
        accept_serendipity_cb = QtWidgets.QCheckBox()
        accept_serendipity_la.setBuddy(accept_serendipity_cb)
        self.registerField("{}_scheduling_accept_serendipity".format(self.param_tag), accept_serendipity_cb)

        label3 = QtWidgets.QLabel("Set the checkbox to accept back-to-back visits of the "
                                  "same target (field/filter).")
        label3.setWordWrap(True)

        accept_consecutive_visits_la = QtWidgets.QLabel("Accept Consecutive Visits:")
        accept_consecutive_visits_cb = QtWidgets.QCheckBox()
        accept_consecutive_visits_la.setBuddy(accept_consecutive_visits_cb)
        self.registerField("{}_scheduling_accept_consecutive_visits".format(self.param_tag),
                           accept_consecutive_visits_cb)

        label4 = QtWidgets.QLabel("Set the airmass bonus for ranking requested fields.")
        label4.setWordWrap(True)

        airmass_bonus_la = QtWidgets.QLabel("Airmass Bonus:")
        airmass_bonus_le = QtWidgets.QLineEdit("0.5")
        airmass_bonus_la.setBuddy(airmass_bonus_le)
        airmass_bonus_le.setValidator(QtGui.QDoubleValidator())
        self.registerField("{}_scheduling_airmass_bonus".format(self.param_tag), airmass_bonus_le)

        label11 = QtWidgets.QLabel("Set the hour angle bonus for ranking requested fields.")
        label11.setWordWrap(True)

        hour_angle_bonus_la = QtWidgets.QLabel("Hour Angle Bonus:")
        hour_angle_bonus_le = QtWidgets.QLineEdit("0.0")
        hour_angle_bonus_la.setBuddy(hour_angle_bonus_le)
        hour_angle_bonus_le.setValidator(QtGui.QDoubleValidator())
        self.registerField("{}_scheduling_hour_angle_bonus".format(self.param_tag), hour_angle_bonus_le)

        if self.is_general:
            label5 = QtWidgets.QLabel("Set the checkbox to restrict the number of visits in a night of the "
                                      "same target (field/filter).")
            label5.setWordWrap(True)

            restrict_grouped_visits_la = QtWidgets.QLabel("Restrict Grouped Visits:")
            restrict_grouped_visits_cb = QtWidgets.QCheckBox()
            restrict_grouped_visits_la.setBuddy(restrict_grouped_visits_cb)
            self.registerField("scheduling_restrict_grouped_visits", restrict_grouped_visits_cb)

            label_img = QtWidgets.QLabel()
            label_img.setPixmap(QtGui.QPixmap(":/time_domain_window.png"))

            label6 = QtWidgets.QLabel("Set the time interval for subsequent revisits of the same target "
                                      "(field/filter) in a night. Leave zero if all filters only require a "
                                      "single target visit.")
            label6.setWordWrap(True)

            time_interval_la = QtWidgets.QLabel("Time Interval:")
            time_interval_le = QtWidgets.QLineEdit("0.0")
            time_interval_la.setBuddy(time_interval_le)
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

            label9 = QtWidgets.QLabel("Set the relative time where the ranking priority for a target "
                                      "drops to zero.")
            label9.setWordWrap(True)

            time_window_end_la = QtWidgets.QLabel("Time Window End:")
            time_window_end_le = QtWidgets.QLineEdit("0.0")
            time_window_end_la.setBuddy(time_window_end_le)
            time_window_end_le.setValidator(QtGui.QDoubleValidator())
            self.registerField("scheduling_time_window_end", time_window_end_le)

            label10 = QtWidgets.QLabel("Set the weighting value to scale the shape of the time "
                                       "window function.")
            label10.setWordWrap(True)

            time_weight_la = QtWidgets.QLabel("Time Weight:")
            time_weight_le = QtWidgets.QLineEdit("1.0")
            time_weight_la.setBuddy(time_weight_le)
            time_weight_le.setValidator(QtGui.QDoubleValidator())
            self.registerField("scheduling_time_weight", time_weight_le)

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
        scroll_area_widget_layout.addWidget(label11, 8, 0, 1, 3)
        scroll_area_widget_layout.addWidget(hour_angle_bonus_la, 9, 0)
        scroll_area_widget_layout.addWidget(hour_angle_bonus_le, 9, 1)
        if self.is_general:
            scroll_area_widget_layout.addWidget(label5, 10, 0, 1, 3)
            scroll_area_widget_layout.addWidget(restrict_grouped_visits_la, 11, 0)
            scroll_area_widget_layout.addWidget(restrict_grouped_visits_cb, 11, 1)
            scroll_area_widget_layout.addWidget(label_img, 12, 0, 1, 3)
            scroll_area_widget_layout.addWidget(label6, 13, 0, 1, 3)
            scroll_area_widget_layout.addWidget(time_interval_la, 14, 0)
            scroll_area_widget_layout.addWidget(time_interval_le, 14, 1)
            scroll_area_widget_layout.addWidget(time_interval_un, 14, 2)
            scroll_area_widget_layout.addWidget(label7, 15, 0, 1, 3)
            scroll_area_widget_layout.addWidget(time_window_start_la, 16, 0)
            scroll_area_widget_layout.addWidget(time_window_start_le, 16, 1)
            scroll_area_widget_layout.addWidget(label8, 17, 0, 1, 3)
            scroll_area_widget_layout.addWidget(time_window_max_la, 18, 0)
            scroll_area_widget_layout.addWidget(time_window_max_le, 18, 1)
            scroll_area_widget_layout.addWidget(label9, 19, 0, 1, 3)
            scroll_area_widget_layout.addWidget(time_window_end_la, 20, 0)
            scroll_area_widget_layout.addWidget(time_window_end_le, 20, 1)
            scroll_area_widget_layout.addWidget(label10, 21, 0, 1, 3)
            scroll_area_widget_layout.addWidget(time_weight_la, 22, 0)
            scroll_area_widget_layout.addWidget(time_weight_le, 22, 1)

        scroll_area_widget.setLayout(scroll_area_widget_layout)

        scrollable = QtWidgets.QScrollArea()
        scrollable.setWidgetResizable(True)
        scrollable.setWidget(scroll_area_widget)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(scrollable)
        self.setLayout(main_layout)

    def nextId(self):
        """Move to next page.
        """
        if self.is_general:
            return WizardPages.PageGeneralFilters
        else:
            return WizardPages.PageSequenceFilters
