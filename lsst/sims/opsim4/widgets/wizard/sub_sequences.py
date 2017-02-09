import os

from PyQt5 import QtGui, QtWidgets

from lsst.sims.opsim4.widgets.wizard import WizardPages

__all__ = ["SubSequencesPage"]

class SubSequencesPage(QtWidgets.QWizardPage):
    """Main class for setting the proposal's sub-sequences.
    """

    def __init__(self, parent=None, is_nested=False):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        is_nested : bool
            Flag for nested or normal sub-sequence mode.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.is_nested = is_nested
        if not self.is_nested:
            self.title_name = "Sub-Sequence"
        else:
            self.title_name = "Nested Sub-Sequence"
        self.text_name = self.title_name.lower()

        self.setTitle("{} Specifications".format(self.title_name))

        label = QtWidgets.QLabel("Set the parameters for a {} in the form provided.".format(self.text_name))
        label.setWordWrap(True)

        group_box = QtWidgets.QGroupBox("{}".format(self.title_name))

        label1 = QtWidgets.QLabel("Set the identifier for the {}.".format(self.text_name))
        label1.setWordWrap(True)

        name_la = QtWidgets.QLabel("{} Name:".format(self.title_name))
        if not self.is_nested:
            self.name_le = QtWidgets.QLineEdit()
        else:
            self.name_le = QtWidgets.QComboBox()
        name_la.setBuddy(self.name_le)

        label2 = QtWidgets.QLabel("Set a comma-delimited list of band filter names to use "
                                  "in the {}.".format(self.text_name))
        label2.setWordWrap(True)

        filters_la = QtWidgets.QLabel("{} Filters:".format(self.title_name))
        self.filters_le = QtWidgets.QLineEdit()
        filters_la.setBuddy(self.filters_le)

        label3 = QtWidgets.QLabel("Set a comma-delimited list of the number of visits for "
                                  "each band filter in the {}.".format(self.text_name))
        label3.setWordWrap(True)

        visits_per_filter_la = QtWidgets.QLabel("Number of Visits Per Filter:")
        self.visits_per_filter_le = QtWidgets.QLineEdit()
        visits_per_filter_la.setBuddy(self.visits_per_filter_le)

        label4 = QtWidgets.QLabel("Set the number of times the {} should occur over the "
                                  "duration of the survey.".format(self.text_name))
        label4.setWordWrap(True)

        num_events_la = QtWidgets.QLabel("Number of Events:")
        self.num_events_le = QtWidgets.QLineEdit()
        num_events_la.setBuddy(self.num_events_le)
        int_validator = QtGui.QIntValidator()
        int_validator.setBottom(1)
        self.num_events_le.setValidator(int_validator)

        label5 = QtWidgets.QLabel("Set the number of times the {} should be allowed to be "
                                  "missed over the duration of the survey.".format(self.text_name))
        label5.setWordWrap(True)

        num_max_missed_la = QtWidgets.QLabel("Maximum Number of Events:")
        self.num_max_missed_le = QtWidgets.QLineEdit()
        num_max_missed_la.setBuddy(self.num_max_missed_le)
        int_validator2 = QtGui.QIntValidator()
        int_validator2.setBottom(0)
        self.num_max_missed_le.setValidator(int_validator2)

        label_img = QtWidgets.QLabel()
        label_img.setPixmap(QtGui.QPixmap(":/time_domain_window.png"))

        label6 = QtWidgets.QLabel("Set the time interval for subsequent revisits of the same "
                                  "{}.".format(self.text_name))
        label6.setWordWrap(True)

        time_interval_la = QtWidgets.QLabel("Time Interval:")
        self.time_interval_le = QtWidgets.QLineEdit()
        time_interval_la.setBuddy(self.time_interval_le)
        time_interval_un = QtWidgets.QLabel("seconds")

        label7 = QtWidgets.QLabel("Set the relative time where the ranking priority for the {} "
                                  "starts increasing linearly.".format(self.text_name))
        label7.setWordWrap(True)

        time_window_start_la = QtWidgets.QLabel("Time Window Start:")
        self.time_window_start_le = QtWidgets.QLineEdit("0.0")
        time_window_start_la.setBuddy(self.time_window_start_le)
        self.time_window_start_le.setValidator(QtGui.QDoubleValidator())

        label8 = QtWidgets.QLabel("Set the relative time where the ranking priority for the {} "
                                  "reaches maximum.".format(self.text_name))
        label8.setWordWrap(True)

        time_window_max_la = QtWidgets.QLabel("Time Window Max:")
        self.time_window_max_le = QtWidgets.QLineEdit("0.0")
        time_window_max_la.setBuddy(self.time_window_max_le)
        self.time_window_max_le.setValidator(QtGui.QDoubleValidator())

        label9 = QtWidgets.QLabel("Set the relative time where the ranking priority for the {} "
                                  "drops to zero.".format(self.text_name))
        label9.setWordWrap(True)

        time_window_end_la = QtWidgets.QLabel("Time Window End:")
        self.time_window_end_le = QtWidgets.QLineEdit("0.0")
        time_window_end_la.setBuddy(self.time_window_end_le)
        self.time_window_end_le.setValidator(QtGui.QDoubleValidator())

        label10 = QtWidgets.QLabel("Set the weighting value to scale the shape of the time "
                                   "window function.")
        label10.setWordWrap(True)

        time_weight_la = QtWidgets.QLabel("Time Weight:")
        self.time_weight_le = QtWidgets.QLineEdit("1.0")
        time_weight_la.setBuddy(self.time_weight_le)
        self.time_weight_le.setValidator(QtGui.QDoubleValidator())

        add_button = QtWidgets.QPushButton("Add")
        add_button.clicked.connect(self.add_subsequence)
        add_button.setToolTip("Add the {} to the list.".format(self.text_name))
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(self.clear_subsequence)
        clear_button.setToolTip("Clear the last {} from the list.".format(self.text_name))

        gb_layout = QtWidgets.QGridLayout()

        gb_layout.addWidget(label1, 0, 0, 1, 4)
        gb_layout.addWidget(name_la, 1, 0, 1, 2)
        gb_layout.addWidget(self.name_le, 1, 2, 1, 2)
        gb_layout.addWidget(label2, 2, 0, 1, 4)
        gb_layout.addWidget(filters_la, 3, 0, 1, 2)
        gb_layout.addWidget(self.filters_le, 3, 2, 1, 2)
        gb_layout.addWidget(label3, 4, 0, 1, 4)
        gb_layout.addWidget(visits_per_filter_la, 5, 0, 1, 2)
        gb_layout.addWidget(self.visits_per_filter_le, 5, 2, 1, 2)
        gb_layout.addWidget(label4, 6, 0, 1, 4)
        gb_layout.addWidget(num_events_la, 7, 0, 1, 2)
        gb_layout.addWidget(self.num_events_le, 7, 2, 1, 2)
        gb_layout.addWidget(label5, 8, 0, 1, 4)
        gb_layout.addWidget(num_max_missed_la, 9, 0, 1, 2)
        gb_layout.addWidget(self.num_max_missed_le, 9, 2, 1, 2)
        gb_layout.addWidget(label_img, 10, 0, 1, 4)
        gb_layout.addWidget(label6, 11, 0, 1, 4)
        gb_layout.addWidget(time_interval_la, 12, 0, 1, 1)
        gb_layout.addWidget(self.time_interval_le, 12, 1, 1, 2)
        gb_layout.addWidget(time_interval_un, 12, 3, 1, 1)
        gb_layout.addWidget(label7, 13, 0, 1, 4)
        gb_layout.addWidget(time_window_start_la, 14, 0, 1, 2)
        gb_layout.addWidget(self.time_window_start_le, 14, 2, 1, 2)
        gb_layout.addWidget(label8, 15, 0, 1, 4)
        gb_layout.addWidget(time_window_max_la, 16, 0, 1, 2)
        gb_layout.addWidget(self.time_window_max_le, 16, 2, 1, 2)
        gb_layout.addWidget(label9, 17, 0, 1, 4)
        gb_layout.addWidget(time_window_end_la, 18, 0, 1, 2)
        gb_layout.addWidget(self.time_window_end_le, 18, 2, 1, 2)
        gb_layout.addWidget(label10, 19, 0, 1, 4)
        gb_layout.addWidget(time_weight_la, 20, 0, 1, 2)
        gb_layout.addWidget(self.time_weight_le, 20, 2, 1, 2)
        gb_layout.addWidget(add_button, 21, 0, 1, 2)
        gb_layout.addWidget(clear_button, 21, 2, 1, 2)

        group_box.setLayout(gb_layout)

        self.show_subsequences = QtWidgets.QPlainTextEdit()
        self.show_subsequences.setReadOnly(True)

        field_name = "sub_sequences"
        if self.is_nested:
            field_name = "nested_" + field_name + "*"

        self.registerField(field_name, self.show_subsequences, "plainText",
                           self.show_subsequences.textChanged)

        scroll_area_widget = QtWidgets.QWidget()
        scroll_area_widget_layout = QtWidgets.QVBoxLayout()

        scroll_area_widget_layout.addWidget(label)
        scroll_area_widget_layout.addWidget(group_box)
        scroll_area_widget_layout.addWidget(self.show_subsequences)

        scroll_area_widget.setLayout(scroll_area_widget_layout)

        scrollable = QtWidgets.QScrollArea()
        scrollable.setWidgetResizable(True)
        scrollable.setWidget(scroll_area_widget)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(scrollable)
        self.setLayout(main_layout)

    def add_subsequence(self):
        """Combine information for a subsequence.
        """
        current_text = self.show_subsequences.toPlainText()
        subsequence_text = "{},{},{},{},{},{},{},{},{},{}"

        if not self.is_nested:
            name = str(self.name_le.text())
        else:
            name = str(self.name_le.itemText(0))
        if name == '':
            return
        filters = self.format_comma_list(str(self.filters_le.text()))
        visits_per_filter = self.format_comma_list(str(self.visits_per_filter_le.text()))
        num_events = str(self.num_events_le.text())
        num_max_missed = str(self.num_max_missed_le.text())
        time_interval = str(self.time_interval_le.text())
        time_window_start = str(self.time_window_start_le.text())
        time_window_max = str(self.time_window_max_le.text())
        time_window_end = str(self.time_window_end_le.text())
        time_weight = str(self.time_weight_le.text())

        current_text += subsequence_text.format(name, filters, visits_per_filter,
                                                num_events, num_max_missed,
                                                time_interval, time_window_start,
                                                time_window_max, time_window_end,
                                                time_weight) + os.linesep
        self.show_subsequences.setPlainText(current_text)

        if self.is_nested:
            self.name_le.removeItem(0)

    def clear_subsequence(self):
        """Clear the last sub-sequence.
        """
        current_text = str(self.show_subsequences.toPlainText()).strip()
        parts = current_text.split(os.linesep)
        if self.is_nested:
            name = parts[-1].split(',')[0]
            self.name_le.insertItem(0, name)
            self.name_le.setCurrentIndex(0)
        del parts[-1]
        self.show_subsequences.setPlainText(os.linesep.join(parts))

    def format_comma_list(self, istr):
        """Format a comma-delimited list of strings

        This function takes a comma-delimited list as a string: a,b,c,d
        and returns a string looking like: (a b c d).

        Parameters
        ----------
        istr : str
            The string to reformat.

        Returns
        -------
        str
            The reformatted string.
        """
        return "({})".format(" ".join(istr.split(',')))

    def get_sub_sequence_names(self):
        """Get the sub-sequence names from master sub-sequences.

        Returns
        -------
        list[str]
            The set of sub-sequence names given by master sub-sequences.
        """
        master_sub_sequences = str(self.field("master_sub_sequences")).strip().split(os.linesep)
        names = []
        for sub_sequence in master_sub_sequences:
            parts = sub_sequence.split(',')
            name = parts[1].strip('(').strip(')').split(' ')
            names.extend(name)
        return names

    def initializePage(self):
        if self.is_nested:
            sub_sequence_names = self.get_sub_sequence_names()
            self.name_le.addItems(sub_sequence_names)
        else:
            pass

    def nextId(self):
        """Move to next page.
        """
        if not self.is_nested:
            return WizardPages.PageMasterSubSequences
        else:
            return WizardPages.PageSequenceScheduling
