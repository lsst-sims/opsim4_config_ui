import os

from lsst.sims.opsim4.widgets.wizard import WriterBase, PADDING

__all__ = ["GeneralWriter"]

class GeneralWriter(WriterBase):
    """Class to handle writing a General proposal configuration file.
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
        WriterBase.file_def(self, params, "GeneralBandFilter, Selection")

    def sky_regions(self, params):
        """Create the sky regions information.

        Parameters
        ----------
        params : dict
            The information for the sky regions.
        """
        self.lines.append("{}# -------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# Sky Region specifications".format(PADDING * 2))
        self.lines.append(os.linesep)
        self.lines.append("{}# -------------------------".format(PADDING * 2))
        self.lines.append(os.linesep)

        sky_regions_selections = str(params["sky_region_selections"]).strip()
        selection_list = []
        time_range_values = []
        selection_mapping_values = []
        for i, sky_region_selection in enumerate(sky_regions_selections.split(os.linesep)):
            selection_obj = "sel{}".format(i)
            selection_list.append((str(i), selection_obj))
            parts = sky_region_selection.split(',')
            self.lines.append("{}{} = Selection()".format(PADDING * 2, selection_obj))
            self.lines.append(os.linesep)
            self.lines.append("{}{}.limit_type = \"{}\"".format(PADDING * 2, selection_obj, parts[0]))
            self.lines.append(os.linesep)
            self.lines.append("{}{}.minimum_limit = {}".format(PADDING * 2, selection_obj,
                                                               float(parts[1])))
            self.lines.append(os.linesep)
            self.lines.append("{}{}.maximum_limit = {}".format(PADDING * 2, selection_obj,
                                                               float(parts[2])))
            self.lines.append(os.linesep)
            bounds_limit = parts[3]
            if parts[3] != "nan":
                self.lines.append("{}{}.bounds_limit = {}".format(PADDING * 2, selection_obj,
                                                                  float(bounds_limit)))
                self.lines.append(os.linesep)
            start_time = int(parts[4])
            if start_time:
                time_range_values.append((start_time, int(parts[5])))
                if len(selection_mapping_values) == 0:
                    selection_mapping_values.append([i])
                else:
                    index = len(time_range_values) - 2
                    if start_time == time_range_values[index][0]:
                        selection_mapping_values[-1].append(i)
                    else:
                        selection_mapping_values.append([i])

        selection_spec = self.format_dictionaries(selection_list, padding_size=PADDING * 9 + "  ")
        self.lines.append("{}self.sky_region.selections = {}{}{}".format(PADDING * 2, "{",
                                                                         selection_spec, "}"))
        self.lines.append(os.linesep)

        if len(time_range_values):
            self.lines[2] += ", SelectionList, TimeRange"
            time_range_list = []
            for j, time_range in enumerate(time_range_values):
                time_range_obj = "time_range{}".format(j)
                time_range_list.append((str(j), time_range_obj))
                self.lines.append("{}{} = TimeRange()".format(PADDING * 2, time_range_obj))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.start = {}".format(PADDING * 2, time_range_obj,
                                                           str(time_range[0])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.end = {}".format(PADDING * 2, time_range_obj,
                                                         str(time_range[1])))
                self.lines.append(os.linesep)
            time_range_spec = self.format_dictionaries(time_range_list, padding_size=PADDING * 9 + "   ")
            self.lines.append("{}self.sky_region.time_ranges = {}{}{}".format(PADDING * 2, "{",
                                                                              time_range_spec, "}"))
            self.lines.append(os.linesep)

            selection_mapping_list = []
            for k, selection_mapping in enumerate(selection_mapping_values):
                selection_mapping_obj = "sel_map{}".format(k)
                selection_mapping_list.append((str(k), selection_mapping_obj))
                self.lines.append("{}{} = SelectionList()".format(PADDING * 2, selection_mapping_obj))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.indexes = {}".format(PADDING * 2, selection_mapping_obj,
                                                             str(selection_mapping)))
                self.lines.append(os.linesep)
            selection_mapping_spec = self.format_dictionaries(selection_mapping_list,
                                                              padding_size=PADDING * 11 + " ")
            self.lines.append("{}self.sky_region.selection_mapping "
                              "= {}{}{}".format(PADDING * 2, "{", selection_mapping_spec, "}"))

            self.lines.append(os.linesep)

        sky_region_combiners = str(params["sky_region_combiners"])
        if sky_region_combiners != "":
            self.lines.append("{}self.sky_region.combiners = "
                              "{}".format(PADDING * 2, sky_region_combiners.split(',')))
            self.lines.append(os.linesep)

    def sky_exclusions(self, params):
        """Create the sky exclusion information.

        Parameters
        ----------
        params : dict
            The information for the sky exclusions.
        """
        WriterBase.sky_exclusions(self, params, "general")

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

        max_num_targets = str(params["general_scheduling_max_num_targets"])
        if max_num_targets == "":
            max_num_targets = "100"
        self.lines.append("{}self.scheduling.max_num_targets "
                          "= {}".format(PADDING * 2, max_num_targets))
        self.lines.append(os.linesep)
        self.lines.append("{}self.scheduling.accept_serendipity "
                          "= {}".format(PADDING * 2,
                                        params["general_scheduling_accept_serendipity"]))
        self.lines.append(os.linesep)
        self.lines.append("{}self.scheduling.accept_consecutive_visits "
                          "= {}".format(PADDING * 2,
                                        params["general_scheduling_accept_consecutive_visits"]))
        self.lines.append(os.linesep)
        self.lines.append("{}self.scheduling.airmass_bonus = {}"
                          .format(PADDING * 2, str(params["general_scheduling_airmass_bonus"])))
        self.lines.append(os.linesep)
        self.lines.append("{}self.scheduling.restrict_grouped_visits "
                          "= {}".format(PADDING * 2,
                                        params["scheduling_restrict_grouped_visits"]))
        self.lines.append(os.linesep)
        time_interval = self.time_interval_format(str(params["scheduling_time_interval"]))
        if time_interval != 0.0 or eval(time_interval) != 0.0:
            self.lines.append("{}self.scheduling.time_interval "
                              "= {}".format(PADDING * 2, time_interval))
            self.lines.append(os.linesep)
            self.lines.append("{}self.scheduling.time_window_start "
                              "= {}".format(PADDING * 2, params["scheduling_time_window_start"]))
            self.lines.append(os.linesep)
            self.lines.append("{}self.scheduling.time_window_max "
                              "= {}".format(PADDING * 2, params["scheduling_time_window_max"]))
            self.lines.append(os.linesep)
            self.lines.append("{}self.scheduling.time_window_end "
                              "= {}".format(PADDING * 2, params["scheduling_time_window_end"]))
            self.lines.append(os.linesep)
            self.lines.append("{}self.scheduling.time_weight "
                              "= {}".format(PADDING * 2, params["scheduling_time_weight"]))
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
            use_filter = params["general_{}_use".format(field_stem)]
            if use_filter:
                used_filters.append(("{}.name".format(field_stem), field_stem))
                self.lines.append("{}{} = GeneralBandFilter()".format(PADDING * 2, field_stem))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.name = \'{}\'".format(PADDING * 2, field_stem, band_filter))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.num_visits = {}".
                                  format(PADDING * 2, field_stem,
                                         str(params["{}_num_visits".format(field_stem)])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.num_grouped_visits = {}".
                                  format(PADDING * 2, field_stem,
                                         str(params["{}_num_grouped_visits".format(field_stem)])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.bright_limit = {}".
                                  format(PADDING * 2, field_stem,
                                         str(params["general_{}_bright_limit".format(field_stem)])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.dark_limit = {}".
                                  format(PADDING * 2, field_stem,
                                         str(params["general_{}_dark_limit".format(field_stem)])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.max_seeing = {}".
                                  format(PADDING * 2, field_stem,
                                         str(params["general_{}_max_seeing".format(field_stem)])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.exposures = [{}]".
                                  format(PADDING * 2, field_stem,
                                         str(params["general_{}_exposures".
                                                    format(field_stem)]).replace(',', ', ')))
                self.lines.append(os.linesep)

        filters_spec = self.format_dictionaries(used_filters)

        self.lines.append("{}self.filters = {}{}{}".format(PADDING * 2, "{", filters_spec, "}"))
        self.lines.append(os.linesep)
