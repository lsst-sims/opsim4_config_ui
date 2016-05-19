from opsim4.controller import BaseController

__all__ = ["ObservatoryController"]

class ObservatoryController(BaseController):

    def __init__(self, name):
        super(ObservatoryController, self).__init__(name)
