import collections

from lsst.sims.opsim4.model import CameraModel, DomeModel, FiltersModel
from lsst.sims.opsim4.model import ObservatoryVariationModel, OpticsLoopCorrModel
from lsst.sims.opsim4.model import ParkModel, RotatorModel
from lsst.sims.opsim4.model import SlewModel, TelescopeModel

__all__ = ["ObservatoryModel"]

class ObservatoryModel(object):
    """Model class for the bbservatory configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.params = collections.OrderedDict()
        self.params["telescope"] = TelescopeModel()
        self.params["dome"] = DomeModel()
        self.params["rotator"] = RotatorModel()
        self.params["camera"] = CameraModel()
        self.params["optics_loop_corr"] = OpticsLoopCorrModel()
        self.params["slew"] = SlewModel()
        self.params["park"] = ParkModel()
        self.params["filters"] = FiltersModel()
        self.params["obs_var"] = ObservatoryVariationModel()

    def check_parameter(self, parameter_name, value_to_check):
        """Check a given value against the currently stored information.

        Parameters
        ----------
        parameter_name : str
            The name of the parameter to check.
        value_to_check : str
            The string representation of the parameter's associated value to check.

        Returns
        -------
        bool
            True if value is different from stored, false if same.
        """
        dict_value = str(self.get_parameter(parameter_name))
        return value_to_check != dict_value

    def get_parameter(self, parameter_name):
        """Get a value for the given parameter.

        Parameters
        ----------
        parameter_name : str
            The name of the parameter to fetch the value of.

        Returns
        -------
        any
            The associated parameter value.
        """
        pnames = parameter_name.split('/')

        name = pnames.pop(0)
        pvalue = None
        if name in self.params:
            params = self.params[name].params
            while len(pnames):
                name = pnames.pop(0)
                if pvalue is None:
                    pvalue = params[name]["value"]
                else:
                    pvalue = pvalue[name]["value"]

        return pvalue

    def save_configuration(self, save_dir, name, changed_params):
        """Save the changed parameters to file.

        Parameters
        ----------
        save_dir : str
            The directory to save the configuration to.
        name : str
            The name for the configuration file.
        changed_params : list((str, str))
            The list of changed parameters.
        """
        # Need to strip out tab identifier since the diff file doesn't need it.
        corrected_changes = [(k.split('/')[-1], v) for k, v in changed_params]
        self.params[name].save_configuration(save_dir, name, corrected_changes)
