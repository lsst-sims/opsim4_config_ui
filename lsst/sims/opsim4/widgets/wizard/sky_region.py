import os

from PyQt5 import QtGui, QtWidgets

from lsst.sims.ocs.configuration.proposal import SELECTION_LIMIT_TYPES

__all__ = ["SkyRegionPage"]

class SkyRegionPage(QtWidgets.QWizardPage):
    """Main class for setting the proposal's sky region.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.setTitle("Sky Region Selection")

        label = QtWidgets.QLabel("Select the region of sky for the proposals. There can be "
                                 "more than one selection, but one selection MUST be made.")
        label.setWordWrap(True)

        self.selection_text = []

        group_box = QtWidgets.QGroupBox("Select Regions")

        self.selection_types = QtWidgets.QComboBox()
        self.selection_types.editable = False
        for selection in SELECTION_LIMIT_TYPES:
            self.selection_types.addItem(selection)
        self.selection_types.activated.connect(self.check_bounds_limit)

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
        self.bounds_limit_le.setReadOnly(True)
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
        add_button.setToolTip("Add the selection to the list.")
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(self.clear_selection)
        clear_button.setToolTip("Clear the last selection from the list.")

        gb_layout.addWidget(add_button, 4, 0, 1, 2)
        gb_layout.addWidget(clear_button, 4, 2, 1, 2)

        group_box.setLayout(gb_layout)

        self.show_selections = QtWidgets.QPlainTextEdit()
        self.show_selections.setReadOnly(True)
        self.registerField("sky_region_selections*", self.show_selections, "plainText",
                           self.show_selections.textChanged)

        comb_label = QtWidgets.QLabel("If more than one selection is made, a logical operator "
                                      "must be designated below. Multiple operators should be in "
                                      "a comma-delimited list. The number of operators should always be "
                                      "one less than the number of selections.")
        comb_label.setWordWrap(True)

        combiners_le = QtWidgets.QLineEdit()
        self.registerField("sky_region_combiners", combiners_le)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(group_box)
        layout.addWidget(self.show_selections)
        layout.addWidget(comb_label)
        layout.addWidget(combiners_le)

        scroll_area_widget = QtWidgets.QWidget()
        scroll_area_widget_layout = QtWidgets.QVBoxLayout()
        scroll_area_widget_layout.addWidget(label)
        scroll_area_widget_layout.addWidget(group_box)
        scroll_area_widget_layout.addWidget(self.show_selections)
        scroll_area_widget_layout.addWidget(comb_label)
        scroll_area_widget_layout.addWidget(combiners_le)
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
        selection_text = "{},{},{}".format(str(self.selection_types.currentText()),
                                           str(self.min_limit_le.text()),
                                           str(self.max_limit_le.text()))
        if not self.bounds_limit_le.isReadOnly():
            selection_text += str(self.bounds_limit_le.text())

        current_text += selection_text + os.linesep
        self.show_selections.setPlainText(current_text)

    def check_bounds_limit(self, selection):
        """Check to see if bounds limit can be editable.

        This function checks the selection type being made and if it is
        a GP selection, then the bounds_limit line edit becomes editable.

        Parameters
        ----------
        selection : str
            The seleciton type from the QComboBox
        """
        self.bounds_limit_le.setReadOnly(str(selection) == "GP")

    def clear_selection(self):
        """Clear the last selection.
        """
        current_text = str(self.show_selections.toPlainText())
        parts = current_text.split(os.linesep)
        del parts[-1]
        self.show_selections.setPlainText(os.linesep.join(parts))
