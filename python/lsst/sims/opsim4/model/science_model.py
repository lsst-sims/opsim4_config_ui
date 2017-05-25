import collections
import os

from lsst.sims.ocs.configuration import ScienceProposals, Survey

from lsst.sims.opsim4.model import GeneralPropModel, ModelHelper, SequencePropModel
from lsst.sims.opsim4.utilities import load_class

__all__ = ["ScienceModel"]

class ScienceModel(object):
    """Model class for the science proposal configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        sci_props = ScienceProposals()
        survey = Survey()
        sci_props.load_proposals({"GEN": survey.general_proposals,
                                  "SEQ": survey.sequence_proposals})

        self.general_params = {}
        self.general_modules = {}

        for general_obj in sci_props.general_props.active:
            general_module = load_class(general_obj).__module__
            general_model = GeneralPropModel(general_obj)
            params = general_model.make_parameter_dictionary()
            prop_name = params["name"]["value"]
            self.general_params[prop_name] = params
            self.general_modules[prop_name] = general_module

        self.sequence_params = {}
        self.sequence_modules = {}

        for sequence_obj in sci_props.sequence_props.active:
            sequence_module = load_class(sequence_obj).__module__
            sequence_model = SequencePropModel(sequence_obj)
            params = sequence_model.make_parameter_dictionary()
            prop_name = params["name"]["value"]
            self.sequence_params[prop_name] = params
            self.sequence_modules[prop_name] = sequence_module

    def apply_overrides(self, config_files, extra_props=None):
        """Apply configuration overrides.

        Parameters
        ----------
        config_files : list
            The list of configuration file paths.
        extra_props : str, optional
            A path for extra proposals.
        """
        original_props = self.get_proposal_names()

        sci_props = ScienceProposals()
        survey = Survey()
        sci_props.load_proposals({"GEN": survey.general_proposals,
                                  "SEQ": survey.sequence_proposals},
                                 alternate_proposals=extra_props)

        general_params = {}
        new_general = {}

        for general_obj in sci_props.general_props.active:
            if general_obj.name not in original_props:
                name = general_obj.name
                self.general_modules[name] = load_class(general_obj).__module__
                model = GeneralPropModel(general_obj)
                params = model.make_parameter_dictionary()
                self.general_params[name] = params
                new_general[name] = params
            ModelHelper.load_config(general_obj, config_files)
            general_model = GeneralPropModel(general_obj)
            params = general_model.make_parameter_dictionary()
            prop_name = params["name"]["value"]
            general_params[prop_name] = params

        sequence_params = {}
        new_sequence = {}

        for sequence_obj in sci_props.sequence_props.active:
            if sequence_obj.name not in original_props:
                name = sequence_obj.name
                self.sequence_modules[name] = load_class(sequence_obj).__module__
                model = SequencePropModel(sequence_obj)
                params = model.make_parameter_dictionary()
                self.sequence_params[name] = params
                new_sequence[name] = params
            ModelHelper.load_config(sequence_obj, config_files)
            sequence_model = SequencePropModel(sequence_obj)
            params = sequence_model.make_parameter_dictionary()
            prop_name = params["name"]["value"]
            sequence_params[prop_name] = params

        new_params = collections.namedtuple("new_params",
                                            "general_params sequence_params "
                                            "new_general new_sequence")
        new_params.general_params = general_params
        new_params.sequence_params = sequence_params
        new_params.new_general = new_general
        new_params.new_sequence = new_sequence

        return new_params

    def get_proposal_names(self):
        """Return names of stored proposals.

        Returns
        -------
        list(str)
        """
        proposal_names = self.general_params.keys()
        proposal_names += self.sequence_params.keys()
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

        prop_name = pnames.pop(0)
        pvalue = None
        if prop_name in self.general_params:
            prop_params = self.general_params[prop_name]
        if prop_name in self.sequence_params:
            prop_params = self.sequence_params[prop_name]

        while len(pnames):
            name = pnames.pop(0)
            try:
                # Need to handle integer indexed dictionaries
                name = int(name)
                pvalue = pvalue[name]
                continue
            except ValueError:
                # Filter keys are single letters
                if len(name) == 1:
                    pvalue = pvalue[name]
                    continue
                else:
                    pass
            if pvalue is None:
                pvalue = prop_params[name]["value"]
            else:
                try:
                    pvalue = pvalue[name]["value"]
                except KeyError:
                    # This is a filter parameter, so it needs to be
                    # handled differently
                    name = "_".join(name.split('_')[1:])
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
        if name in self.general_modules:
            modules = self.general_modules
        if name in self.sequence_modules:
            modules = self.sequence_modules

        filename = "{}_prop.py".format(name.lower())
        full_filename = os.path.join(save_dir, filename)
        if not len(changed_params):
            if os.path.exists(full_filename):
                os.remove(full_filename)
            return

        with open(full_filename, 'w') as ofile:
            ofile.write("import {}".format(modules[name]))
            ofile.write(os.linesep)
            ofile.write("assert type(config)=={0}.{1}, \'config is of type %s.%s instead of {0}.{1}\' % "
                        "(type(config).__module__, type(config).__name__)"
                        "".format(modules[name], name))
            ofile.write(os.linesep)
            for pname, value in changed_params:
                property_format = "config.{}={}"
                pparts = pname.split('/')
                if name in pparts:
                    index = pparts.index(name)
                    del pparts[index]
                # Filter parameters need leading part stripped
                if pparts[0] == "filters":
                    pparts[-1] = "_".join(pparts[-1].split('_')[1:])
                prop_name = "{}".format(pparts[0])
                for ppart in pparts[1:]:
                    if ppart.isdigit():
                        prop_name = "{}[{}]".format(prop_name, ppart)
                    elif len(ppart) == 1:
                        prop_name = "{}[\'{}\']".format(prop_name, ppart)
                    else:
                        prop_name = "{}.{}".format(prop_name, ppart)
                try:
                    if "," in value:
                        items = value.split(',')
                        if items[-1] == '':
                            del items[-1]
                        try:
                            if "." in items[0]:
                                pvalue = str([float(x) for x in items])
                            else:
                                pvalue = str([int(x) for x in items])
                        except ValueError:
                            pvalue = str([str(x) for x in items])
                    else:
                        if "." in value:
                            pvalue = float(value)
                        else:
                            pvalue = int(value)
                except ValueError:
                    if value in (str(True), str(False)):
                        pvalue = value == str(True)
                    else:
                        pvalue = str(value)
                        property_format = "config.{}=\'{}\'"

                ofile.write(property_format.format(prop_name, pvalue))
                ofile.write(os.linesep)
