from opsim4.controller import BaseController

__all__ = ["ObservingSiteController"]

class ObservingSiteController(BaseController):

    def __init__(self, name):
        super(ObservingSiteController, self).__init__(name)
