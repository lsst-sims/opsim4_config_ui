import collections
import re

import lsst.pex.config.listField
import lsst.pex.config.configDictField

from opsim4.utilities import load_class

__all__ = ["ModelHelper"]

class ModelHelper(object):

    def __init__(self, config_obj=None):
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

            print("D:", parameter_name, value_to_check, srep)
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
        obj : configuation instance
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
        fields : dict
            (Optional) The dictionary of configuration information to parse.

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
