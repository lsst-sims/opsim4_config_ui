import importlib

from lsst.sims.opsim4.utilities import title
from lsst.sims.opsim4.widgets import ConfigurationTabWidget

__all__ = ["ObservatoryWidget"]

class ObservatoryWidget(ConfigurationTabWidget):

    def __init__(self, name, parent=None):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name for the tab title.
        parent : QWidget
            The parent widget of this one.
        """
        ConfigurationTabWidget.__init__(self, name, parent)

        self.tab_mapping = {"telescope": "TelescopeWidget",
                            "dome": "DomeWidget",
                            "rotator": "RotatorWidget",
                            "camera": "CameraWidget",
                            "optics_loop_corr": "OpticsLoopCorrWidget",
                            "slew": "SlewWidget",
                            "park": "ParkWidget",
                            "filters": "FiltersWidget",
                            "obs_var": "ObservatoryVariationWidget"}

    def create_tabs(self, params):
        """Create the individual proposal tabs.

        Parameters
        ----------
        params : dict(str: params)
            Set of configuration information.
        """
        module = importlib.import_module("lsst.sims.opsim4.widgets")
        for name in params:
            obs_widget = getattr(module, self.tab_mapping[name])
            tab = obs_widget(name)
            self.addTab(tab, title(name))

    def set_information(self, params, full_check=False):
        """Set information for the configuration tabs.

        Parameters
        ----------
        params : dict
            The set of information for the configuration
        full_check : bool
            Flag to trigger signals for property changes.
        """
        for i in range(self.count()):
            tab = self.widget(i)
            for key, info in params[tab.name].params.items():
                tab.set_information(key, info, full_check=full_check)
