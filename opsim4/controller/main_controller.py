import collections

import opsim4.controller
from opsim4.utilities import title

__all__ = ["MainController"]

class MainController(object):
    """Main class for widget-model interactions.

    This class is responsible for setting up and handling interactions
    between the various widgets and their corresponding models.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.tab_order = ["survey", "science", "observatory", "observing_site",
                          "scheduler_driver", "downtime"]
        for tab in self.tab_order:
            setattr(self, tab + "_controller",
                    getattr(opsim4.controller, title(tab, spacer="") + "Controller")(tab))

    def get_diff(self):
        """Get the changed parameters and associated defaults.

        Returns
        -------
        dict
            Set of changed parameters and their associated defaults.
        """
        diff_dict = {}
        for tab in self.tab_order:
            tab_diff = getattr(self, tab + "_controller").get_diff()
            diff_dict.update(tab_diff)
        return diff_dict

    def get_tabs(self):
        """Get the set of tabs for the UI.

        Returns
        -------
        dict(str: QWidget)
            The dictionary of tab, widget pairs.
        """
        tab_dictionary = collections.OrderedDict()
        for tab in self.tab_order:
            tab_dictionary[tab] = getattr(self, tab + "_controller").get_tab()
        return tab_dictionary
