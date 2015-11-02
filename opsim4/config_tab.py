import os
from PyQt4 import QtCore, QtGui

import lsst.pex.config.listField

from utilities import load_class

class ConfigurationTab(QtGui.QWidget):
    def __init__(self, tab_name, config_obj, parent=None):
        super(QtGui.QWidget, self).__init__(parent)

        self.tab_name = tab_name
        self.config_obj = config_obj
        self.config_cls = load_class(self.config_obj)

        self.layout = QtGui.QGridLayout()
        self.signal_mapper = QtCore.QSignalMapper(self)
        self.signal_mapper.mapped[QtGui.QWidget].connect(self.check_property)

        self.create_form()
        self.setLayout(self.layout)

    @property
    def title(self):
        values = self.tab_name.split('_')
        for i, value in enumerate(values):
            if value == "lsst":
                values[i] = value.upper()
            else:
                values[i] = value.capitalize()
        return " ".join(values)

    def create_form(self):
        for i, (k, v) in enumerate(self.config_cls.__dict__["_fields"].items()):
            tcls = None
            name_label = QtGui.QLabel(k)

            if v.dtype == float:
                tcls = "Float"
            if v.dtype == bool:
                tcls = "Bool"
            if v.dtype == str:
                tcls = "Str"
            if isinstance(v, lsst.pex.config.listField.ListField):
                tcls = "List"
            if tcls is None:
                print("Cannot handle {}".format(k))

            if tcls is not None:
                self.layout.addWidget(name_label, i, 0)
                pwidget = self.make_property_widget(tcls, v)
                name_label.setBuddy(pwidget)
                pwidget.editingFinished.connect(self.signal_mapper.map)
                self.signal_mapper.setMapping(pwidget, pwidget)
                self.layout.addWidget(pwidget, i, 1)
                unit_label = QtGui.QLabel("")
                self.layout.addWidget(unit_label, i, 2)

    def make_property_widget(self, tcls, v):
        widget = QtGui.QWidget()
        if tcls == "Str":
            widget = QtGui.QLineEdit(self.get_dict_value(v.name))
        if tcls == "Float":
            widget = QtGui.QLineEdit(str(self.get_dict_value(v.name)))
            widget.setValidator(QtGui.QDoubleValidator())

        widget.setToolTip(v.doc)
        return widget

    def get_dict_value(self, name):
        return self.config_obj.toDict()[name]

    def check_property(self, pwidget):
        pos = self.layout.indexOf(pwidget)
        plabel = self.layout.itemAt(pos - 1).widget()
        pname = str(plabel.text())

        try:
            v1 = float(pwidget.text())
        except ValueError:
            v1 = pwidget.text()
        v2 = self.get_dict_value(pname)
        #print("{}, {}".format(v1, type(v1)))
        #print("{}, {}".format(v2, type(v2)))
        if v1 != v2:
            #print("{} finished editing.".format(pname))
            changed_label = "{}*".format(pname)
            plabel.setText(changed_label)
            self.change_label_color(plabel, QtCore.Qt.red)

    def change_label_color(self, label, color):
        palette = label.palette()
        palette.setColor(label.foregroundRole(), color)
        label.setPalette(palette)

    def save(self, save_dir):
        changed_values = []
        for i in range(self.layout.rowCount()):
            property_label = self.layout.itemAtPosition(i, 0).widget()
            property_name_mod = str(property_label.text())
            if property_name_mod.endswith('*'):
                property_name = property_name_mod.strip('*')
                property_widget = self.layout.itemAtPosition(i, 1).widget()
                try:
                    property_value = float(property_widget.text())
                    property_format = "config.{}={}"
                except ValueError:
                    property_value = str(property_widget.text())
                    property_format = "config.{}=\'{}\'"

                changed_values.append(property_format.format(property_name, property_value))
                changed_values.append(os.linesep)

        if len(changed_values) != 0:
            filename = self.tab_name + ".py"
            with open(os.path.join(save_dir, filename), 'w') as ofile:
                ofile.write("import {}".format(self.config_cls.__module__))
                ofile.write(os.linesep)
                ofile.write("assert type(config)=={0}.{1}, \'config is of type %s.%s instead of {0}.{1}\' % "
                            "(type(config).__module__, type(config).__name__)"
                            "".format(self.config_cls.__module__, self.config_cls.__name__))
                ofile.write(os.linesep)
                for line in changed_values:
                    ofile.write(line)
