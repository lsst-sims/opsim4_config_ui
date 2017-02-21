import os

from PyQt5 import QtCore, QtGui, QtWidgets

from lsst.sims.opsim4.widgets.wizard import WizardPages

__all__ = ["SkyExclusionPage"]

class SkyExclusionPage(QtWidgets.QWizardPage):
    """Main class for setting the proposal's sky exclusion.
    """

    def __init__(self, parent=None, is_general=True):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.setTitle("Sky Exclusion Selection")
        self.is_general = is_general
        if self.is_general:
            self.param_id = "general"
        else:
            self.param_id = "sequence"

        dec_win_gb = QtWidgets.QGroupBox()

        dec_win_note_label = QtWidgets.QLabel("The declination window is used to handle moving the "
                                              "observation site from current LSST location.")
        dec_win_note_label.setWordWrap(True)

        dec_win_label = QtWidgets.QLabel("Dec Window:")
        dec_win_le = QtWidgets.QLineEdit("90.0")
        dec_win_label.setBuddy(dec_win_le)
        dec_win_units = QtWidgets.QLabel("degrees")

        dwgb_layout = QtWidgets.QGridLayout()
        dwgb_layout.addWidget(dec_win_label, 0, 0)
        dwgb_layout.addWidget(dec_win_le, 0, 1, 1, 2)
        dwgb_layout.addWidget(dec_win_units, 0, 3)

        dec_win_gb.setLayout(dwgb_layout)

        self.registerField("{}_sky_exclusions_dec_window".format(self.param_id),
                           dec_win_le)

        if self.is_general:
            exclusion_label = QtWidgets.QLabel("A galactic plane exclusion zone is available by "
                                               "filling out the form below.")
            exclusion_label.setWordWrap(True)

            label_img = QtWidgets.QLabel()
            label_img.setPixmap(QtGui.QPixmap(":/galactic_plane_envelope.png"))
            label_img.setAlignment(QtCore.Qt.AlignHCenter)

            self.selection_text = []

            group_box = QtWidgets.QGroupBox("Add Exclusion")

            self.selection_types = QtWidgets.QComboBox()
            self.selection_types.editable = False
            self.selection_types.addItem("GP")

            degrees_units1 = QtWidgets.QLabel("degrees")
            degrees_units2 = QtWidgets.QLabel("degrees")
            degrees_units3 = QtWidgets.QLabel("degrees")
            validator = QtGui.QDoubleValidator()

            min_limit_la = QtWidgets.QLabel("Min Limit:")
            self.min_limit_le = QtWidgets.QLineEdit()
            self.min_limit_le.setValidator(validator)
            min_limit_la.setBuddy(self.min_limit_le)

            max_limit_la = QtWidgets.QLabel("Max Limit:")
            self.max_limit_le = QtWidgets.QLineEdit()
            self.max_limit_le.setValidator(validator)
            max_limit_la.setBuddy(self.max_limit_le)

            bounds_limit_la = QtWidgets.QLabel("Bounds Limit:")
            self.bounds_limit_le = QtWidgets.QLineEdit("")
            self.bounds_limit_le.setValidator(validator)
            bounds_limit_la.setBuddy(self.bounds_limit_le)

            gb_layout = QtWidgets.QGridLayout()
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

            add_button = QtWidgets.QPushButton("Add")
            add_button.clicked.connect(self.add_selection)
            add_button.setToolTip("Add the exclusion to the list.")
            clear_button = QtWidgets.QPushButton("Clear")
            clear_button.clicked.connect(self.clear_selection)
            clear_button.setToolTip("Clear the exclusion from the list.")

            gb_layout.addWidget(add_button, 4, 0, 1, 2)
            gb_layout.addWidget(clear_button, 4, 2, 1, 2)

            group_box.setLayout(gb_layout)

            self.show_selections = QtWidgets.QPlainTextEdit()
            self.show_selections.setReadOnly(True)
            self.registerField("sky_exclusion_selections", self.show_selections, "plainText",
                               self.show_selections.textChanged)

        scroll_area_widget = QtWidgets.QWidget()
        scroll_area_widget_layout = QtWidgets.QVBoxLayout()

        scroll_area_widget_layout.addWidget(dec_win_note_label)
        scroll_area_widget_layout.addWidget(dec_win_gb)
        if self.is_general:
            scroll_area_widget_layout.addWidget(exclusion_label)
            scroll_area_widget_layout.addWidget(label_img)
            scroll_area_widget_layout.addWidget(group_box)
            scroll_area_widget_layout.addWidget(self.show_selections)
        scroll_area_widget_layout.addStretch(1)
        scroll_area_widget.setLayout(scroll_area_widget_layout)

        scrollable = QtWidgets.QScrollArea()
        scrollable.setWidgetResizable(True)
        scrollable.setWidget(scroll_area_widget)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(scrollable)
        self.setLayout(main_layout)

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

    def nextId(self):
        """Move to next page.
        """
        return WizardPages.PageSkyNightlyBounds
