from PyQt4 import QtCore, QtGui

from opsim4.widgets import get_widget_by_type

__all__ = ["ConfigurationTab"]

class ConfigurationTab(QtGui.QWidget):
    """Widget for configuration information.
    """

    def __init__(self, name, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        """
        super(ConfigurationTab, self).__init__(parent)

        self.name = name
        self.layout = QtGui.QGridLayout()
        self.layout.setSizeConstraint
        self.signal_mapper = QtCore.QSignalMapper(self)
        self.signal_mapper.mapped[QtGui.QWidget].connect(self.check_property)
        self.rows = 0

        self.create_form()

        temp_widget = QtGui.QWidget()
        temp_widget.setLayout(self.layout)
        self.scrollable = QtGui.QScrollArea()
        self.scrollable.setWidget(temp_widget)

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.addWidget(self.scrollable)
        self.setLayout(main_layout)

    def create_widget(self, wtype, name):
        parameter_label = QtGui.QLabel(name)
        parameter_widget, change_signal = get_widget_by_type(wtype)
        parameter_label.setBuddy(parameter_widget)
        parameter_widget.setObjectName(name)
        parameter_units = QtGui.QLabel()

        signal = getattr(parameter_widget, change_signal)
        signal.connect(self.signal_mapper.map)
        self.signal_mapper.setMapping(parameter_widget, parameter_widget)

        self.layout.addWidget(parameter_label, self.rows, 0)
        self.layout.addWidget(parameter_widget, self.rows, 1)
        self.layout.addWidget(parameter_units, self.rows, 2)

        self.rows += 1

    def create_form(self):
        raise NotImplementedError("Classes must override this!")

    def set_information(self, key, info):
        for i in xrange(self.layout.rowCount()):
            widget = self.layout.itemAtPosition(i, 1).widget()
            if str(widget.objectName()) == key:
                value = info["value"]
                try:
                    widget.setText(str(value))
                except AttributeError:
                    widget.setChecked(value)
                widget.setToolTip(info["doc"])
                if info["format"] is not None:
                    widget.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(info["format"])))
                if info["units"] is not None:
                    unit_widget = self.layout.itemAtPosition(i, 2).widget()
                    unit_widget.setText(info["units"])

    def check_property(self, pwidget):
        pass
