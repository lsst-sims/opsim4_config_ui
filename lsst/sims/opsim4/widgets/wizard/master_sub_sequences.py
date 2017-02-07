import os

from PyQt5 import QtGui, QtWidgets

from lsst.sims.opsim4.widgets.wizard import WizardPages

__all__ = ["MasterSubSequencesPage"]

class MasterSubSequencesPage(QtWidgets.QWizardPage):
    """Main class for setting the proposal's master sub-sequences.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.setTitle("Master Sub-sequence Specifications")

        self.name_list = []

        label = QtWidgets.QLabel("Set the parameters for a master sub-sequence in the form provided.")
        label.setWordWrap(True)

        group_box = QtWidgets.QGroupBox("Master Sub-sequence")

        label1 = QtWidgets.QLabel("Set the identifier for the master sub-sequence.")
        label1.setWordWrap(True)

        name_la = QtWidgets.QLabel("Master Sub-sequence Name:")
        self.name_le = QtWidgets.QLineEdit()
        name_la.setBuddy(self.name_le)

        label2 = QtWidgets.QLabel("Set a comma-delimited list for the identifier(s) for the master "
                                  "sub-sequence nested sub-sequence(s). NOTE: The names MUST be unique")
        label2.setWordWrap(True)

        sub_sequence_name_la = QtWidgets.QLabel("Nested Sub-sequence Name(s):")
        self.sub_sequence_names_le = QtWidgets.QLineEdit()
        sub_sequence_name_la.setBuddy(self.sub_sequence_names_le)

        label4 = QtWidgets.QLabel("Set the number of times the master sub-sequence should occur over the "
                                  "duration of the survey.")
        label4.setWordWrap(True)

        num_events_la = QtWidgets.QLabel("Number of Events:")
        self.num_events_le = QtWidgets.QLineEdit()
        num_events_la.setBuddy(self.num_events_le)
        int_validator = QtGui.QIntValidator()
        int_validator.setBottom(1)
        self.num_events_le.setValidator(int_validator)

        label5 = QtWidgets.QLabel("Set the number of times the master sub-sequence should be allowed to be "
                                  "missed over the duration of the survey.")
        label5.setWordWrap(True)

        num_max_missed_la = QtWidgets.QLabel("Maximum Number of Events:")
        self.num_max_missed_le = QtWidgets.QLineEdit()
        num_max_missed_la.setBuddy(self.num_max_missed_le)
        int_validator2 = QtGui.QIntValidator()
        int_validator2.setBottom(0)
        self.num_max_missed_le.setValidator(int_validator2)

        label_img = QtWidgets.QLabel()
        label_img.setPixmap(QtGui.QPixmap(":/time_domain_window.png"))

        label6 = QtWidgets.QLabel("Set the time interval for subsequent revisits of the same master "
                                  "sub-sequence.")
        label6.setWordWrap(True)

        time_interval_la = QtWidgets.QLabel("Time Interval:")
        self.time_interval_le = QtWidgets.QLineEdit()
        time_interval_la.setBuddy(self.time_interval_le)
        #self.time_interval_le.setValidator(QtGui.QDoubleValidator())
        time_interval_un = QtWidgets.QLabel("seconds")

        label7 = QtWidgets.QLabel("Set the relative time where the ranking priority for the master "
                                  "sub-sequence starts increasing linearly.")
        label7.setWordWrap(True)

        time_window_start_la = QtWidgets.QLabel("Time Window Start:")
        self.time_window_start_le = QtWidgets.QLineEdit("0.0")
        time_window_start_la.setBuddy(self.time_window_start_le)
        self.time_window_start_le.setValidator(QtGui.QDoubleValidator())

        label8 = QtWidgets.QLabel("Set the relative time where the ranking priority for the master "
                                  "sub-sequence reaches maximum.")
        label8.setWordWrap(True)

        time_window_max_la = QtWidgets.QLabel("Time Window Max:")
        self.time_window_max_le = QtWidgets.QLineEdit("0.0")
        time_window_max_la.setBuddy(self.time_window_max_le)
        self.time_window_max_le.setValidator(QtGui.QDoubleValidator())

        label9 = QtWidgets.QLabel("Set the relative time where the ranking priority for the master "
                                  "sub-sequence drops to zero.")
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
        add_button.setToolTip("Add the sub-sequence to the list.")
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(self.clear_subsequence)
        clear_button.setToolTip("Clear the last sub-sequence from the list.")

        gb_layout = QtWidgets.QGridLayout()

        gb_layout.addWidget(label1, 0, 0, 1, 4)
        gb_layout.addWidget(name_la, 1, 0, 1, 2)
        gb_layout.addWidget(self.name_le, 1, 2, 1, 2)
        gb_layout.addWidget(label2, 2, 0, 1, 4)
        gb_layout.addWidget(sub_sequence_name_la, 3, 0, 1, 2)
        gb_layout.addWidget(self.sub_sequence_names_le, 3, 2, 1, 2)
        gb_layout.addWidget(label4, 4, 0, 1, 4)
        gb_layout.addWidget(num_events_la, 5, 0, 1, 2)
        gb_layout.addWidget(self.num_events_le, 5, 2, 1, 2)
        gb_layout.addWidget(label5, 6, 0, 1, 4)
        gb_layout.addWidget(num_max_missed_la, 7, 0, 1, 2)
        gb_layout.addWidget(self.num_max_missed_le, 7, 2, 1, 2)
        gb_layout.addWidget(label_img, 8, 0, 1, 4)
        gb_layout.addWidget(label6, 9, 0, 1, 4)
        gb_layout.addWidget(time_interval_la, 10, 0, 1, 1)
        gb_layout.addWidget(self.time_interval_le, 10, 1, 1, 2)
        gb_layout.addWidget(time_interval_un, 10, 3, 1, 1)
        gb_layout.addWidget(label7, 11, 0, 1, 4)
        gb_layout.addWidget(time_window_start_la, 12, 0, 1, 2)
        gb_layout.addWidget(self.time_window_start_le, 12, 2, 1, 2)
        gb_layout.addWidget(label8, 13, 0, 1, 4)
        gb_layout.addWidget(time_window_max_la, 14, 0, 1, 2)
        gb_layout.addWidget(self.time_window_max_le, 14, 2, 1, 2)
        gb_layout.addWidget(label9, 15, 0, 1, 4)
        gb_layout.addWidget(time_window_end_la, 16, 0, 1, 2)
        gb_layout.addWidget(self.time_window_end_le, 16, 2, 1, 2)
        gb_layout.addWidget(label10, 17, 0, 1, 4)
        gb_layout.addWidget(time_weight_la, 18, 0, 1, 2)
        gb_layout.addWidget(self.time_weight_le, 18, 2, 1, 2)
        gb_layout.addWidget(add_button, 19, 0, 1, 2)
        gb_layout.addWidget(clear_button, 19, 2, 1, 2)

        group_box.setLayout(gb_layout)

        self.show_subsequences = QtWidgets.QPlainTextEdit()
        self.show_subsequences.setReadOnly(True)
        self.registerField("master_sub_sequences", self.show_subsequences, "plainText",
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
        """Combine information for a master subsequence.
        """
        current_text = self.show_subsequences.toPlainText()
        subsequence_text = "{},{},{},{},{},{},{},{},{}"

        name = str(self.name_le.text())
        self.name_list.append(name)
        sub_sequence_names = self.format_comma_list(str(self.sub_sequence_names_le.text()))
        num_events = str(self.num_events_le.text())
        num_max_missed = str(self.num_max_missed_le.text())
        time_interval = str(self.time_interval_le.text())
        time_window_start = str(self.time_window_start_le.text())
        time_window_max = str(self.time_window_max_le.text())
        time_window_end = str(self.time_window_end_le.text())
        time_weight = str(self.time_weight_le.text())

        current_text += subsequence_text.format(name, sub_sequence_names,
                                                num_events, num_max_missed,
                                                time_interval, time_window_start,
                                                time_window_max, time_window_end,
                                                time_weight) + os.linesep
        self.show_subsequences.setPlainText(current_text)

    def clear_subsequence(self):
        """Clear the last sub-sequence.
        """
        current_text = str(self.show_subsequences.toPlainText()).strip()
        parts = current_text.split(os.linesep)
        del parts[-1]
        del self.name_list[-1]
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

    def nextId(self):
        """Move to next page.
        """
        if len(self.name_list):
            return WizardPages.PageNestedSubSequences
        else:
            return WizardPages.PageSequenceScheduling
