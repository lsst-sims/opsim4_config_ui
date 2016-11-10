from PyQt5 import QtWidgets

from lsst.sims.opsim4.widgets import get_widget_by_type

class ParameterWidget(QtWidgets.QWidget):

    def __init__(self, widget_type, parameter_path, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.widget_type = widget_type

        self.layout = QtWidgets.QHBoxLayout()

        self.parameter_label = QtWidgets.QLabel(parameter_path)
        self.parameter_widget, self.change_signal = get_widget_by_type(self.widget_type)
        self.parameter_label.setBuddy(self.parameter_widget)
        self.parameter_widget.setObjectName(parameter_path)
        self.parameter_units = QtWidgets.QLabel()

        self.layout.addWidget(self.parameter_label)
        self.layout.addWidget(self.parameter_widget)
        self.layout.addWidget(self.parameter_units)

    def set_mapping(self, signal_mapper):
        signal = getattr(self.parameter_widget, self.change_signal)
        signal.connect(signal_mapper.map)
        signal_mapper.setMapping(self.parameter_widget, self.parameter_widget)
