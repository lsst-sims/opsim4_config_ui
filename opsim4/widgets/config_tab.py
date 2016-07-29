import collections

from PyQt4 import QtCore, QtGui

from opsim4.widgets import get_widget_by_type

__all__ = ["ConfigurationTab"]

class ConfigurationTab(QtGui.QWidget):
    """Widget for configuration information.
    """
    CHANGED_PARAMETER = '*'

    checkProperty = QtCore.pyqtSignal('QString', 'QString', list)
    getProperty = QtCore.pyqtSignal('QString', list)
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

        #print("G:", full_name)
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

    def get_changed_parameters(self, layout=None, parent_name=None):
        """Find the changed parameters.

        Parameters
        ----------
        layout : QtGui.QLayout, optional
            An alternative layout to check.
        parent_name : str, optional
            The name of a parent tab.

        Returns
        -------
        list((str, str))
                    A list of 2-tuples of the changed property name and the property value.
        """
        if layout is None:
            layout = self.layout
        changed_values = []
        for i in xrange(layout.rowCount()):
            property_label = layout.itemAtPosition(i, 0).widget()
            property_name = str(property_label.text())
            if property_name.endswith(self.CHANGED_PARAMETER):
                property_widget = layout.itemAtPosition(i, 1).widget()
                try:
                    property_value = str(property_widget.isChecked())
                except AttributeError:
                    property_value = property_widget.text()
                    pname = str(property_widget.objectName())
                    if parent_name is not None:
                        pname = "{}/{}".format(parent_name, pname)
                changed_values.append((pname, property_value))
        return changed_values

    def get_diff(self, layout=None, parent_name=None):
        """Get the changed parameters.

        Parameters
        ----------
        layout : QtGui.QLayout, optional
            An alternative layout to check.
        parent_name : str, optional
            The name of a parent tab.

        Returns
        -------
        dict{str: str}
            The set of changed parameters.
        """
        if layout is None:
            layout = self.layout
        ddict = collections.defaultdict(dict)
        for i in range(layout.rowCount()):
            #property_label = layout.itemAtPosition(i, 0).widget()
            widget = layout.itemAtPosition(i, 0).widget()
            if isinstance(widget, QtGui.QGroupBox):
                gb_name = str(widget.title())
                glayout = widget.layout()
                ddict.update(self.get_diff(layout=glayout, parent_name=gb_name))
            else:
                property_label = widget
                property_name_mod = str(property_label.text())
                if property_name_mod.endswith('*'):
                    property_widget = layout.itemAtPosition(i, 1).widget()
                    property_name = str(property_widget.objectName())
                    #property_name = property_name_mod.strip('*')
                    #print(property_name)
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
                        ddict[self.name + "/" + parent_name][property_name] = [str(property_value)]
                    else:
                        ddict[self.name][property_name] = [str(property_value)]
        return ddict

    def is_changed(self, position, is_changed, layout=None):
        """Mark a parameter widget as changed.

        Parameters
        ----------
        position : int
            The position (usually row) of the widget.
        is_changed : bool
            Flag set to True if the parameter has changed from baseline, false if not.
        layout : QLayout, optional
            An alternative layout to check.
        """
        print("is changed")
        if not is_changed:
            return
        if layout is None:
            layout = self.layout
        plabel = layout.itemAt(position[-1] - 1).widget()
        pname = str(plabel.text())
        changed_label = "{}{}".format(pname, self.CHANGED_PARAMETER)
        plabel.setText(changed_label)
        self.change_label_color(plabel, QtCore.Qt.red)

    def property_changed(self, pwidget, layout=None, qualifier=None, position=None):
        """Get information from a possibly changed parameter.

        Parameters
        ----------
        pwidget : QWidget
            The parameter widget that has possibly changed.
        layout : QLayout, optional
            An alternative layout to check.
        qualifier : str, optional
            A string tp prepend to the parameter name.
        position : int, optional
            A position from another layout. Used when layout is not None.
        """
        location = []
        if layout is None:
            layout = self.layout
        print("HI")
        pos = layout.indexOf(pwidget)
        print("HI2", pos)
        plabel = layout.itemAt(pos - 1).widget()
        print("HI3")
        pname = pwidget.objectName()
        if qualifier is not None:
            pname = "{}/{}".format(qualifier, pname)
        print("HI4")
        if plabel.text().endsWith(self.CHANGED_PARAMETER):
            return
        try:
            pstate = pwidget.checkState()
            if pstate == 0:
                pbool = "False"
            if pstate == 2:
                pbool = "True"
            pvalue = QtCore.QString(pbool)
            print("YYYY:", pvalue)
        except AttributeError:
            pvalue = pwidget.text()

        if position is not None:
            location.append(position)
        location.append(pos)

        self.checkProperty.emit(pname, pvalue, location)
        print("Done")

    def reset_active_field(self, layout=None, qualifier=None, position=None):
        """Reset the active (has focus) parameter widget.
        """
        location = []
        if layout is None:
            layout = self.layout
        for i in xrange(layout.rowCount()):
            property_label = layout.itemAtPosition(i, 0).widget()
            property_name = str(property_label.text())
            if property_name.endswith(self.CHANGED_PARAMETER):
                property_widget = layout.itemAtPosition(i, 1).widget()
                if property_widget.hasFocus():
                    pname = property_widget.objectName()
                    if qualifier is not None:
                        pname = "{}/{}".format(qualifier, pname)
                    if position is not None:
                        location.append(position)
                    location.append(i)
                    self.getProperty.emit(pname, location)

    def reset_active_tab(self):
        """Reset the current tab.
        """
        self.reset_all()

    def reset_all(self, layout=None, qualifier=None, position=None):
        """Reset all of the changed parameters.
        """
        location = []
        if layout is None:
            layout = self.layout
        for i in xrange(layout.rowCount()):
            property_label = layout.itemAtPosition(i, 0).widget()
            property_name = str(property_label.text())
            if property_name.endswith(self.CHANGED_PARAMETER):
                property_widget = layout.itemAtPosition(i, 1).widget()
                pname = property_widget.objectName()
                if qualifier is not None:
                    pname = "{}/{}".format(qualifier, pname)
                if position is not None:
                    location.append(position)
                location.append(i)
                self.getProperty.emit(pname, location)

    def reset_field(self, position, param_value, layout=None):
        """Reset a specific parameter widget.

        Parameters
        ----------
        position : list[int]
            The position (usually row) of the widget to reset.
        param_value : str
            The string representation of the parameter value.
        """
        if layout is None:
            layout = self.layout
        plabel = layout.itemAtPosition(position[-1], 0).widget()
        pname = str(plabel.text())
        plabel.setText(pname.strip(self.CHANGED_PARAMETER))
        pwidget = layout.itemAtPosition(position[-1], 1).widget()
        try:
            print("DD:", param_value)
            pwidget.setChecked(param_value == "True")
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
            widget = self.layout.itemAtPosition(i, 0).widget()
            if isinstance(widget, QtGui.QGroupBox):
                gb_name = str(widget.title())
                glayout = widget.layout()
                changed_values.extend(self.get_changed_parameters(layout=glayout, parent_name=gb_name))
            else:
                property_label = widget
                property_name = str(property_label.text())
                if property_name.endswith(self.CHANGED_PARAMETER):
                    property_widget = self.layout.itemAtPosition(i, 1).widget()
                    try:
                        property_value = str(property_widget.isChecked())
                    except AttributeError:
                        property_value = property_widget.text()
                    changed_values.append((str(property_widget.objectName()),
                                          property_value))

        if len(changed_values):
            #print("R:", self.name)
            self.saveConfiguration.emit(QtCore.QString(save_dir), self.name, changed_values)

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
