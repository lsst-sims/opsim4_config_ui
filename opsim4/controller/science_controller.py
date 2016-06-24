from opsim4.controller import BaseController
from opsim4.model import ScienceModel
from opsim4.widgets import ScienceWidget

__all__ = ["ScienceController"]

class ScienceController(BaseController):

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            Tab name for the configuration view.
        """
        BaseController.__init__(self, name)
        self.model = ScienceModel()
        self.widget = ScienceWidget(name)

        self.widget.create_tabs(self.model.get_proposal_names())
