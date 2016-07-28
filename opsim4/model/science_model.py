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
        print("YY:", value_to_check, dict_value)
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
        print("H:", pnames)

        prop_name = pnames.pop(0)
        pvalue = None
        if prop_name in self.ad_params:
            prop_params = self.ad_params[prop_name]
            while len(pnames):
                name = pnames.pop(0)
                print("X:", name)
                try:
                    # Need to handle integer indexed dictionaries
                    name = int(name)
                    pvalue = pvalue[name]
                    continue
                except ValueError:
                    pass
                if pvalue is None:
                    pvalue = prop_params[name]["value"]
                else:
                    try:
                        pvalue = pvalue[name]["value"]
                    except KeyError:
                        # This is a filter parameter, so it needs to be
                        # handled differently
                        # print("Q:", pvalue)
                        name = "_".join(name.split('_')[1:])
                        pvalue = pvalue[name]["value"]

        print("CC:", pvalue)
        return pvalue
