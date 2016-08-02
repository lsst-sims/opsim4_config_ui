from opsim4.model import CameraModel, DomeModel, ObservatoryVariationModel
from opsim4.model import OpticsLoopCorrModel, ParkModel, RotatorModel
from opsim4.model import SlewModel, TelescopeModel

__all__ = ["ObservatoryModel"]

class ObservatoryModel(object):
    """Model class for the bbservatory configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.params = {}
        self.params["telescope"] = TelescopeModel()
        self.params["dome"] = DomeModel()
        self.params["camera"] = CameraModel()
        self.params["rotator"] = RotatorModel()
        self.params["slew"] = SlewModel()
        self.params["optics_loop_corr"] = OpticsLoopCorrModel()
        self.params["park"] = ParkModel()
        self.params["obs_variation"] = ObservatoryVariationModel()
