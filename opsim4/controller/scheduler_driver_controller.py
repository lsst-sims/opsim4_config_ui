from opsim4.controller import BaseController
from opsim4.model import SchedulerDriverModel
from opsim4.widgets import SchedulerDriverWidget

__all__ = ["SchedulerDriverController"]

class SchedulerDriverController(BaseController):
    """The controller for the scheduler driver configuration.
    """

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The tab name for the configuration view.
        """
        super(SchedulerDriverController, self).__init__(name)
        self.model = SchedulerDriverModel()
        self.widget = SchedulerDriverWidget(name)

        for key, value in self.model.params.items():
            self.widget.set_information(key, value)
        self.widget.checkProperty.connect(self.check_property)
        self.widget.getProperty.connect(self.get_property)
        self.widget.saveConfiguration.connect(self.save_configuration)
