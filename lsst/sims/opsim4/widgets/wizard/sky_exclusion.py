import os

from PyQt4 import QtGui

__all__ = ["SkyExclusionPage"]

class SkyExclusionPage(QtGui.QWizardPage):
    """Main class for setting the proposal's sky exclusion.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtGui.QWizardPage.__init__(self, parent)
        self.setTitle("Sky Exclusion Selection")

        dec_win_gb = QtGui.QGroupBox()

        dec_win_note_label = QtGui.QLabel("The declination window is used to handle moving the observation "
                                          "site from current LSST location.")
        dec_win_note_label.setWordWrap(True)

        dec_win_label = QtGui.QLabel("Dec Window:")
        dec_win_le = QtGui.QLineEdit("90.0")
        dec_win_label.setBuddy(dec_win_le)
        dec_win_units = QtGui.QLabel("degrees")

        dwgb_layout = QtGui.QGridLayout()
        dwgb_layout.addWidget(dec_win_label, 0, 0)
        dwgb_layout.addWidget(dec_win_le, 0, 1, 1, 2)
        dwgb_layout.addWidget(dec_win_units, 0, 3)

        dec_win_gb.setLayout(dwgb_layout)

        self.registerField("sky_exclusions_dec_window", dec_win_le)

        exclusion_label = QtGui.QLabel("A galactic plane exclusion zone is available by filling out the "
                                       "form below.")
        exclusion_label.setWordWrap(True)

        self.selection_text = []

        group_box = QtGui.QGroupBox("Add Exclusion")

        self.selection_types = QtGui.QComboBox()
        self.selection_types.editable = False
        self.selection_types.addItem("GP")

        degrees_units1 = QtGui.QLabel("degrees")
        degrees_units2 = QtGui.QLabel("degrees")
        degrees_units3 = QtGui.QLabel("degrees")
        validator = QtGui.QDoubleValidator()

        min_limit_la = QtGui.QLabel("Min Limit:")
        self.min_limit_le = QtGui.QLineEdit()
        self.min_limit_le.setValidator(validator)
        min_limit_la.setBuddy(self.min_limit_le)

        max_limit_la = QtGui.QLabel("Max Limit:")
        self.max_limit_le = QtGui.QLineEdit()
        self.max_limit_le.setValidator(validator)
        max_limit_la.setBuddy(self.max_limit_le)

        bounds_limit_la = QtGui.QLabel("Bounds Limit:")
        self.bounds_limit_le = QtGui.QLineEdit("")
        self.bounds_limit_le.setValidator(validator)
        bounds_limit_la.setBuddy(self.bounds_limit_le)

        gb_layout = QtGui.QGridLayout()
        gb_layout.addWidget(self.selection_types, 0, 0, 1, 4)

        gb_layout.addWidget(min_limit_la, 1, 0)
        gb_layout.addWidget(self.min_limit_le, 1, 1, 1, 2)
        gb_layout.addWidget(degrees_units1, 1, 3)

        gb_layout.addWidget(max_limit_la, 2, 0)
        gb_layout.addWidget(self.max_limit_le, 2, 1, 1, 2)
        gb_layout.addWidget(degrees_units2, 2, 3)

        gb_layout.addWidget(bounds_limit_la, 3, 0)
        gb_layout.addWidget(self.bounds_limit_le, 3, 1, 1, 2)
        gb_layout.addWidget(degrees_units3, 3, 3)

        add_button = QtGui.QPushButton("Add")
        add_button.clicked.connect(self.add_selection)
        add_button.setToolTip("Add the exclusion to the list.")
        clear_button = QtGui.QPushButton("Clear")
        clear_button.clicked.connect(self.clear_selection)
        clear_button.setToolTip("Clear the exclusion from the list.")

        gb_layout.addWidget(add_button, 4, 0, 1, 2)
        gb_layout.addWidget(clear_button, 4, 2, 1, 2)

        group_box.setLayout(gb_layout)

        self.show_selections = QtGui.QPlainTextEdit()
        self.show_selections.setReadOnly(True)
        self.registerField("sky_exclusion_selections", self.show_selections, "plainText",
                           self.show_selections.textChanged)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(dec_win_note_label)
        layout.addWidget(dec_win_gb)
        layout.addWidget(exclusion_label)
        layout.addWidget(group_box)
        layout.addWidget(self.show_selections)

        self.setLayout(layout)

    def add_selection(self):
        """Combine information for a sky region selection.
        """
        current_text = self.show_selections.toPlainText()
        selection_text = "{},{},{},{}".format(str(self.selection_types.currentText()),
                                              str(self.min_limit_le.text()),
                                              str(self.max_limit_le.text()),
                                              str(self.bounds_limit_le.text()))

        current_text += selection_text + os.linesep
        self.show_selections.setPlainText(current_text)

    def clear_selection(self):
        """Clear the last selection.
        """
        current_text = str(self.show_selections.toPlainText())
        parts = current_text.split(os.linesep)
        del parts[-1]
        self.show_selections.setPlainText(os.linesep.join(parts))
