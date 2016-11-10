from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = ["BandFiltersPage"]

class BandFiltersPage(QtWidgets.QWizardPage):
    """Main class for setting the proposal's band filters information.
    """

    def __init__(self, parent=None):
        """Initialize the class

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizardPage.__init__(self, parent)
        self.setTitle("Band Filters Setup")

        label = QtWidgets.QLabel("Set the band filter information. At least one filter must be specified "
                                 "otherwise the proposal will not gather any observations. When setting "
                                 "the exposures, a comma-delimited list of times is required.")
        label.setWordWrap(True)

        self.u_band = self.create_band_filter_information("u")
        self.g_band = self.create_band_filter_information("g")
        self.r_band = self.create_band_filter_information("r")
        self.i_band = self.create_band_filter_information("i")
        self.z_band = self.create_band_filter_information("z")
        self.y_band = self.create_band_filter_information("y")

        scroll_area_widget = QtWidgets.QWidget()
        scroll_area_widget_layout = QtWidgets.QVBoxLayout()
        scroll_area_widget_layout.addWidget(label)
        scroll_area_widget_layout.addWidget(self.u_band)
        scroll_area_widget_layout.addWidget(self.g_band)
        scroll_area_widget_layout.addWidget(self.r_band)
        scroll_area_widget_layout.addWidget(self.i_band)
        scroll_area_widget_layout.addWidget(self.z_band)
        scroll_area_widget_layout.addWidget(self.y_band)
        scroll_area_widget_layout.addStretch(10)
        scroll_area_widget.setLayout(scroll_area_widget_layout)

        scrollable = QtWidgets.QScrollArea()
        scrollable.setWidgetResizable(True)
        scrollable.setWidget(scroll_area_widget)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(scrollable)
        self.setLayout(main_layout)

        self.setField("band_filters_testing", QtCore.QVariant())

    def create_band_filter_information(self, band_filter):
        """Create the band filter information group box.

        Parameters
        ----------
        band_filter : str
            The short name for the band filter.
        """
        group_box = QtWidgets.QGroupBox(band_filter + " Band Filter")
        group_box.setCheckable(True)
        group_box.setChecked(False)
        self.registerField("{}_filter_use".format(band_filter), group_box, "checked", group_box.clicked)

        glayout = QtWidgets.QGridLayout()

        num_visits_la = QtWidgets.QLabel("Number of Visits:")
        num_visits_le = QtWidgets.QLineEdit()
        num_visits_la.setBuddy(num_visits_le)
        int_validator = QtGui.QIntValidator()
        int_validator.setBottom(1)
        num_visits_le.setValidator(int_validator)
        self.registerField("{}_filter_num_visits".format(band_filter), num_visits_le)

        bright_limit_la = QtWidgets.QLabel("Bright Limit:")
        bright_limit_le = QtWidgets.QLineEdit()
        bright_limit_la.setBuddy(bright_limit_le)
        dbl_validator1 = QtGui.QDoubleValidator()
        bright_limit_le.setValidator(dbl_validator1)
        self.registerField("{}_filter_bright_limit".format(band_filter), bright_limit_le)

        dark_limit_la = QtWidgets.QLabel("Dark Limit:")
        dark_limit_le = QtWidgets.QLineEdit()
        dark_limit_la.setBuddy(dark_limit_le)
        dbl_validator2 = QtGui.QDoubleValidator()
        dark_limit_le.setValidator(dbl_validator2)
        self.registerField("{}_filter_dark_limit".format(band_filter), dark_limit_le)

        max_seeing_la = QtWidgets.QLabel("Maximum Seeing:")
        max_seeing_le = QtWidgets.QLineEdit()
        max_seeing_la.setBuddy(max_seeing_le)
        dbl_validator3 = QtGui.QDoubleValidator()
        max_seeing_le.setValidator(dbl_validator3)
        self.registerField("{}_filter_max_seeing".format(band_filter), max_seeing_le)

        exposures_la = QtWidgets.QLabel("Exposures:")
        exposures_le = QtWidgets.QLineEdit()
        exposures_la.setBuddy(exposures_le)
        exposures_un = QtWidgets.QLabel("seconds")
        self.registerField("{}_filter_exposures".format(band_filter), exposures_le)

        glayout.addWidget(num_visits_la, 0, 0)
        glayout.addWidget(num_visits_le, 0, 1)
        glayout.addWidget(bright_limit_la, 1, 0)
        glayout.addWidget(bright_limit_le, 1, 1)
        glayout.addWidget(dark_limit_la, 2, 0)
        glayout.addWidget(dark_limit_le, 2, 1)
        glayout.addWidget(max_seeing_la, 3, 0)
        glayout.addWidget(max_seeing_le, 3, 1)
        glayout.addWidget(exposures_la, 4, 0)
        glayout.addWidget(exposures_le, 4, 1)
        glayout.addWidget(exposures_un, 4, 2)

        group_box.setLayout(glayout)
        return group_box
