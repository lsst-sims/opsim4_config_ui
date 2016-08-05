from opsim4.controller import BaseController
from opsim4.model import ObservingSiteModel
from opsim4.widgets import ObservingSiteWidget

__all__ = ["ObservingSiteController"]

class ObservingSiteController(BaseController):
    """The controller for the observing site configuration.
    """

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The tab name for the configuration view.
        """
        BaseController.__init__(self, name)
        self.model = ObservingSiteModel()
        self.widget = ObservingSiteWidget(name)

        for key, value in self.model.params.items():
            self.widget.set_information(key, value)
        self.widget.checkProperty.connect(self.check_property)
        self.widget.getProperty.connect(self.get_property)
        self.widget.saveConfiguration.connect(self.save_configuration)
