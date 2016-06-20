import collections

import opsim4.controller
from opsim4.utilities import title

__all__ = ["MainController"]

class MainController(object):

    def __init__(self):
        self.tab_order = ["survey"]
        for tab in self.tab_order:
            setattr(self, tab + "_controller",
                    getattr(opsim4.controller, title(tab, spacer="") + "Controller")(tab))

    def get_tabs(self):
        tab_dictionary = collections.OrderedDict()
        for key in self.tab_order:
            tab_dictionary[key] = getattr(self, key + "_controller").get_tab()
        return tab_dictionary
