from lsst.sims.ocs.configuration import ScienceProposals

from opsim4.model import AreaDistributionPropModel

__all__ = ["ScienceModel"]

class ScienceModel(object):

    def __init__(self):
        """Initialize the class.
        """
        sci_props = ScienceProposals()
        sci_props.load_proposals()

        self.ad_params = {}

        ad_objs = sci_props.area_dist_props.active
        for ad_obj in ad_objs:
            ad_model = AreaDistributionPropModel(ad_obj)
            params = ad_model.make_parameter_dictionary()
            prop_name = params["name"]["value"]
            self.ad_params[prop_name] = params

        #print(self.ad_params)

    def get_proposal_names(self):
        """Return names of stored proposals.

        Returns
        -------
        list[str]
        """
        proposal_names = self.ad_params.keys()
        return proposal_names
