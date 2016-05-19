import collections

import opsim4.controller

__all__ = ["MainController"]

class MainController(object):

    def __init__(self):
        self.tab_order = ["survey", "science", "observing_site", "observatory"]
        self.survey_controller = opsim4.controller.SurveyController()
        self.science_controller = opsim4.controller.ScienceController()
        self.observing_site_controller = opsim4.controller.ObservingSiteController()
        self.observatory_controller = opsim4.controller.ObservatoryController()

    def get_tabs(self):
        tab_dictionary = collections.OrderedDict()
        for key in self.tab_order:
            tab_dictionary[key] = getattr(self, key + "_controller").get_tab()
        return tab_dictionary
