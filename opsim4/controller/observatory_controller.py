from opsim4.controller import BaseController
from opsim4.model import ObservatoryModel
from opsim4.widgets import ObservatoryWidget

__all__ = ["ObservatoryController"]

class ObservatoryController(BaseController):

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            Tab name for the configuration view.
        """
        BaseController.__init__(self, name)
        self.model = ObservatoryModel()
        self.widget = ObservatoryWidget(name)

        #self.widget.create_tabs(self.model.params)
