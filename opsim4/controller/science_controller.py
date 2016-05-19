from opsim4.controller import BaseController

__all__ = ["ScienceController"]

class ScienceController(BaseController):

    def __init__(self, name):
        super(ScienceController, self).__init__(name)
