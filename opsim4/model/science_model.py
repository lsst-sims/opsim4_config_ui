import os

from lsst.sims.ocs.configuration import ScienceProposals

from opsim4.model import AreaDistributionPropModel
from opsim4.utilities import load_class

__all__ = ["ScienceModel"]

class ScienceModel(object):

    def __init__(self):
        """Initialize the class.
        """
        sci_props = ScienceProposals()
        sci_props.load_proposals()

        self.ad_params = {}
        self.ad_modules = {}

        ad_objs = sci_props.area_dist_props.active
        for ad_obj in ad_objs:
            ad_module = load_class(ad_obj).__module__
            ad_model = AreaDistributionPropModel(ad_obj)
            params = ad_model.make_parameter_dictionary()
            prop_name = params["name"]["value"]
            self.ad_params[prop_name] = params
            self.ad_modules[prop_name] = ad_module

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
        #print("RR:", name)
        #print("RRR:", changed_params)
        if name in self.ad_modules:
            modules = self.ad_modules

        filename = "{}_prop.py".format(name.lower())
        with open(os.path.join(save_dir, filename), 'w') as ofile:
            ofile.write("import {}".format(modules[name]))
            ofile.write(os.linesep)
            ofile.write("assert type(config)=={0}.{1}, \'config is of type %s.%s instead of {0}.{1}\' % "
                        "(type(config).__module__, type(config).__name__)"
                        "".format(modules[name], name))
            ofile.write(os.linesep)
            for pname, value in changed_params:
                property_format = "config.{}={}"
                pparts = pname.split('/')
                # Filter parameters need leading part stripped
                if pparts[0] == "filters":
                    pparts[-1] = "_".join(pparts[-1].split('_')[1:])
                prop_name = "{}".format(pparts[0])
                for ppart in pparts[1:]:
                    if ppart.isdigit():
                        prop_name = "{}[{}]".format(prop_name, ppart)
                    else:
                        prop_name = "{}.{}".format(prop_name, ppart)
                try:
                    if "," in value:
                        items = value.split(',')
                        try:
                            pvalue = str([float(x) for x in items])
                        except ValueError:
                            pvalue = str([str(x) for x in items])
                    else:
                        pvalue = float(value)
                except ValueError:
                    if value in (str(True), str(False)):
                        pvalue = value == str(True)
                    else:
                        pvalue = str(value)
                        property_format = "config.{}=\'{}\'"

                ofile.write(property_format.format(prop_name, pvalue))
                ofile.write(os.linesep)
