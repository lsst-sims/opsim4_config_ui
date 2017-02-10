from lsst.sims.opsim4.widgets import ConfigurationTab

__all__ = ["SchedulerDriverWidget"]

class SchedulerDriverWidget(ConfigurationTab):
    """Widget for the scheduler driver configuration information.
    """

    def __init__(self, name, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        parent : QWidget
            The parent widget of this one.
        """
        ConfigurationTab.__init__(self, name, parent=parent)

    def create_form(self):
        """Create the UI form for the SchedulerDriver widget.
        """
        self.create_widget("Bool", "coadd_values")
        self.create_widget("Bool", "time_balancing")
        self.create_widget("Float", "timecost_time_max")
        self.create_widget("Float", "timecost_time_ref")
        self.create_widget("Float", "timecost_cost_ref")
        self.create_widget("Float", "timecost_weight")
        self.create_widget("Float", "filtercost_weight")
        self.create_widget("Float", "night_boundary")
        self.create_widget("Float", "new_moon_phase_threshold")
        self.create_widget("Bool", "ignore_sky_brightness")
        self.create_widget("Bool", "ignore_airmass")
        self.create_widget("Bool", "ignore_clouds")
        self.create_widget("Bool", "ignore_seeing")
