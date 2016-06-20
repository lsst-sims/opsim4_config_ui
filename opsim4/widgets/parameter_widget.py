from PyQt4 import QtGui

from opsim4.widgets import get_widget_by_type

class ParameterWidget(QtGui.QWidget):

    def __init__(self, widget_type, parameter_path, parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        self.widget_type = widget_type

        self.layout = QtGui.QHBoxLayout()

        self.parameter_label = QtGui.QLabel(parameter_path)
        self.parameter_widget, self.change_signal = get_widget_by_type(self.widget_type)
        self.parameter_label.setBuddy(self.parameter_widget)
        self.parameter_widget.setObjectName(parameter_path)
        self.parameter_units = QtGui.QLabel()

        self.layout.addWidget(self.parameter_label)
        self.layout.addWidget(self.parameter_widget)
        self.layout.addWidget(self.parameter_units)

    def set_mapping(self, signal_mapper):
        signal = getattr(self.parameter_widget, self.change_signal)
        signal.connect(signal_mapper.map)
        signal_mapper.setMapping(self.parameter_widget, self.parameter_widget)
