import collections
import os
import re
from PyQt4 import QtCore, QtGui

import lsst.pex.config.listField

from utilities import load_class

class ConfigurationTab(QtGui.QWidget):
    def __init__(self, tab_name, config_obj, parent=None):
        super(QtGui.QWidget, self).__init__(parent)

        self.tab_name = tab_name
        self.config_obj = config_obj
        self.config_cls = load_class(self.config_obj)
        self.paren_match = re.compile(r'\(([^\)]+)\)')

        self.layout = QtGui.QGridLayout()
        self.signal_mapper = QtCore.QSignalMapper(self)
        self.signal_mapper.mapped[QtGui.QWidget].connect(self.check_property)

        self.create_form()
        temp_widget = QtGui.QWidget()
        temp_widget.setLayout(self.layout)
        self.scrollable = QtGui.QScrollArea()
        self.scrollable.setWidget(temp_widget)

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.addWidget(self.scrollable)
        self.setLayout(main_layout)

    def create_form(self):
        for i, (k, v) in enumerate(sorted(self.config_cls.__dict__["_fields"].items())):
            tcls = None
            name_label = QtGui.QLabel(k)

            if v.dtype == float:
                tcls = "Float"
            if v.dtype == bool:
                tcls = "Bool"
            if v.dtype == str:
                tcls = "Str"
            if isinstance(v, lsst.pex.config.listField.ListField):
                if v.dtype == float:
                    tcls = "DoubleList"
                else:
                    tcls = "StringList"
            if tcls is None:
                print("Cannot handle {}".format(k))

            if tcls is not None:
                self.layout.addWidget(name_label, i, 0)
                pwidget = self.make_property_widget(tcls, v)
                name_label.setBuddy(pwidget)
                self.signal_mapper.setMapping(pwidget, pwidget)
                self.layout.addWidget(pwidget, i, 1)
                unit_label = QtGui.QLabel(self.make_unit_label(v))
                self.layout.addWidget(unit_label, i, 2)

    def make_property_widget(self, tcls, v):
        widget = QtGui.QWidget()
        if tcls == "Str":
            widget = QtGui.QLineEdit(self.get_dict_value(v.name))
            regex_val = self.make_regex(v.doc)
            if regex_val is not None:
                widget.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(regex_val)))
            widget.editingFinished.connect(self.signal_mapper.map)
        if tcls == "Float":
            widget = QtGui.QLineEdit(str(self.get_dict_value(v.name)))
            widget.setValidator(QtGui.QDoubleValidator())
            widget.editingFinished.connect(self.signal_mapper.map)
        if tcls == "Bool":
            widget = QtGui.QCheckBox()
            widget.setChecked(self.get_dict_value(v.name))
            widget.stateChanged.connect(self.signal_mapper.map)
        if tcls.endswith("List"):
            widget = QtGui.QLineEdit(",".join([str(x) for x in self.get_dict_value(v.name)]))
            widget.editingFinished.connect(self.signal_mapper.map)

        widget.setToolTip(v.doc)
        return widget

    def make_unit_label(self, v):
        units = ""
        for match in self.paren_match.findall(v.doc):
            if match.startswith("units"):
                units = match.split('=')[-1]

        return units

    def make_regex(self, doc):
        regex = None
        for match in self.paren_match.findall(doc):
            if match.startswith("format"):
                value = match.split('=')[-1]
                if value == 'YYYY-MM-DD':
                    regex = r'\d{4}-\d{2}-\d{2}'
        return regex

    def get_dict_value(self, name):
        return self.config_obj.toDict()[name]

    def check_property(self, pwidget):
        pos = self.layout.indexOf(pwidget)
        plabel = self.layout.itemAt(pos - 1).widget()
        pname = str(plabel.text())
        if pname.endswith('*'):
            return

        try:
            v1 = bool(pwidget.checkState())
        except AttributeError:
            try:
                text = pwidget.text()
                if "," in text:
                    v1 = [float(v)for v in text.split(',')]
                else:
                    v1 = float(text)
            except ValueError:
                text = pwidget.text()
                if "," in text:
                    v1 = [str(v)for v in text.split(',')]
                else:
                    v1 = text
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
                property_format = "config.{}={}"
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

    def reset_all(self):
        for i in range(self.layout.rowCount()):
            property_label = self.layout.itemAtPosition(i, 0).widget()
            property_name_mod = str(property_label.text())
            if property_name_mod.endswith('*'):
                property_name = property_name_mod.strip('*')
                property_widget = self.layout.itemAtPosition(i, 1).widget()
                self._reset_field(property_name, property_label, property_widget)

    def reset_active_tab(self):
        self.reset_all()

    def reset_active_field(self):
        for i in range(self.layout.rowCount()):
            property_label = self.layout.itemAtPosition(i, 0).widget()
            property_name_mod = str(property_label.text())
            property_widget = self.layout.itemAtPosition(i, 1).widget()
            if property_name_mod.endswith('*'):
                property_widget = self.layout.itemAtPosition(i, 1).widget()
                if property_widget.hasFocus():
                    property_name = property_name_mod.strip('*')
                    self._reset_field(property_name, property_label, property_widget)

    def _reset_field(self, pn, pl, pw):
        pl.setText(pn)
        self.change_label_color(pl, QtCore.Qt.black)
        try:
            pw.setChecked(self.get_dict_value(pn))
        except AttributeError:
            value = self.get_dict_value(pn)
            if isinstance(value, list):
                pw.setText(",".join([str(x) for x in value]))
            else:
                pw.setText(str(value))

    def get_diff(self, parent_name=None):
        #print("B:", self.tab_name)
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

                default_value = self.get_dict_value(property_name)
                if isinstance(default_value, list):
                    default_value = ",".join([str(x) for x in default_value])
                else:
                    default_value = str(default_value)

                if parent_name is not None:
                    ddict[parent_name + "/" + self.tab_name][property_name] = [default_value,
                                                                               str(property_value)]
                else:
                    ddict[self.tab_name][property_name] = [default_value, str(property_value)]
        return ddict
