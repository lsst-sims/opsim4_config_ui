import os

from lsst.sims.opsim4.widgets.wizard import WriterBase, PADDING

__all__ = ["SequenceWriter"]

class SequenceWriter(WriterBase):
    """Class to handle writing a Sequence proposal configuration file.
    """

    def __init__(self):
        """Initialize the class.
        """
        WriterBase.__init__(self)

    def file_def(self, params):
        """Create the file definition information.

        Parameters
        ----------
        params : dict
            The information for the file definition.
        """
        WriterBase.file_def(self, params, "BandFilter")

    def sky_user_regions(self, params):
        """Create the sky user regions information.

        Parameters
        ----------
        params : dict
            The information for the sky user regions.
        """
        self.lines.append("{}# -------------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# Sky User Regions specifications".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# -------------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}self.sky_user_regions = {}".format(PADDING * 2, params["sky_user_regions"]))
        self.lines.append(os.linesep)

    def sky_exclusions(self, params):
        """Create the sky exclusions information.

        Parameters
        ----------
        params : dict
            The information for the sky exclusions.
        """
        WriterBase.sky_exclusions(self, params, "sequence")

    def scheduling(self, params):
        """Create the scheduling information.

        Parameters
        ----------
        params : dict
            The information for the scheduling.
        """
        self.lines.append("{}# ----------------------".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# Scheduling information".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# ----------------------".format(PADDING * 2))
        self.lines.append(os.linesep)

        max_num_targets = str(params["sequence_scheduling_max_num_targets"])
        if max_num_targets == "":
            max_num_targets = "100"
        self.lines.append("{}self.scheduling.max_num_targets "
                          "= {}".format(PADDING * 2, max_num_targets))
        self.lines.append(os.linesep)
        self.lines.append("{}self.scheduling.accept_serendipity "
                          "= {}".format(PADDING * 2,
                                        params["sequence_scheduling_accept_serendipity"]))
        self.lines.append(os.linesep)
        self.lines.append("{}self.scheduling.accept_consecutive_visits "
                          "= {}".format(PADDING * 2,
                                        params["sequence_scheduling_accept_consecutive_visits"]))
        self.lines.append(os.linesep)
        self.lines.append("{}self.scheduling.airmass_bonus = {}"
                          .format(PADDING * 2, str(params["sequence_scheduling_airmass_bonus"])))
        self.lines.append(os.linesep)

    def band_filters(self, params):
        """Create the band filters information.

        Parameters
        ----------
        params : dict
            The information for the band filters.
        """
        self.lines.append("{}# --------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# Band Filter specifications".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# --------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)

        used_filters = []
        for band_filter in "u,g,r,i,z,y".split(','):
            field_stem = "{}_filter".format(band_filter)
            use_filter = params["sequence_{}_use".format(field_stem)]
            if use_filter:
                used_filters.append(("{}.name".format(field_stem), field_stem))
                self.lines.append("{}{} = BandFilter()".format(PADDING * 2, field_stem))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.name = \'{}\'".format(PADDING * 2, field_stem, band_filter))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.bright_limit = {}".
                                  format(PADDING * 2, field_stem,
                                         str(params["sequence_{}_bright_limit".format(field_stem)])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.dark_limit = {}".
                                  format(PADDING * 2, field_stem,
                                         str(params["sequence_{}_dark_limit".format(field_stem)])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.max_seeing = {}".
                                  format(PADDING * 2, field_stem,
                                         str(params["sequence_{}_max_seeing".format(field_stem)])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.exposures = [{}]".
                                  format(PADDING * 2, field_stem,
                                         str(params["sequence_{}_exposures".
                                                    format(field_stem)]).replace(',', ', ')))
                self.lines.append(os.linesep)

        filters_spec = self.format_dictionaries(used_filters)

        self.lines.append("{}self.filters = {}{}{}".format(PADDING * 2, "{", filters_spec, "}"))
        self.lines.append(os.linesep)
