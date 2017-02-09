from lsst.sims.opsim4.widgets import ProposalWidget

__all__ = ["SequenceProposalWidget"]

class SequenceProposalWidget(ProposalWidget):

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
        ProposalWidget.__init__(self, name, params, parent)

    def create_form(self):
        """Create the form for the proposal widget.
        """
        self.create_widget("Str", "name")
        self.layout.itemAtPosition(0, 1).widget().setReadOnly(True)
        self.create_widget("IntList", "sky_user_regions", qualifier=self.name)
        self.create_group_box("sky_exclusion")
        self.create_group_box("sky_nightly_bounds")
        self.create_group_box("sky_constraints")
        self.create_group_box("sub_sequences")
        self.create_group_box("master_sub_sequences")
        self.create_group_box("scheduling")
        self.create_group_box("filters")
        self.hide_unused()

    def create_sky_exclusion(self, glayout, params):
        """Set the information for the proposal sky exclusion.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the sky exclusion.
        """
        ProposalWidget.create_sky_exclusion(self, glayout, params)

    def create_sky_nightly_bounds(self, glayout, params):
        """Set the information for the proposal sky nightly bounds.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the sky nightly bounds.
        """
        ProposalWidget.create_sky_nightly_bounds(self, glayout, params)

    def create_sky_constraints(self, glayout, params):
        """Set the information for the proposal sky constraints.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the sky constraints.
        """
        ProposalWidget.create_sky_constraints(self, glayout, params)

    def create_sub_sequences(self, glayout, params):
        """Set the sub-sequence information for the proposal.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the sub-sequence information.
        """
        num_sub_sequences = len(params)
        if num_sub_sequences:
            num_widgets = 10
            for i in xrange(num_sub_sequences):
                j = i * num_widgets
                qualifier = "{}".format(i)
                self.create_widget("Str", "name", qualifier=qualifier, layout=glayout,
                                   rows=(j + 0))
                self.create_widget("StringList", "filters", qualifier=qualifier, layout=glayout,
                                   rows=(j + 1))
                self.create_widget("IntList", "visits_per_filter", qualifier=qualifier, layout=glayout,
                                   rows=(j + 2))
                self.create_widget("Int", "num_events", qualifier=qualifier, layout=glayout,
                                   rows=(j + 3))
                self.create_widget("Int", "num_max_missed", qualifier=qualifier, layout=glayout,
                                   rows=(j + 4))
                self.create_widget("Float", "time_interval", qualifier=qualifier, layout=glayout,
                                   rows=(j + 5))
                self.create_widget("Float", "time_window_start", qualifier=qualifier, layout=glayout,
                                   rows=(j + 6))
                self.create_widget("Float", "time_window_max", qualifier=qualifier, layout=glayout,
                                   rows=(j + 7))
                self.create_widget("Float", "time_window_end", qualifier=qualifier, layout=glayout,
                                   rows=(j + 8))
                self.create_widget("Float", "time_weight", qualifier=qualifier, layout=glayout,
                                   rows=(j + 9))
            self.group_box_rows.append(num_sub_sequences * num_widgets)
        else:
            self.group_box_rows.append(0)

    def create_master_sub_sequences(self, glayout, params):
        """Set the nested sub-sequences information for the proposal.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the nested sub-sequences information.
        """
        num_master_sub_sequences = len(params)
        if num_master_sub_sequences:
            self.group_box_rows.append(num_master_sub_sequences)
        else:
            self.group_box_rows.append(0)

    def create_scheduling(self, glayout, params):
        """Set the information for the proposal scheduling.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the scheduling.
        """
        ProposalWidget.create_scheduling(self, glayout, params, is_general=False)

    def create_filters(self, glayout, params):
        """Set the information for the proposal filters.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the filters.
        """
        ProposalWidget.create_filters(self, glayout, params, is_general=False)

    def hide_unused(self):
        """Hide sub-sequece ot master sub-sequence group box if none present.
        """
        for i in xrange(2, self.layout.count() - 1):
            try:
                group_box = self.layout.itemAtPosition(i, 0).widget()
            except AttributeError:
                # Somehow have extra unexplained widgets in main layout.
                continue
            if group_box.title() == "master_sub_sequences":
                if not self.group_box_rows[4]:
                    group_box.hide()
            if group_box.title() == "sub_sequences":
                if not self.group_box_rows[3]:
                    group_box.hide()

    def property_changed(self, pwidget):
        """Get information from a possibly changed parameter.

        Parameters
        ----------
        pwidget : QWidget
            The parameter widget that has possibly changed.
        """
        ProposalWidget.property_changed(self, pwidget, 2)

    def set_information(self, params):
        """Set the information for the configuration.

        Parameters
        ----------
        params : dict
            The configuration information.
        """
        name_widget = self.layout.itemAtPosition(0, 1).widget()
        name_widget.setText(str(params["name"]["value"]))
        name_widget.setToolTip(str(params["name"]["doc"]))
        sky_user_regions = self.layout.itemAtPosition(1, 1).widget()
        sky_user_regions.setText(str(params["sky_user_regions"]["value"]))
        sky_user_regions.setToolTip(str(params["sky_user_regions"]["doc"]))
        self.set_sky_exclusion(params["sky_exclusion"]["value"])
        self.set_sky_nightly_bounds(params["sky_nightly_bounds"]["value"], 1)
        self.set_sky_constraints(params["sky_constraints"]["value"], 2)
        self.set_sub_sequences(params["sub_sequences"]["value"])
        self.set_scheduling(params["scheduling"]["value"], 7, 5)
        self.set_filters(params["filters"]["value"], 8, 6)

    def set_sub_sequences(self, params):
        """Set information in the sub-sequences parameters group box.

        Parameters
        ----------
        params : dict
            The set of parameters for the sub-sequences information.
        """
        group_box = self.layout.itemAtPosition(5, 0).widget()
        glayout = group_box.layout()
        num_sub_sequences = len(params)
        if num_sub_sequences:
            num_widgets = self.group_box_rows[3] / num_sub_sequences
            for j, v in enumerate(params.values()):
                for i in xrange(num_widgets):
                    k = j * num_widgets + i
                    self.set_widget_information(k, glayout, v)
