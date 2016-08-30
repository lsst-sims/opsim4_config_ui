from lsst.sims.opsim4.widgets import ConfigurationTab

__all__ = ["SlewWidget"]

class SlewWidget(ConfigurationTab):
    """Widget for the slew configuration information.
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
        """Create the UI form for the Slew widget.
        """
        self.create_widget("StringList", "prereq_domalt", qualifier=self.name)
        self.create_widget("StringList", "prereq_domaz", qualifier=self.name)
        self.create_widget("StringList", "prereq_domazsettle", qualifier=self.name)
        self.create_widget("StringList", "prereq_telalt", qualifier=self.name)
        self.create_widget("StringList", "prereq_telaz", qualifier=self.name)
        self.create_widget("StringList", "prereq_telrot", qualifier=self.name)
        self.create_widget("StringList", "prereq_telopticsopenloop", qualifier=self.name)
        self.create_widget("StringList", "prereq_telopticsclosedloop", qualifier=self.name)
        self.create_widget("StringList", "prereq_telsettle", qualifier=self.name)
        self.create_widget("StringList", "prereq_filter", qualifier=self.name)
        self.create_widget("StringList", "prereq_exposures", qualifier=self.name)
        self.create_widget("StringList", "prereq_readout", qualifier=self.name)
        self.create_widget("StringList", "prereq_adc", qualifier=self.name)
        self.create_widget("StringList", "prereq_ins_optics", qualifier=self.name)
        self.create_widget("StringList", "prereq_guider_pos", qualifier=self.name)
        self.create_widget("StringList", "prereq_guider_adq", qualifier=self.name)
