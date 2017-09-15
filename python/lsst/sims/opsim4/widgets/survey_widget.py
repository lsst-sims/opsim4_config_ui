from PyQt5 import QtWidgets

from lsst.sims.opsim4.widgets import ConfigurationTab

__all__ = ["SurveyWidget"]

class SurveyWidget(ConfigurationTab):
    """Widget for the survey configuration information.
    """

    def __init__(self, name, proposals, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        proposals : dict
            The default set of proposals.
        parent : QWidget
            The parent widget of this one.
        """
        self.proposals = proposals
        self.GEN_PROP_GB_POS = 3
        self.SEQ_PROP_GB_POS = 4
        self.prop_loc_map = {"general_proposals": self.GEN_PROP_GB_POS,
                             "sequence_proposals": self.SEQ_PROP_GB_POS}
        self.diff_props = []
        ConfigurationTab.__init__(self, name, parent=parent)

    def create_form(self):
        """Create the UI form for the Survey widget.
        """
        self.create_widget("Float", "duration")
        self.create_widget("Str", "start_date")
        self.create_widget("Float", "idle_delay")

        general_group_box = QtWidgets.QGroupBox("general_proposals")
        general_group_box.setObjectName("general_proposals")
        general_group_box.setToolTip("Use the checkboxes to deactivate a general proposal.")
        glayout = QtWidgets.QGridLayout()

        for i, prop_name in enumerate(self.proposals["GEN"]):
            self.create_widget("Bool", prop_name, layout=glayout, rows=i)

        general_group_box.setLayout(glayout)

        self.layout.addWidget(general_group_box, self.GEN_PROP_GB_POS, 0, 1, 3)

        sequence_group_box = QtWidgets.QGroupBox("sequence_proposals")
        sequence_group_box.setObjectName("sequence_proposals")
        sequence_group_box.setToolTip("Use the checkboxes to deactivate a sequence proposal.")
        glayout = QtWidgets.QGridLayout()

        for i, prop_name in enumerate(self.proposals["SEQ"]):
            self.create_widget("Bool", prop_name, layout=glayout, rows=i)

        sequence_group_box.setLayout(glayout)

        self.layout.addWidget(sequence_group_box, self.SEQ_PROP_GB_POS, 0, 1, 3)

    def get_changed_parameters(self, layout=None, parent_name=None):
        """Find the changed parameters.

        Parameters
        ----------
        layout : QLayout, optional
            An alternative layout to check.
        parent_name : str, optional
            The name of a parent tab.

        Returns
        -------
        list((str, str))
            A list of 2-tuples of the changed property name and the property value.
        """
        changed_values = ConfigurationTab.get_changed_parameters(self, layout=layout, parent_name=parent_name)
        props_changed = False
        for changed_value in changed_values:
            if parent_name in changed_value[0]:
                props_changed = True
        corrected_changed_values = []
        if props_changed:
            for changed_value in changed_values:
                if parent_name not in changed_value[0]:
                    corrected_changed_values.append(changed_value)
            prop_gb_loc = self.prop_loc_map[parent_name]
            prop_gb = self.layout.itemAtPosition(prop_gb_loc, 0).widget()
            prop_gb_layout = prop_gb.layout()
            props = []
            for i in range(prop_gb_layout.rowCount()):
                cb = prop_gb_layout.itemAtPosition(i, 1).widget()
                if cb.isChecked():
                    props.append(str(prop_gb_layout.itemAtPosition(i, 0).widget().text()))
            corrected_changed_values.append((parent_name, props))
        else:
            corrected_changed_values = changed_values

        return corrected_changed_values

    def get_diff(self, layout=None, parent_name=None):
        """Get the changed parameters.

        Parameters
        ----------
        layout : QLayout, optional
            An alternative layout to check.
        parent_name : str, optional
            The name of a parent tab.

        Returns
        -------
        dict{str: str}
            The set of changed parameters.
        """
        if layout is None:
            diff = ConfigurationTab.get_diff(self, layout=layout, parent_name=parent_name)
        else:
            self.diff_props.append(parent_name)
            # Parent class calls this function with another layout, so just return the results.
            return ConfigurationTab.get_diff(self, layout=layout, parent_name=parent_name)
        for name in self.diff_props:
            props_changed = False
            for key in diff:
                if name in key:
                    props_changed = True
            if props_changed:
                del diff["survey/{}".format(name)]
                prop_gb_loc = self.prop_loc_map[name]
                prop_gb = self.layout.itemAtPosition(prop_gb_loc, 0).widget()
                prop_gb_layout = prop_gb.layout()
                proposals = []
                for i in range(prop_gb_layout.rowCount()):
                    cb = prop_gb_layout.itemAtPosition(i, 1).widget()
                    if cb.isChecked():
                        proposals.append(str(prop_gb_layout.itemAtPosition(i, 0).widget().text()))
                diff["survey"][name] = [",".join(proposals)]

        self.diff_props = []
        return diff

    def is_changed(self, position, is_changed):
        """Mark a parameter widget as changed.

        Parameters
        ----------
        position : int
            The position (usually row) of the widget.
        is_changed : bool
            Flag set to True if the parameter has changed from baseline, false if not.
        """
        if len(position) > 1:
            group_box = self.layout.itemAtPosition(position[0], 0).widget()
            glayout = group_box.layout()
            ConfigurationTab.is_changed(self, position, is_changed, layout=glayout)
        else:
            ConfigurationTab.is_changed(self, position, is_changed)

    def property_changed(self, pwidget):
        """Get information from a possibly changed parameter.

        Parameters
        ----------
        pwidget : QWidget
            The parameter widget that has possibly changed.
        """
        pos = self.layout.indexOf(pwidget)
        if pos == -1:
            for i in range(3, self.layout.count() - 1):
                group_box = self.layout.itemAtPosition(i, 0).widget()
                glayout = group_box.layout()
                pos = glayout.indexOf(pwidget)
                if pos != -1:
                    qualifier = "{}/{}".format(self.name, group_box.objectName())
                    ConfigurationTab.property_changed(self, pwidget, layout=glayout,
                                                      qualifier=qualifier, position=i)
                    break
        else:
            ConfigurationTab.property_changed(self, pwidget)

    def reset_active_field(self):
        """Reset the active (has focus) parameter widget.
        """
        for i in range(self.layout.rowCount()):
            widget = self.layout.itemAtPosition(i, 0).widget()
            if isinstance(widget, QtWidgets.QGroupBox):
                glayout = widget.layout()
                qualifier = "{}/{}".format(self.name, widget.title())
                ConfigurationTab.reset_active_field(self, layout=glayout, qualifier=qualifier, position=i)
            else:
                property_name = str(widget.text())
                if property_name.endswith(self.CHANGED_PARAMETER):
                    self.getProperty.emit(property_name.strip(self.CHANGED_PARAMETER), [i])

    def reset_all(self):
        """Reset all of the changed parameters.
        """
        for i in range(self.layout.rowCount()):
            widget = self.layout.itemAtPosition(i, 0).widget()
            if isinstance(widget, QtWidgets.QGroupBox):
                glayout = widget.layout()
                qualifier = "{}/{}".format(self.name, widget.title())
                ConfigurationTab.reset_all(self, layout=glayout, qualifier=qualifier, position=i)
            else:
                property_name = str(widget.text())
                if property_name.endswith(self.CHANGED_PARAMETER):
                    self.getProperty.emit(property_name.strip(self.CHANGED_PARAMETER), [i])

    def reset_field(self, position, param_value):
        """Mark a parameter widget as changed.

        Parameters
        ----------
        position : list(int)
            The position (usually row) of the widget.
        param_value : str
            The string representation of the parameter value.
        """
        if len(position) > 1:
            group_box = self.layout.itemAtPosition(position[0], 0).widget()
            glayout = group_box.layout()
            ConfigurationTab.reset_field(self, position, param_value, layout=glayout)
        else:
            ConfigurationTab.reset_field(self, position, param_value)

    def set_information(self, params, full_check=False):
        """Set the information for the configuration.

        Parameters
        ----------
        params : dict
            The configuration information.
        full_check : bool
            Flag to run through all proposals in group boxes.
        """
        for key, value in list(params.items()):
            if "proposals" in key:
                prop_gb = None
                if "general" in key:
                    prop_gb = self.layout.itemAtPosition(self.GEN_PROP_GB_POS, 0).widget()
                if "sequence" in key:
                    prop_gb = self.layout.itemAtPosition(self.SEQ_PROP_GB_POS, 0).widget()
                if not full_check:
                    for proposal in value["value"].split(','):
                        cb = prop_gb.findChild(QtWidgets.QCheckBox, proposal)
                        if cb is not None:
                            cb.setChecked(True)
                else:
                    glayout = prop_gb.layout()
                    proposals = value["value"].split(',')
                    for i in range(glayout.rowCount()):
                        lwidget = glayout.itemAtPosition(i, 0).widget()
                        prop_label = str(lwidget.text())
                        if prop_label not in proposals:
                            cb = glayout.itemAtPosition(i, 1).widget()
                            cb.setChecked(False)
            else:
                ConfigurationTab.set_information(self, key, value, full_check=full_check)
