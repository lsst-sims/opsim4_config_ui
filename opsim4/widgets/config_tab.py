import collections

from PyQt4 import QtCore, QtGui

from opsim4.widgets import get_widget_by_type

__all__ = ["ConfigurationTab"]

class ConfigurationTab(QtGui.QWidget):
    """Widget for configuration information.
    """
    CHANGED_PARAMETER = '*'

    checkProperty = QtCore.pyqtSignal('QString', 'QString', int)
    getProperty = QtCore.pyqtSignal('QString', int)
    saveConfiguration = QtCore.pyqtSignal('QString', 'QString', list)

    def __init__(self, name, mapping=None, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        parent : QWidget
            The parent widget of this one.
        """
        QtGui.QWidget.__init__(self, parent)

        self.name = name
        self.layout = QtGui.QGridLayout()
        self.layout.setSizeConstraint
        self.signal_mapper = QtCore.QSignalMapper(self)
        if mapping is not None:
            func = mapping
        else:
            func = self.property_changed
        self.signal_mapper.mapped[QtGui.QWidget].connect(func)
        self.rows = 0

        self.create_form()

        temp_widget = QtGui.QWidget()
        temp_widget.setLayout(self.layout)
        self.scrollable = QtGui.QScrollArea()
        self.scrollable.setWidget(temp_widget)

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.addWidget(self.scrollable)
        self.setLayout(main_layout)

    def create_widget(self, wtype, name, qualifier=None, layout=None, rows=None, mapping=None):
        """Create a parameter widget.

        Parameters
        ----------
        wtype : str
            The representation string for the parameter type.
        name : str
            The name of the parameter.
        qualifier : str, optional
            A prefix to the name for setting to the object name.
        layout : QtGui.QGridLayout, optional
            An alternate layout instance.
        rows : int, optional
            An alternate value for rows in a layout
        """
        parameter_label = QtGui.QLabel(name)
        parameter_widget, change_signal = get_widget_by_type(wtype)
        parameter_label.setBuddy(parameter_widget)
        if qualifier is not None:
            full_name = "{}/{}".format(qualifier, name)
        else:
            full_name = name
        parameter_widget.setObjectName(full_name)
        parameter_units = QtGui.QLabel()

        print("G:", full_name)
        signal = getattr(parameter_widget, change_signal)
        signal.connect(self.signal_mapper.map)
        self.signal_mapper.setMapping(parameter_widget, parameter_widget)

        if layout is None:
            layout = self.layout

        if rows is None:
            current_row = self.rows
        else:
            current_row = rows

        layout.addWidget(parameter_label, current_row, 0)
        layout.addWidget(parameter_widget, current_row, 1)
        layout.addWidget(parameter_units, current_row, 2)

        if rows is None:
            self.rows += 1
        else:
            rows += 1

        return rows

    def create_form(self, params=None):
        """Create UI form.
        """
        raise NotImplementedError("Classes must override this!")

    def get_diff(self, parent_name=None):
        """Get the changed parameters.

        Parameters
        ----------
        parent_name : str, optional
            The name of a parent tab.

        Returns
        -------
        dict{str: str}
            The set of changed parameters.
        """
        ddict = collections.defaultdict(dict)
        for i in range(self.layout.rowCount()):
            property_label = self.layout.itemAtPosition(i, 0).widget()
            property_name_mod = str(property_label.text())
            if property_name_mod.endswith('*'):
                property_name = property_name_mod.strip('*')
                #print(property_name)
                property_widget = self.layout.itemAtPosition(i, 1).widget()
                try:
                    property_value = str(property_widget.isChecked())
                except AttributeError:
                    try:
                        property_text = property_widget.text()
                        if "," in property_text:
                            values = property_text.split(',')
                            try:
                                property_value = str([float(x) for x in values])
                            except ValueError:
                                property_value = str([str(x) for x in values])
                        else:
                            property_value = float(property_text)
                    except ValueError:
                        property_value = str(property_widget.text())

                if parent_name is not None:
                    ddict[parent_name + "/" + self.name][property_name] = [str(property_value)]
                else:
                    ddict[self.name][property_name] = [str(property_value)]
        return ddict

    def set_information(self, key, info):
        """Set information in a particular parameter widget.

        Parameters
        ----------
        key : str
            The name of the parameter.
        info : dict
            The set of information that describes this parameter.
        """
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

    def property_changed(self, pwidget):
        """Get information from a possibly changed parameter.

        Parameters
        ----------
        pwidget : QWidget
            The parameter widget that has possibly changed.
        """
        print("HI")
        pos = self.layout.indexOf(pwidget)
        print("HI2", pos)
        plabel = self.layout.itemAt(pos - 1).widget()
        print("HI3")
        pname = plabel.text()
        print("HI4")
        if pname.endsWith(self.CHANGED_PARAMETER):
            return
        try:
            pvalue = QtCore.QString(pwidget.checkState())
        except AttributeError:
            pvalue = pwidget.text()

        self.checkProperty.emit(pname, pvalue, pos)
        print("Done")

    @QtCore.pyqtSlot(int, bool)
    def is_changed(self, position, is_changed):
        """Mark a parameter widget as changed.

        Parameters
        ----------
        position : int
            The position (usually row) of the widget.
        is_changed : bool
            Flag set to True if the parameter has changed from baseline, false if not.
        """
        print("is changed")
        if not is_changed:
            return
        plabel = self.layout.itemAt(position - 1).widget()
        pname = str(plabel.text())
        changed_label = "{}{}".format(pname, self.CHANGED_PARAMETER)
        plabel.setText(changed_label)
        self.change_label_color(plabel, QtCore.Qt.red)

    def change_label_color(self, label, color):
        """Change a label's text color.

        Parameters
        ----------
        label : QLabel
            The label that needs text color change.
        color : QColor
            The color for the text change.
        """
        palette = label.palette()
        palette.setColor(label.foregroundRole(), color)
        label.setPalette(palette)

    def reset_active_field(self):
        """Reset the active (has focus) parameter widget.
        """
        for i in xrange(self.layout.rowCount()):
            property_label = self.layout.itemAtPosition(i, 0).widget()
            property_name = str(property_label.text())
            if property_name.endswith(self.CHANGED_PARAMETER):
                property_widget = self.layout.itemAtPosition(i, 1).widget()
                if property_widget.hasFocus():
                    self.getProperty.emit(property_name.strip(self.CHANGED_PARAMETER), i)

    def reset_active_tab(self):
        """Reset the current tab.
        """
        self.reset_all()

    def reset_all(self):
        """Reset all of the changed parameters.
        """
        for i in xrange(self.layout.rowCount()):
            property_label = self.layout.itemAtPosition(i, 0).widget()
            property_name = str(property_label.text())
            if property_name.endswith(self.CHANGED_PARAMETER):
                self.getProperty.emit(property_name.strip(self.CHANGED_PARAMETER), i)

    @QtCore.pyqtSlot(int, str)
    def reset_field(self, position, param_value):
        """Reset a specific parameter widget.

        Parameters
        ----------
        position : int
            The position (usually row) of the widget to reset.
        param_value : str
            The string representation of the parameter value.
        """
        plabel = self.layout.itemAtPosition(position, 0).widget()
        pname = str(plabel.text())
        plabel.setText(pname.strip(self.CHANGED_PARAMETER))
        pwidget = self.layout.itemAtPosition(position, 1).widget()
        try:
            pwidget.setChecked(bool(param_value))
        except AttributeError:
            pwidget.setText(param_value)
        self.change_label_color(plabel, QtCore.Qt.black)

    def save(self, save_dir):
        """Get the changed parameters for saving.

        Parameters
        ----------
        save_dir : str
            The directory for saving the configuration in.
        """
        changed_values = []
        for i in xrange(self.layout.rowCount()):
            property_label = self.layout.itemAtPosition(i, 0).widget()
            property_name = str(property_label.text())
            if property_name.endswith(self.CHANGED_PARAMETER):
                property_widget = self.layout.itemAtPosition(i, 1).widget()
                try:
                    property_value = str(property_widget.isChecked())
                except AttributeError:
                    property_value = property_widget.text()
                changed_values.append((property_name.strip(self.CHANGED_PARAMETER),
                                      property_value))

        if len(changed_values):
            self.saveConfiguration.emit(QtCore.QString(save_dir), self.name, changed_values)

