import collections

from opsim4.model import ModelHelper
from opsim4.utilities import load_class

__all__ = ["AreaDistributionPropModel"]

class AreaDistributionPropModel(ModelHelper):

    def __init__(self, config_obj):
        """Initialize class.

        Parameters
        ----------
        config_obj : lsst.sims.ocs.configuration.proposal.AreaDistribution instance
            The instance containing the area distribution proposal information.
        """
        self.parameter_order = ["name", "sky_region", "sky_exclusion", "sky_nightly_bounds",
                                "sky_constraints", "scheduling", "filters"]

        ModelHelper.__init__(self, config_obj)

    def make_parameter_dictionary(self):
        """Parameter dictionary for area distribution proposals.
        """
        iparams = ModelHelper.make_parameter_dictionary(self)

        for key in iparams:
            if iparams[key]["dtype"] is None:
                iparams[key]["dtype"] = "GroupBox"
                sub_obj = getattr(self.config_obj, key)
                sub_cls = load_class(sub_obj)
                try:
                    sparams = ModelHelper.make_parameter_dictionary(self, fields=sub_cls._fields, obj=sub_obj)
                    iparams[key]["value"] = sparams
                except AttributeError:
                    iparams[key]["value"] = {}
                    for i, (k1, v1) in enumerate(sub_obj.items()):
                        sub_cls1 = load_class(v1)
                        sparams1 = ModelHelper.make_parameter_dictionary(self, fields=sub_cls1._fields,
                                                                         obj=v1)
                        iparams[key]["value"][i] = sparams1

                iparams1 = iparams[key]["value"]
                for k2 in iparams1:
                    if isinstance(iparams1[k2], collections.defaultdict):
                        continue
                    if iparams1[k2]["dtype"] is None:
                        iparams1[k2]["dtype"] = "GroupBox"
                        sub_obj2 = getattr(sub_obj, k2)
                        try:
                            sub_cls2 = load_class(sub_obj2)
                        except ValueError:
                            continue
                        try:
                            sparams1 = ModelHelper.make_parameter_dictionary(self, fields=sub_cls2._fields,
                                                                             obj=sub_obj2)
                            iparams1[k2]["value"] = sparams1
                        except AttributeError:
                            iparams1[k2]["value"] = {}
                            for j, (k3, v3) in enumerate(sub_obj2.items()):
                                sub_cls3 = load_class(v3)
                                sparams2 = ModelHelper.make_parameter_dictionary(self,
                                                                                 fields=sub_cls3._fields,
                                                                                 obj=v3)
                                iparams1[k2]["value"][j] = sparams2
                        iparams[key]["value"] = iparams1

        final_params = collections.OrderedDict()
        for parameter_name in self.parameter_order:
            final_params[parameter_name] = iparams.get(parameter_name)

        return final_params
