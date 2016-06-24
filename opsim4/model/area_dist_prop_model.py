from opsim4.model import ModelHelper

__all__ = ["AreaDistributionPropModel"]

class AreaDistributionPropModel(ModelHelper):

    def __init__(self, config_obj):
        """Initialize class.

        Parameters
        ----------
        config_obj : lsst.sims.ocs.configuration.proposal.AreaDistribution instance
            The instance containing the area distribution proposal information.
        """
        ModelHelper.__init__(self, config_obj)
        self.parameter_order = ["name", "sky_region", "sky_exclusions", "sky_nightly_bounds",
                                "sky_constraints", "scheduling", "filters"]
