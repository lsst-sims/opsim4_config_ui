from PyQt4 import QtGui

from opsim4.widgets import ConfigurationTab
from opsim4.widgets.constants import CSS_GROUPBOX

__all__ = ["ProposalWidget"]

class ProposalWidget(ConfigurationTab):

    def __init__(self, name, parent=None):
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

        ConfigurationTab.__init__(self, name, parent)

    def create_form(self):
        """Create the form for the proposal widget.
        """
        self.create_widget("Str", "name")
        self.create_group_box("sky_regions")
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
        group_box = QtGui.QGroupBox(name)
        group_box.setStyleSheet(CSS_GROUPBOX)
        grid_layout = QtGui.QGridLayout()
        group_box.setLayout(grid_layout)
        self.num_group_boxes += 1
        self.group_box_rows.append(0)

        self.layout.addWidget(group_box, self.rows, 0, 1, 3)
        self.rows += 1
