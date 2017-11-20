from builtins import zip

from lsst.sims.opsim4.widgets import ProposalWidget

__all__ = ["GeneralProposalWidget"]

class GeneralProposalWidget(ProposalWidget):

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
        self.create_group_box("sky_region")
        self.create_group_box("sky_exclusion")
        self.create_group_box("sky_nightly_bounds")
        self.create_group_box("sky_constraints")
        self.create_group_box("scheduling")
        self.create_group_box("filters")
        self.create_group_box("group_limit")
        

    def create_sky_region(self, glayout, params):
        """Set the information for the proposal sky region.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the sky region.
        """
        num_selections = len(params["selections"]["value"])
        if params["time_ranges"]["value"] is not None:
            num_time_ranges = len(params["time_ranges"]["value"])
        else:
            num_time_ranges = 0
        if params["selection_mapping"]["value"] is not None:
            num_mappings = len(params["selection_mapping"]["value"])
        else:
            num_mappings = 0
        use_time_ranges = False
        use_mappings = False
        if num_selections:
            num_widgets = 4
            if num_time_ranges:
                num_widgets += 2
                use_time_ranges = True
            if num_mappings:
                num_widgets += 1
                use_mappings = True
            for i in range(num_selections):
                j = i * num_widgets
                qualifier = "selections/{}".format(i)
                self.create_widget("Str", "limit_type", qualifier=qualifier, layout=glayout,
                                   rows=(j + 0))
                self.create_widget("Float", "minimum_limit", qualifier=qualifier, layout=glayout,
                                   rows=(j + 1))
                self.create_widget("Float", "maximum_limit", qualifier=qualifier, layout=glayout,
                                   rows=(j + 2))
                self.create_widget("Float", "bounds_limit", qualifier=qualifier, layout=glayout,
                                   rows=(j + 3))
                if use_time_ranges:
                    qualifier = "time_ranges/{}".format(i)
                    self.create_widget("Int", "start", qualifier=qualifier, layout=glayout,
                                       rows=(j + 4))
                    self.create_widget("Int", "end", qualifier=qualifier, layout=glayout,
                                       rows=(j + 5))
                if use_mappings:
                    qualifier = "selection_mapping/{}".format(i)
                    self.create_widget("IntList", "indexes", qualifier=qualifier, layout=glayout,
                                       rows=(j + 6))
            self.group_box_rows.append(num_selections * num_widgets)

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

    def create_scheduling(self, glayout, params):
        """Set the information for the proposal scheduling.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the scheduling.
        """
        ProposalWidget.create_scheduling(self, glayout, params)

    def create_filters(self, glayout, params):
        """Set the information for the proposal filters.

        Parameters
        ----------
        glayout : QGridLayout
            Instance of a grid layout.
        params : dict
            The configuration information for the filters.
        """
        ProposalWidget.create_filters(self, glayout, params)

    def property_changed(self, pwidget):
        """Get information from a possibly changed parameter.

        Parameters
        ----------
        pwidget : QWidget
            The parameter widget that has possibly changed.
        """
        ProposalWidget.property_changed(self, pwidget, 1)

    def set_information(self, params, full_check=False):
        """Set the information for the configuration.

        Parameters
        ----------
        params : dict
            The configuration information.
        full_check : bool
            Flag to trigger signals for property changes.
        """
        self.full_check = full_check
        name_widget = self.layout.itemAtPosition(0, 1).widget()
        name_widget.setText(str(params["name"]["value"]))
        name_widget.setToolTip(str(params["name"]["doc"]))
        self.set_sky_region(params["sky_region"]["value"])

        print(params)
        print("\n")
        print(params["sky_region"]["value"])
        print("\n")

        self.set_sky_exclusion(params["sky_exclusion"]["value"])
        
        print(params["sky_exclusion"]["value"])
        print("\n")

        self.set_sky_nightly_bounds(params["sky_nightly_bounds"]["value"], 2)
        self.set_sky_constraints(params["sky_constraints"]["value"], 3)
        self.set_scheduling(params["scheduling"]["value"], 5, 4)
        self.set_filters(params["filters"]["value"], 6, 5)


        print(params["group_limit"]["value"])
        print("\n")
        self.set_group_limit(params["group_limit"]["value"], 6)


    def set_sky_region(self, params):
        """Set information in the sky region parameters group box.

        Parameters
        ----------
        params : dict
            The set of parameters for the sky region information.
        """

        group_box = self.layout.itemAtPosition(1, 0).widget()
        glayout = group_box.layout()
        num_selections = len(params["selections"]["value"])
        if num_selections:
            num_widgets = self.group_box_rows[0] / num_selections
            if num_widgets == 4:
                for j, v in enumerate(params["selections"]["value"].values()):
                    for i in range(num_widgets):
                        k = j * num_widgets + i
                        self.set_widget_information(k, glayout, v)
            else:
                selections = list(params["selections"]["value"].values())
                time_ranges = list(params["time_ranges"]["value"].values())
                selection_mapping = list(params["selection_mapping"]["value"].values())
                for j, (v1, v2, v3) in enumerate(zip(selections, time_ranges,
                                                     selection_mapping)):
                    for i in range(num_widgets):
                        k = j * num_widgets + i
                        if i < 4:
                            self.set_widget_information(k, glayout, v1)
                        elif i >= 4 and i < 6:
                            self.set_widget_information(k, glayout, v2)
                        else:
                            self.set_widget_information(k, glayout, v3)
