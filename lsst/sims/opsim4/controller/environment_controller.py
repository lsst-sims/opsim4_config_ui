from lsst.sims.opsim4.controller import BaseController
from lsst.sims.opsim4.model import EnvironmentModel
from lsst.sims.opsim4.widgets import EnvironmentWidget

__all__ = ["EnvironmentController"]

class EnvironmentController(BaseController):
    """The controller for the environment configuration.
    """

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The tab name for the configuration view.
        """
        BaseController.__init__(self, name)
        self.model = EnvironmentModel()
        self.widget = EnvironmentWidget(name)

        for key, value in self.model.params.items():
            self.widget.set_information(key, value)
        self.widget.checkProperty.connect(self.check_property)
        self.widget.getProperty.connect(self.get_property)
        self.widget.saveConfiguration.connect(self.save_configuration)
