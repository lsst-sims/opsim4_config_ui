from PyQt5 import QtWidgets

from lsst.sims.opsim4.widgets import ConfigurationTab

__all__ = ["ProposalWidget"]

class ProposalWidget(ConfigurationTab):

    def __init__(self, name, params, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        params : dict
            A set of parameters to help dynamically create the widgets.
        parent : QWidget
            The parent widget of this one.
        """
        self.group_box_rows = []
        self.num_group_boxes = 0
        self.setup = params
        self.full_check = False

        ConfigurationTab.__init__(self, name, self.property_changed, parent)
        del self.setup

    def create_group_box(self, name):
        """Create a group box for configuration information."

        Parameters
        ----------
        name : str
            Label for the group box widget.
        """
        try:
            params = self.setup[name]["value"]
        except TypeError:
            return
        except KeyError:
            # Treating nested sub-sequences differently
            params = self.setup["master_sub_sequences"]["value"]

        self.num_group_boxes += 1
        group_box = QtWidgets.QGroupBox(name)
        grid_layout = QtWidgets.QGridLayout()
        func = getattr(self, "create_{}".format(name))

        func(grid_layout, params)
        group_box.setLayout(grid_layout)
        self.layout.addWidget(group_box, self.rows, 0, 1, 3)
        self.rows += 1

    def create_sky_exclusion(self, glayout, params, is_general=True):
        """Set the information for the proposal sky exclusion.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the sky exclusion.
        """
        self.create_widget("Float", "dec_window", layout=glayout, rows=0)
        num_selections = len(params["selections"]["value"])
        if num_selections:
            num_widgets = 4
            for i in xrange(num_selections):
                j = i * num_widgets
                qualifier = "selections/{}".format(i)
                self.create_widget("Str", "limit_type", qualifier=qualifier, layout=glayout,
                                   rows=(j + 1))
                self.create_widget("Float", "minimum_limit", qualifier=qualifier, layout=glayout,
                                   rows=(j + 2))
                self.create_widget("Float", "maximum_limit", qualifier=qualifier, layout=glayout,
                                   rows=(j + 3))
                self.create_widget("Float", "bounds_limit", qualifier=qualifier, layout=glayout,
                                   rows=(j + 4))
        self.group_box_rows.append(1 + (num_selections * 4))

    def create_sky_nightly_bounds(self, glayout, params):
        """Set the information for the proposal sky nightly bounds.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the sky nightly bounds.
        """
        self.create_widget("Float", "twilight_boundary", layout=glayout, rows=0)
        self.create_widget("Float", "delta_lst", layout=glayout, rows=1)
        self.group_box_rows.append(2)

    def create_sky_constraints(self, glayout, params):
        """Set the information for the proposal sky constraints.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the sky constraints.
        """
        self.create_widget("Float", "max_airmass", layout=glayout, rows=0)
        self.create_widget("Float", "max_cloud", layout=glayout, rows=1)
        self.create_widget("Float", "min_distance_moon", layout=glayout, rows=2)
        self.create_widget("Bool", "exclude_planets", layout=glayout, rows=3)
        self.group_box_rows.append(4)

    def create_scheduling(self, glayout, params, is_general=True):
        """Set the information for the proposal scheduling.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the scheduling.
        is_general : bool, optional
            Flag set to True is general proposal, False for sequence proposal.
        """
        offset = 0
        self.create_widget("Int", "max_num_targets", layout=glayout, rows=0)
        self.create_widget("Bool", "accept_serendipity", layout=glayout, rows=1)
        self.create_widget("Bool", "accept_consecutive_visits", layout=glayout, rows=2)
        if not is_general:
            offset = 3
            self.create_widget("Bool", "restart_lost_sequences", layout=glayout, rows=3)
            self.create_widget("Bool", "restart_complete_sequences", layout=glayout, rows=4)
            self.create_widget("Int", "max_visits_goal", layout=glayout, rows=5)
        self.create_widget("Float", "airmass_bonus", layout=glayout, rows=3 + offset)
        self.create_widget("Float", "hour_angle_bonus", layout=glayout, rows=4 + offset)
        self.create_widget("Float", "hour_angle_max", layout=glayout, rows=5 + offset)
        if is_general:
            self.create_widget("Bool", "restrict_grouped_visits", layout=glayout, rows=6)
            self.create_widget("Float", "time_interval", layout=glayout, rows=7)
            self.create_widget("Float", "time_window_start", layout=glayout, rows=8)
            self.create_widget("Float", "time_window_max", layout=glayout, rows=9)
            self.create_widget("Float", "time_window_end", layout=glayout, rows=10)
            self.create_widget("Float", "time_weight", layout=glayout, rows=11)
            num_widgets = 12
        else:
            num_widgets = 9
        self.group_box_rows.append(num_widgets)

    def create_filters(self, glayout, params, is_general=True):
        """Set the information for the proposal filters.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the filters.
        is_general : bool, optional
            Flag set to True is general proposal, False for sequence proposal.
        """
        num_filters = len(params)
        if num_filters:
            if is_general:
                offset = 2
            else:
                offset = 0
            filter_order = "u g r i z y".split()
            self.filter_index = {v["name"]["value"]: k for k, v in params.items()}
            used_filters = []
            for band_filter in filter_order:
                x = self.filter_index.get(band_filter, None)
                if x is not None:
                    used_filters.append(x)
            for i, x in enumerate(used_filters):
                # Remove name parameter from count
                n = len(params[x]) - 1
                j = n * i
                qualifier = "{}".format(x)
                filter_name = params[x]["name"]["value"]
                if is_general:
                    self.create_widget("Int", "{}_num_visits".format(filter_name), qualifier=qualifier,
                                       layout=glayout, rows=(j + 0))
                    self.create_widget("Int", "{}_num_grouped_visits".format(filter_name),
                                       qualifier=qualifier, layout=glayout, rows=(j + 1))
                self.create_widget("Float", "{}_bright_limit".format(filter_name), qualifier=qualifier,
                                   layout=glayout, rows=(j + offset))
                self.create_widget("Float", "{}_dark_limit".format(filter_name), qualifier=qualifier,
                                   layout=glayout, rows=(j + offset + 1))
                self.create_widget("Float", "{}_max_seeing".format(filter_name), qualifier=qualifier,
                                   layout=glayout, rows=(j + offset + 2))
                self.create_widget("StringList", "{}_exposures".format(filter_name), qualifier=qualifier,
                                   layout=glayout, rows=(j + offset + 3))

        self.group_box_rows.append(num_filters * (offset + 4))

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

    def property_changed(self, pwidget, index):
        """Get information from a possibly changed parameter.

        Parameters
        ----------
        pwidget : QWidget
            The parameter widget that has possibly changed.
        index : int
            The first group box location in the layout.
        """
        pos = self.layout.indexOf(pwidget)
        if pos == -1:
            for i in xrange(index, self.layout.count() - 1):
                group_box = self.layout.itemAtPosition(i, 0).widget()
                glayout = group_box.layout()
                pos = glayout.indexOf(pwidget)
                if pos != -1:
                    qualifier = "{}/{}".format(self.name, group_box.title())
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
            if isinstance(widget, QtWidgets.QGroupBox):
                glayout = widget.layout()
                qualifier = "{}/{}".format(self.name, widget.title())
                ConfigurationTab.reset_active_field(self, layout=glayout, qualifier=qualifier, position=i)
            else:
                property_name = str(widget.text())
                if property_name.endswith(self.CHANGED_PARAMETER):
                    self.getProperty.emit(property_name.strip(self.CHANGED_PARAMETER), [i])

    def reset_active_tab(self):
        """Reset the current tab.
        """
        self.reset_all()

    def reset_all(self, layout=None, qualifier=None, positions=None):
        """Reset all of the changed parameters.
        """
        for i in xrange(self.layout.rowCount()):
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

    def set_sky_exclusion(self, params):
        """Set information in the sky exclusion parameters group box.

        Parameters
        ----------
        params : dict
            The set of parameters for the sky exclusion information.
        """
        group_box = self.layout.itemAtPosition(2, 0).widget()
        glayout = group_box.layout()
        self.set_widget_information(0, glayout, params)
        num_selections = len(params["selections"]["value"])

        if num_selections:
            for v in params["selections"]["value"].values():
                for i in xrange(self.group_box_rows[1] - 1):
                    self.set_widget_information(i + 1, glayout, v)

    def set_sky_nightly_bounds(self, params, gbr_loc):
        """Set information in the sky nightly bounds parameters group box.

        Parameters
        ----------
        params : dict
            The set of parameters for the sky nightly bounds information.
        gbr_loc : int
            The index into the group_box_rows array for the main widget.
        """
        group_box = self.layout.itemAtPosition(3, 0).widget()
        glayout = group_box.layout()
        for i in xrange(self.group_box_rows[gbr_loc]):
            self.set_widget_information(i, glayout, params)

    def set_sky_constraints(self, params, gbr_loc):
        """Set information in the sky constraints group box.

        Parameters
        ----------
        params : dict
            The set of parameters for the sky constraints information.
        gbr_loc : int
            The index into the group_box_rows array for the main widget.
        """
        group_box = self.layout.itemAtPosition(4, 0).widget()
        glayout = group_box.layout()
        for i in xrange(self.group_box_rows[gbr_loc]):
            self.set_widget_information(i, glayout, params)

    def set_scheduling(self, params, gb_loc, gbr_loc):
        """Set information in the scheduling parameters group box.

        Parameters
        ----------
        params : dict
            The set of parameters for the scheduling information.
        gb_loc : int
            The index into the main layout for the main widget.
        gbr_loc : int
            The index into the group_box_rows array for the main widget.
        """
        group_box = self.layout.itemAtPosition(gb_loc, 0).widget()
        glayout = group_box.layout()
        for i in xrange(self.group_box_rows[gbr_loc]):
            self.set_widget_information(i, glayout, params)

    def set_filters(self, params, gb_loc, gbr_loc):
        """Set information in the filters parameters group box.

        Parameters
        ----------
        params : dict
            The set of parameters for the filters information.
        gb_loc : int
            The index into the main layout for the main widget.
        gbr_loc : int
            The index into the group_box_rows array for the main widget.
        """
        group_box = self.layout.itemAtPosition(gb_loc, 0).widget()
        glayout = group_box.layout()
        num_filters = len(params)
        if num_filters:
            for i in xrange(self.group_box_rows[gbr_loc]):
                self.set_widget_information(i, glayout, params,
                                            alt_indexer=self.filter_index)

    def set_unit_labels(self, widget, params):
        """Set the unit labels if necessary.

        Parameters
        ----------
        widget : QtWidgets.QLabel
            The label for the units.
        params : dict
            The instance containing the unit information.
        """
        value = str(params["units"])
        if value != "None":
            widget.setText(value)

    def set_widget_information(self, position, ilayout, params,
                               alt_indexer=None):
        """Set the information for a given widget.

        Parameters
        ----------
        position : int
            Row location of the widget in the layout.
        ilayout : QLayout
            The layout where the widget is.
        params : dict
            The set of parameters to get the information from.
        alt_indexer : dict, optional
            A dictionary containing a different set of rules to find a
            parameter.
        """
        label = ilayout.itemAtPosition(position, 0).widget()
        label_text = str(label.text())
        widget = ilayout.itemAtPosition(position, 1).widget()
        if alt_indexer is None:
            param = params[label_text]
        else:
            leading_label = label_text.split('_')[0]
            data_label = "_".join(label_text.split('_')[1:])
            index = alt_indexer[leading_label]
            param = params[index][data_label]
        value = param["value"]
        try:
            widget.setChecked(value)
        except AttributeError:
            widget.setText(str(value))
            if self.full_check:
                widget.editingFinished.emit()
        widget.setToolTip(param["doc"])
        units = ilayout.itemAtPosition(position, 2).widget()
        self.set_unit_labels(units, param)
