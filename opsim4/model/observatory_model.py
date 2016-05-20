import collections

from lsst.sims.ocs.configuration import Observatory
from opsim4.model import ModelHelper
from opsim4.utilities import load_class

__all__ = ["ObservatoryModel"]

class ObservatoryModel(ModelHelper):

    def __init__(self):
        super(ObservatoryModel, self).__init__(Observatory())
        self.tab_order = ["telescope", "dome", "rotator", "camera", "slew", "park", "obs_var"]

    def make_parameter_dictionary(self):
        param_dict = collections.OrderedDict()
        for k in self.tab_order:
            v = getattr(self.config_obj, k)
            v_cls_fields = load_class(v)._fields
            param_dict[k] = super(ObservatoryModel, self).make_parameter_dictionary(fields=v_cls_fields,
                                                                                    obj=v)
        return param_dict
