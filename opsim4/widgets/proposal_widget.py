from PyQt4 import QtGui

from opsim4.widgets import ConfigurationTab
from opsim4.widgets.constants import CSS_GROUPBOX

__all__ = ["ProposalWidget"]

class ProposalWidget(ConfigurationTab):

    def __init__(self, name, params, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        parent : QWidget
            The parent widget of this one.
        """
        self.group_box_rows = []
        self.num_group_boxes = 0
        self.setup = params

        ConfigurationTab.__init__(self, name, parent)
        #self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #print(params)
        #self.create_sky_region(params["sky_region"]["value"])
        del self.setup

    def create_form(self):
        """Create the form for the proposal widget.
        """
        self.create_widget("Str", "name")
        self.create_group_box("sky_region")
        self.create_group_box("sky_exclusions")
        self.create_group_box("sky_nightly_bounds")
        self.create_group_box("sky_constraints")
        self.create_group_box("scheduling")
        self.create_group_box("filters")

    def create_group_box(self, name):
        """Create a group box for configuration information."

        Parameters
        ----------
        name : str
            Label for the group box widget.
        """
        #print(self.setup[name])
        try:
            params = self.setup[name]["value"]
        except TypeError:
            print("Oops!")
            return
        self.num_group_boxes += 1
        #self.group_box_rows.append(0)
        group_box = QtGui.QGroupBox(name)
        group_box.setStyleSheet(CSS_GROUPBOX)
        grid_layout = QtGui.QGridLayout()
        func = getattr(self, "create_{}".format(name))

        func(grid_layout, params)
        group_box.setLayout(grid_layout)
        self.layout.addWidget(group_box, self.rows, 0, 1, 3)
        self.rows += 1

    def set_information(self, params):
        """Set the information for the configuration.

        Parameters
        ----------
        params : dict
            The configuration information.
        """
        pass
        #self.set_sky_region(params["sky_region"]["value"])

    def create_sky_region(self, glayout, params):
        """Set the information for the proposal sky region.

        params : dict
            The configuration information for the sky region.
        """
        num_selections = len(params["selections"]["value"])
        if num_selections:
            for i in xrange(num_selections):
                qualifier = "selections/{}".format(i)
                self.create_widget("Str", "limit_type", qualifier=qualifier, layout=glayout,
                                   rows=(num_selections + 0))
                self.create_widget("Float", "minimum_limit", qualifier=qualifier, layout=glayout,
                                   rows=(num_selections + 1))
                self.create_widget("Float", "maximum_limit", qualifier=qualifier, layout=glayout,
                                   rows=(num_selections + 2))
                self.create_widget("Float", "bounds_limit", qualifier=qualifier, layout=glayout,
                                   rows=(num_selections + 3))
            self.group_box_rows.append(num_selections * 4)

    def create_sky_exclusions(self, glayout, params):
        self.create_widget("Float", "dec_window", layout=glayout, rows=0)
        num_selections = len(params["selections"]["value"])
        if num_selections:
            n = num_selections - 1
            for i in xrange(num_selections):
                j = n - i
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
        self.create_widget("Float", "twilight_boundary", layout=glayout, rows=0)
        self.create_widget("Float", "delta_lst", layout=glayout, rows=1)
        self.group_box_rows.append(2)

    def create_sky_constraints(self, glayout, params):
        self.create_widget("Float", "max_airmass", layout=glayout, rows=0)
        self.group_box_rows.append(1)

    def create_scheduling(self, glayout, params):
        self.create_widget("Int", "max_num_targets", layout=glayout, rows=0)
        self.create_widget("Bool", "accept_serendipity", layout=glayout, rows=1)
        self.create_widget("Bool", "accept_consecutive_obs", layout=glayout, rows=2)
        self.group_box_rows.append(3)

    def create_filters(self, glayout, params):
        num_filters = len(params)
        if num_filters:
            filter_order = "u g r i z y".split()
            filter_index = {v["name"]["value"]: k for k, v in params.items()}
            n = num_filters - 1
            for i, band_filter in enumerate(filter_order):
                x = filter_index.get(band_filter, None)
                if i is not None:
                    j = n * i
                    qualifier = "filter/{}".format(x)
                    filter_name = params[x]["name"]["value"]
                    self.create_widget("Int", "{}_num_visits".format(filter_name), qualifier=qualifier,
                                       layout=glayout, rows=(j + 0))
                    self.create_widget("Float", "{}_bright_limit".format(filter_name), qualifier=qualifier,
                                       layout=glayout, rows=(j + 1))
                    self.create_widget("Float", "{}_dark_limit".format(filter_name), qualifier=qualifier,
                                       layout=glayout, rows=(j + 2))
                    self.create_widget("Float", "{}_max_seeing".format(filter_name), qualifier=qualifier,
                                       layout=glayout, rows=(j + 3))
                    self.create_widget("StringList", "{}_exposures".format(filter_name), qualifier=qualifier,
                                       layout=glayout, rows=(j + 4))
                else:
                    continue
        self.group_box_rows.append(num_filters * 5)
