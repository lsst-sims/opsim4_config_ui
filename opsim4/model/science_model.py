import collections

from lsst.sims.ocs.configuration import ScienceProposals

from opsim4.model import ModelHelper
from opsim4.utilities import load_class

__all__ = ["ScienceModel"]

class ScienceModel(ModelHelper):

    def __init__(self):
        super(ScienceModel, self).__init__()
        sci_props = ScienceProposals()
        sci_props.load_proposals()

        self.ad_objs = sci_props.area_dist_props.active
        self.ad_cls = load_class(self.ad_objs[0])
        self.ad_tab_order = ["name", "sky_region", "filters", "scheduling"]

    def make_parameter_dictionary(self):
        param_dict = {}
        for ad_obj in self.ad_objs:
            pdict = super(ScienceModel,
                          self).make_parameter_dictionary(fields=self.ad_cls._fields,
                                                          obj=ad_obj)
            for key in pdict:
                if pdict[key]["dtype"] is None:
                    pdict[key]["dtype"] = "GroupBox"

                    sub_obj = getattr(ad_obj, key)
                    sub_cls = load_class(sub_obj)
                    try:
                        sub_dict = super(ScienceModel,
                                         self).make_parameter_dictionary(fields=sub_cls._fields,
                                                                         obj=sub_obj)
                        pdict[key]["value"] = sub_dict
                    except AttributeError:
                        pdict[key]["value"] = {}
                        for j, (k3, v3) in enumerate(sub_obj.items()):
                            sub_cls3 = load_class(v3)
                            sub_dict3 = super(ScienceModel,
                                              self).make_parameter_dictionary(fields=sub_cls3._fields,
                                                                              obj=v3)
                            pdict[key]["value"][j] = sub_dict3

                    psub_dict = pdict[key]["value"]
                    for k1 in psub_dict:
                        if isinstance(psub_dict[k1], collections.defaultdict):
                            continue
                        if psub_dict[k1]["dtype"] is None:
                            psub_dict[k1]["dtype"] = "GroupBox"

                            sub_obj1 = getattr(sub_obj, k1)
                            sub_cls1 = load_class(sub_obj1)
                            try:
                                sub_dict1 = super(ScienceModel,
                                                  self).make_parameter_dictionary(fields=sub_cls1._fields,
                                                                                  obj=sub_obj1)
                                psub_dict[k1]["value"] = sub_dict1
                            except AttributeError:
                                psub_dict[k1]["value"] = {}
                                for i, (k2, v2) in enumerate(sub_obj1.items()):
                                    sub_cls2 = load_class(v2)
                                    sub_dict2 = super(ScienceModel,
                                                      self).make_parameter_dictionary(fields=sub_cls2._fields,
                                                                                      obj=v2)
                                    psub_dict[k1]["value"][i] = sub_dict2

                            pdict[key]["value"] = psub_dict
            param_dict[ad_obj.name] = pdict

        return param_dict
