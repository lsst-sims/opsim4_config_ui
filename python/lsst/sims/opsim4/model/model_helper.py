import collections
import os
import re
import sys

import lsst.pex.config.listField
import lsst.pex.config.configDictField

from lsst.sims.opsim4.utilities import load_class

__all__ = ["ModelHelper"]

class ModelHelper(object):
    """The base class for the configuration models.
    """

    def __init__(self, config_obj=None):
        """Initialize the class.

        Parameters
        ----------
        config_obj : instance, optional
            An instance of a configuration object.
        """
        self.config_obj = config_obj
        self.config_cls = load_class(self.config_obj) if config_obj is not None else None
        self.paren_match = re.compile(r'\(([^\)]+)\)')
        self.params = self.make_parameter_dictionary() if config_obj is not None else None

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
        if self.params is not None:
            srep = str(self.params[parameter_name]["value"])
            return value_to_check != srep
        else:
            return False

    def get_dict_value(self, name, is_list=False, obj=None):
        """Get the parameter value from the configuration.

        Parameters
        ----------
        name : str
            The parameter name.
        is_list : bool
            A flag to invoke special processing if parameter is a list.
        obj : configuation instance, optional
            An alternate configuration instance to use.

        Returns
        -------
        simple type
            Returns the value of the configuration parameter.
        """
        cobj = obj if obj is not None else self.config_obj
        value = cobj.toDict()[name]
        if is_list:
            value = ','.join([str(x) for x in value])
        return value

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
        return self.params[parameter_name]["value"]

    def make_parameter(self, pinfo, k, v, obj=None):
        """Create a single set of parameter information.

        Parameters
        ----------
        pinfo : dict
            The parameter information dictionary to fill.
        obj : instance
            (Optional) An instance of the configuration object.
        """
        tcls = None

        pinfo["doc"] = v.doc

        if v.dtype == int:
            tcls = "Int"
        if v.dtype == float:
            tcls = "Float"
        if v.dtype == bool:
            tcls = "Bool"
        if v.dtype == str:
            tcls = "Str"
        if isinstance(v, lsst.pex.config.listField.ListField):
            if v.dtype == float:
                tcls = "DoubleList"
            else:
                tcls = "StringList"
        if tcls is None:
            #print("Cannot handle {}".format(k))
            pinfo["dtype"] = tcls
            pinfo["value"] = tcls
            return

        pinfo["dtype"] = tcls
        pinfo["units"] = self.make_unit_label(v.doc)
        pinfo["format"] = self.make_regex(v.doc)
        pinfo["value"] = self.get_dict_value(k, is_list=pinfo["dtype"].endswith("List"), obj=obj)

    def make_parameter_dictionary(self, fields=None, obj=None, pd=None):
        """Create a parameter information dictionary from configuration.

        This function creates a parameter information dictionary from a particular
        configuration dictionary. Each key, with is the associated parameter name will
        contain the following information:

            - dtype: A string of the basic type for the parameter.
            - units: A string with the parameter's units, None if not required.
            - doc: The documentation string for the parameter.
            - format: A string for a validator from the parameter, None if not required.
            - value: The default value of the parameter.
            - complex: An identifier that indicates the "parameter" is a complex type,
                       None if not required.

        Parameters
        ----------
        fields : dict, optional
            The dictionary of configuration information to parse.
        obj : instance, optional
            An alternate instance of a configuration object.
        pd : dict, optional
            An alternative parameter dictionary to use.
        Returns
        -------
        dict
            The parameter information dictionary.
        """
        if fields is None:
            fields = self.config_cls._fields
        if obj is None:
            obj = self.config_obj

        if pd is None:
            param_dict = collections.defaultdict(dict)
        else:
            param_dict = pd

        for k, v in fields.items():
            pinfo = param_dict[k]
            self.make_parameter(pinfo, k, v, obj=obj)

        return param_dict

    def make_regex(self, doc):
        """Create a regex based off a format request in a parameter doc string.

        Parameters
        ----------
        doc : str
            The doc string to search for units.

        Returns
        -------
        str
            The regex for the format request.
        """
        regex = None
        for match in self.paren_match.findall(doc):
            if match.startswith("format"):
                value = match.split('=')[-1]
                if value == 'YYYY-MM-DD':
                    regex = r'\d{4}-\d{2}-\d{2}'
        return regex

    def make_unit_label(self, doc):
        """Get the untis from a parameter doc string.

        Parameters
        ----------
        doc : str
            The doc string to search for units.

        Returns
        -------
        str
            The units name.
        """
        units = None
        for match in self.paren_match.findall(doc):
            if match.startswith("units"):
                units = match.split('=')[-1]

        return units

    def save_configuration(self, save_dir, name, changed_params):
        """Save the changed parameters to file.

        This function saves changed parameters to file. If a
        file exists and no changes are requested that file is
        deleted.

        Parameters
        ----------
        save_dir : str
            The directory to save the configuration to.
        name : str
            The name for the configuration file.
        changed_params : list((str, str))
            The list of changed parameters.
        """
        filename = "{}.py".format(name)
        full_filename = os.path.join(save_dir, filename)
        if not len(changed_params):
            if os.path.exists(full_filename):
                os.remove(full_filename)
            return

        with open(full_filename, 'w') as ofile:
            ofile.write("import {}".format(self.config_cls.__module__))
            ofile.write(os.linesep)
            ofile.write("assert type(config)=={0}.{1}, \'config is of type %s.%s instead of {0}.{1}\' % "
                        "(type(config).__module__, type(config).__name__)"
                        "".format(self.config_cls.__module__, self.config_cls.__name__))
            ofile.write(os.linesep)
            for pname, value in changed_params:
                property_format = "config.{}={}"
                try:
                    if "," in value:
                        items = value.split(',')
                        try:
                            if "." in items[0]:
                                pvalue = str([float(x) for x in items])
                            else:
                                pvalue = str([int(x) for x in items])
                        except ValueError:
                            pvalue = str([str(x) for x in items])
                    elif isinstance(value, list):
                        pvalue = str(value)
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

                ofile.write(property_format.format(pname, pvalue))
                ofile.write(os.linesep)

    @classmethod
    def load_config(cls, config_obj, config_files):
        """Apply overrides to configuration object.

        Parameters
        ----------
        config_obj : instance
            A configuration instance.
        config_files : list
            A set of paths to configuration file overrides.
        """
        for config_file in config_files:
            try:
                config_obj.load(config_file)
            except AssertionError:
                # Not the right configuration file, so do nothing.
                pass
