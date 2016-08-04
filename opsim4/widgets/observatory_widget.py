import importlib

from opsim4.widgets import ConfigurationTabWidget
from opsim4.utilities import title

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
                            "obs_var": "ObservatoryVariationWidget"}

    def create_tabs(self, params):
        """Create the individual proposal tabs.

        Parameters
        ----------
        params : dict{str : params}
            Set of configuration information.
        """
        module = importlib.import_module("opsim4.widgets")
        for name in params:
            obs_widget = getattr(module, self.tab_mapping[name])
            tab = obs_widget(name)
            self.addTab(tab, title(name))

    def set_information(self, params):
        """Set information for the configuration tabs.

        Parameters
        ----------
        param_dict : dict
            The set of information for the configuration
        """
        for i in xrange(self.count()):
            tab = self.widget(i)
            for key, info in params[tab.name].params.items():
                tab.set_information(key, info)
