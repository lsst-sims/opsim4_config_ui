import collections
import re

import lsst.pex.config.listField

from opsim4.utilities import load_class

__all__ = ["ModelHelper"]

class ModelHelper(object):

    def __init__(self, config_obj):
        self.config_obj = config_obj
        self.config_cls = load_class(self.config_obj)
        self.paren_match = re.compile(r'\(([^\)]+)\)')

    def get_dict_value(self, name, is_list=False, obj=None):
        """Get the parameter value from the configuration.

        Parameters
        ----------
        name : str
            The parameter name.
        is_list : bool
            A flag to invoke special processing is parameter is a list.
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

    def make_parameter_dictionary(self, fields=None):
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

        param_dict = collections.defaultdict(dict)
        for k, v in fields.items():
            pinfo = param_dict[k]

            tcls = None

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
                print("Cannot handle {}".format(k))

            pinfo["dtype"] = tcls if tcls is not None else str(type(k))
            pinfo["units"] = self.make_unit_label(v.doc)
            pinfo["doc"] = v.doc
            pinfo["format"] = self.make_regex(v.doc)
            pinfo["value"] = self.get_dict_value(k, is_list=pinfo["dtype"].endswith("List"))
            pinfo["complex"] = None

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
