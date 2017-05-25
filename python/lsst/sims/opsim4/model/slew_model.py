import os

from lsst.sims.ocs.configuration.instrument import Slew

from lsst.sims.opsim4.model import ModelHelper

__all__ = ["SlewModel"]

class SlewModel(ModelHelper):
    """Model class for the slew configuration.
    """

    def __init__(self):
        """Initialize the class.
        """
        ModelHelper.__init__(self, Slew())

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
                if "," in value:
                    items = value.split(',')
                    if items[-1] == '':
                        del items[-1]
                    pvalue = str([str(x) for x in items])
                elif value != "":
                    pvalue = "[\'{}\']".format(value)
                else:
                    pvalue = "[]"

                ofile.write(property_format.format(pname, pvalue))
                ofile.write(os.linesep)
