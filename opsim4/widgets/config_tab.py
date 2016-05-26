import collections
import os

from PyQt4 import QtCore, QtGui
from opsim4.constants import CSS_GROUPBOX

class ConfigurationTab(QtGui.QWidget):
    def __init__(self, tab_name, config_dict, parent=None):
        super(QtGui.QWidget, self).__init__(parent)

        self.tab_name = tab_name
        self.config_dict = config_dict

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

    def create_form(self, cdict=None, layout=None, progress=0):
        i = 0
        #print("F:", i, progress)
        widget_layout = self.layout if layout is None else layout
        conf_dict = self.config_dict if cdict is None else cdict

        for k, v in sorted(conf_dict.items()):
            name_label = QtGui.QLabel(k)

            if v["dtype"] != "GroupBox":
                #print("Z:", k, i, i + progress)
                widget_layout.addWidget(name_label, i + progress, 0)
                pwidget = self.make_property_widget(v)
                name_label.setBuddy(pwidget)
                self.signal_mapper.setMapping(pwidget, pwidget)
                widget_layout.addWidget(pwidget, i + progress, 1)
                unit_label = QtGui.QLabel("" if v["units"] is None else v["units"])
                widget_layout.addWidget(unit_label, i + progress, 2)
            else:
                #print("ZZ:", k, i, i + progress)
                group_box = QtGui.QGroupBox(k)
                group_box.setStyleSheet(CSS_GROUPBOX)
                grid_layout = QtGui.QGridLayout()
                #print("A:", v["value"], type(v["value"]))
                if isinstance(v["value"], collections.defaultdict):
                    self.create_form(v["value"], grid_layout)
                else:
                    prg2 = 0
                    for value in v["value"].values():
                        prg2 += self.create_form(value, grid_layout, i + progress + prg2)
                        #print("B:", i, prg2)
                group_box.setLayout(grid_layout)
                widget_layout.addWidget(group_box, i + progress, 0, 1, 3)
                print(self.signal_mapper)

            i += 1
        #print("G:", i, progress)
        return i

    def make_property_widget(self, v):
        widget = QtGui.QWidget()
        tcls = v["dtype"]
        if tcls == "Str":
            widget = QtGui.QLineEdit(v["value"])
            regex_val = v["format"]
            if regex_val is not None:
                widget.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(regex_val)))
            widget.editingFinished.connect(self.signal_mapper.map)
        if tcls == "Float":
            widget = QtGui.QLineEdit(str(v["value"]))
            widget.setValidator(QtGui.QDoubleValidator())
            widget.editingFinished.connect(self.signal_mapper.map)
        if tcls == "Int":
            widget = QtGui.QLineEdit(str(v["value"]))
            widget.setValidator(QtGui.QIntValidator())
            widget.editingFinished.connect(self.signal_mapper.map)
        if tcls == "Bool":
            widget = QtGui.QCheckBox()
            widget.setChecked(v["value"])
            widget.stateChanged.connect(self.signal_mapper.map)
        if tcls.endswith("List"):
            widget = QtGui.QLineEdit(v["value"])
            widget.editingFinished.connect(self.signal_mapper.map)

        widget.setToolTip(v["doc"])
        return widget

    def get_dict_value(self, name):
        return self.config_dict[name]["value"]

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
