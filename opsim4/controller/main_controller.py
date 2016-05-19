__all__ = ["MainController"]

class MainController(object):

    def __init__(self):
        self.tab_order = ["survey", "science", "observing_site", "observatory"]

    def get_tabs(self):
        return {}
