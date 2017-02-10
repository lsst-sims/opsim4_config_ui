from lsst.sims.opsim4.controller import BaseController
from lsst.sims.opsim4.model import DowntimeModel
from lsst.sims.opsim4.widgets import DowntimeWidget

__all__ = ["DowntimeController"]

class DowntimeController(BaseController):
    """The controller for the downtime configuration.
    """

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The tab name for the configuration view.
        """
        BaseController.__init__(self, name)
        self.model = DowntimeModel()
        self.widget = DowntimeWidget(name)

        for key, value in self.model.params.items():
            self.widget.set_information(key, value)
        self.widget.checkProperty.connect(self.check_property)
        self.widget.getProperty.connect(self.get_property)
        self.widget.saveConfiguration.connect(self.save_configuration)
