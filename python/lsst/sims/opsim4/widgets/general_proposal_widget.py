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
        if num_selections:
            num_widgets = 4
            for i in xrange(num_selections):
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
            self.group_box_rows.append(num_selections * 4)

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
        """
        self.full_check = full_check
        name_widget = self.layout.itemAtPosition(0, 1).widget()
        name_widget.setText(str(params["name"]["value"]))
        name_widget.setToolTip(str(params["name"]["doc"]))
        self.set_sky_region(params["sky_region"]["value"])
        self.set_sky_exclusion(params["sky_exclusion"]["value"])
        self.set_sky_nightly_bounds(params["sky_nightly_bounds"]["value"], 2)
        self.set_sky_constraints(params["sky_constraints"]["value"], 3)
        self.set_scheduling(params["scheduling"]["value"], 5, 4)
        self.set_filters(params["filters"]["value"], 6, 5)

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
            for j, v in enumerate(params["selections"]["value"].values()):
                for i in xrange(num_widgets):
                    k = j * num_widgets + i
                    self.set_widget_information(k, glayout, v)
