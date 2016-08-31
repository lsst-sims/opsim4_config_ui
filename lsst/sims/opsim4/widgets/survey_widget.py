from PyQt4 import QtGui

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
        ConfigurationTab.__init__(self, name, parent=parent)

    def create_form(self):
        """Create the UI form for the Survey widget.
        """
        self.create_widget("Float", "duration")
        self.create_widget("Str", "start_date")
        self.create_widget("Float", "idle_delay")

        ad_group_box = QtGui.QGroupBox("ad_proposals")
        ad_group_box.setObjectName("ad_proposals")
        ad_group_box.setToolTip("Use the checkboxes to select which area distribution proposals NOT to run.")
        glayout = QtGui.QGridLayout()

        for i, prop_name in enumerate(self.proposals["AD"]):
            self.create_widget("Bool", prop_name, layout=glayout, rows=i)

        ad_group_box.setLayout(glayout)

        self.layout.addWidget(ad_group_box, 3, 0, 1, 3)

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
        ad_props_changed = False
        for changed_value in changed_values:
            if "ad_proposals" in changed_value[0]:
                ad_props_changed = True
        corrected_changed_values = []
        if ad_props_changed:
            for changed_value in changed_values:
                if "ad_proposals" not in changed_value[0]:
                    corrected_changed_values.append(changed_value)
            ad_prop_gb = self.layout.itemAtPosition(3, 0).widget()
            ad_prop_gb_layout = ad_prop_gb.layout()
            ad_proposals = []
            for i in xrange(ad_prop_gb_layout.rowCount()):
                cb = ad_prop_gb_layout.itemAtPosition(i, 1).widget()
                if not cb.isChecked():
                    ad_proposals.append(str(ad_prop_gb_layout.itemAtPosition(i, 0).widget().text()))
            corrected_changed_values.append(("ad_proposals", ad_proposals))
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
            # Parent class calls this function with another layout, so just return the results.
            return ConfigurationTab.get_diff(self, layout=layout, parent_name=parent_name)
        ad_props_changed = False
        for key in diff:
            if "ad_proposals" in key:
                ad_props_changed = True
        if ad_props_changed:
            del diff["survey/ad_proposals"]
            ad_prop_gb = self.layout.itemAtPosition(3, 0).widget()
            ad_prop_gb_layout = ad_prop_gb.layout()
            ad_proposals = []
            for i in xrange(ad_prop_gb_layout.rowCount()):
                cb = ad_prop_gb_layout.itemAtPosition(i, 1).widget()
                if not cb.isChecked():
                    ad_proposals.append(str(ad_prop_gb_layout.itemAtPosition(i, 0).widget().text()))
            diff["survey"]["ad_proposals"] = [",".join(ad_proposals)]

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
            for i in xrange(3, self.layout.count() - 1):
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
        for i in xrange(self.layout.rowCount()):
            widget = self.layout.itemAtPosition(i, 0).widget()
            if isinstance(widget, QtGui.QGroupBox):
                glayout = widget.layout()
                qualifier = "{}/{}".format(self.name, widget.title())
                ConfigurationTab.reset_active_field(self, layout=glayout, qualifier=qualifier, position=i)
            else:
                property_name = str(widget.text())
                if property_name.endswith(self.CHANGED_PARAMETER):
                    self.getProperty.emit(property_name.strip(self.CHANGED_PARAMETER), i)

    def reset_all(self):
        """Reset all of the changed parameters.
        """
        for i in xrange(self.layout.rowCount()):
            widget = self.layout.itemAtPosition(i, 0).widget()
            if isinstance(widget, QtGui.QGroupBox):
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
