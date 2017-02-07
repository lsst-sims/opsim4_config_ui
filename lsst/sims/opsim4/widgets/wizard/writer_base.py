import os

from lsst.sims.opsim4.widgets.wizard import PADDING

__all__ = ["WriterBase"]

class WriterBase(object):
    """Base class for handling proposal configuration file writing.
    """

    def __init__(self):
        """Initialize the class.
        """
        self.lines = []

    def file_def(self, params, extra_classes):
        """Create the file definition information.

        Parameters
        ----------
        params : dict
            The information for the file definition.
        extra_classes : str
            A comma-delimited list of classes.
        """
        full_prop_name = params["full_prop_name"]
        prop_type = params["prop_type"]
        prop_reg_type = params["prop_reg_type"]
        self.lines.append("import lsst.pex.config as pexConfig")
        self.lines.append(os.linesep)
        self.lines.append("from lsst.sims.ocs.configuration.proposal import {}".format(params["prop_type"]))
        self.lines.append(os.linesep)
        self.lines.append("from lsst.sims.ocs.configuration.proposal import {}".format(extra_classes))
        self.lines.append(os.linesep)
        self.lines.append("from lsst.sims.ocs.configuration.proposal import {}".format(prop_reg_type))
        self.lines.append(os.linesep)
        self.lines.append("__all__ = [\"{}\"]".format(full_prop_name))
        self.lines.append(os.linesep)
        self.lines.append("@pexConfig.registerConfig(\"{}\", {}, {})".format(full_prop_name,
                                                                             prop_reg_type, prop_type))
        self.lines.append(os.linesep)
        self.lines.append("class {}({}):".format(full_prop_name, prop_type))
        self.lines.append(os.linesep)
        self.lines.append("{}def setDefaults(self):".format(PADDING))
        self.lines.append(os.linesep)
        self.lines.append("{}self.name = \"{}\"".format(PADDING * 2, full_prop_name))
        self.lines.append(os.linesep)

    def sky_exclusions(self, params, param_tag):
        """Create the sky exclusion information.

        Parameters
        ----------
        params : dict
            The information for the sky exclusions.
        param_tag : str
            Identifier for proposal type.
        """
        self.lines.append("{}# ----------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# Sky Exclusion specifications".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# ----------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)

        self.lines.append("{}self.sky_exclusion.dec_window "
                          "= {}".format(PADDING * 2,
                                        str(params["{}_sky_exclusions_dec_window".format(param_tag)])))
        self.lines.append(os.linesep)

        sky_exclusion_selections = str(params["sky_exclusion_selections"]).strip()
        if sky_exclusion_selections != "":
            selection_obj = "excl0"
            parts = sky_exclusion_selections.split(',')
            self.lines.append("{}{} = Selection()".format(PADDING * 2, selection_obj))
            self.lines.append(os.linesep)
            self.lines.append("{}{}.limit_type = \"{}\"".format(PADDING * 2, selection_obj, parts[0]))
            self.lines.append(os.linesep)
            self.lines.append("{}{}.minimum_limit = {}".format(PADDING * 2, selection_obj, float(parts[1])))
            self.lines.append(os.linesep)
            self.lines.append("{}{}.maximum_limit = {}".format(PADDING * 2, selection_obj, float(parts[2])))
            self.lines.append(os.linesep)
            self.lines.append("{}{}.bounds_limit = {}".format(PADDING * 2, selection_obj, float(parts[3])))
            self.lines.append(os.linesep)
            self.lines.append("{}self.sky_exclusion.selections = {}0: {}{}".format(PADDING * 2, "{",
                                                                                   selection_obj, "}"))
            self.lines.append(os.linesep)

    def sky_nightly_bounds(self, params):
        """Create the sky nightly bounds information.

        Parameters
        ----------
        params : dict
            The information for the sky nightly bounds.
        """
        self.lines.append("{}# ---------------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# Sky Nightly Bounds specifications".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# ---------------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}self.sky_nightly_bounds.twilight_boundary = {}"
                          .format(PADDING * 2, str(params["sky_nightly_bounds_twilight_boundary"])))
        self.lines.append(os.linesep)

        self.lines.append("{}self.sky_nightly_bounds.delta_lst = {}"
                          .format(PADDING * 2, str(params["sky_nightly_bounds_delta_lst"])))
        self.lines.append(os.linesep)

    def sky_constraints(self, params):
        """Create the sky constraints information.

        Parameters
        ----------
        params : dict
            The information for the sky constraints.
        """
        self.lines.append("{}# ------------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# Sky Constraints specifications".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# ------------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)

        self.lines.append("{}self.sky_constraints.max_airmass = {}"
                          .format(PADDING * 2, str(params["sky_constraints_max_airmass"])))
        self.lines.append(os.linesep)
        self.lines.append("{}self.sky_constraints.max_cloud = {}"
                          .format(PADDING * 2, str(params["sky_constraints_max_cloud"])))
        self.lines.append(os.linesep)

    def format_dictionaries(self, infos, padding_size=PADDING * 6):
        """Format dictionaries in columns.

        Parameters
        ----------
        infos : list
            The set of information for writing the dictionary.

        Returns
        -------
        list
            The column list for the dictionary.
        """
        out_list = []
        for i, info in enumerate(infos):
            if i != 0:
                line_padding = padding_size
            else:
                line_padding = ""
            out_list.append("{}{}: {},".format(line_padding, info[0], info[1]))

        out_list[-1] = out_list[-1].strip(',')
        return os.linesep.join(out_list)
