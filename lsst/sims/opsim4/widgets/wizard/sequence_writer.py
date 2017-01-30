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

    def sub_sequences(self, params):
        """Create the sub-sequence information.

        Parameters
        ----------
        params : dict
            The information for the sub-sequence.
        """
        sub_sequences = str(params["sub_sequences"]).strip().split(os.linesep)
        if sub_sequences[0] == '':
            sub_sequences = []
        if len(sub_sequences):
            self.lines.append("{}# --------------------------".format(PADDING * 2))
            self.lines.append(os.linesep)
            self.lines.append("{}# Sub-sequence specification".format(PADDING * 2))
            self.lines.append(os.linesep)
            self.lines.append("{}# --------------------------".format(PADDING * 2))
            self.lines.append(os.linesep)

            self.lines[2] += ", SubSequence"
            sub_sequence_list = []
            for i, sub_sequence in enumerate(sub_sequences):
                sub_sequence_obj = "sseq{}".format(i)
                sub_sequence_list.append((str(i), sub_sequence_obj))
                parts = sub_sequence.split(',')
                self.lines.append("{}{} = SubSequence()".format(PADDING * 2, sub_sequence_obj))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.name = \"{}\"".format(PADDING * 2, sub_sequence_obj, parts[0]))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.filters = [{}]".format(PADDING * 2, sub_sequence_obj,
                                                               self.reformat_string(parts[1])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.visits_per_filter = [{}]".format(PADDING * 2, sub_sequence_obj,
                                                                         self.reformat_string(parts[2])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.num_events = {}".format(PADDING * 2, sub_sequence_obj,
                                                                int(parts[3])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.num_max_missed = {}".format(PADDING * 2, sub_sequence_obj,
                                                                    int(parts[4])))
                self.lines.append(os.linesep)
                math_ops = "+,-,*,/".split(',')
                check_math = [op for op in math_ops if op in parts[5]]
                if len(check_math):
                    time_interval = parts[5]
                else:
                    time_interval = float(parts[5])
                self.lines.append("{}{}.time_interval = {}".format(PADDING * 2, sub_sequence_obj,
                                                                   time_interval))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.time_window_start = {}".format(PADDING * 2, sub_sequence_obj,
                                                                       float(parts[6])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.time_window_max = {}".format(PADDING * 2, sub_sequence_obj,
                                                                     float(parts[7])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.time_window_end = {}".format(PADDING * 2, sub_sequence_obj,
                                                                     float(parts[8])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.time_weight = {}".format(PADDING * 2, sub_sequence_obj,
                                                                 float(parts[9])))
                self.lines.append(os.linesep)

            sub_sequence_spec = self.format_dictionaries(sub_sequence_list,
                                                         padding_size=PADDING * 7 + "  ")
            self.lines.append("{}self.sub_sequences = {}{}{}".format(PADDING * 2, "{",
                                                                     sub_sequence_spec, "}"))
            self.lines.append(os.linesep)

    def master_sub_sequences(self, params, params2):
        """Create the master sub-sequence information.

        Parameters
        ----------
        params : dict
            The information for the master sub-sequences.
        params2 : dict
            The information for the nested sub-sequences.
        """
        msub_sequences = str(params["master_sub_sequences"]).strip().split(os.linesep)
        nsub_sequences = str(params2["nested_sub_sequences"]).strip().split(os.linesep)
        if msub_sequences[0] == '':
            msub_sequences = []
        if len(msub_sequences):
            self.lines.append("{}# ---------------------------------------------".format(PADDING * 2))
            self.lines.append(os.linesep)
            self.lines.append("{}# Master and Nested Sub-sequence specifications".format(PADDING * 2))
            self.lines.append(os.linesep)
            self.lines.append("{}# ---------------------------------------------".format(PADDING * 2))
            self.lines.append(os.linesep)

            nsub_sequence_count = 0
            self.lines[2] += ", MasterSubSequence"
            if ", SubSequence" not in self.lines[2]:
                self.lines[2] += ", SubSequence"
            msub_sequence_list = []
            for i, msub_sequence in enumerate(msub_sequences):
                msub_sequence_obj = "msseq{}".format(i)
                msub_sequence_list.append((str(i), msub_sequence_obj))
                parts = msub_sequence.split(',')
                self.lines.append("{}{} = MasterSubSequence()".format(PADDING * 2, msub_sequence_obj))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.name = \"{}\"".format(PADDING * 2, msub_sequence_obj, parts[0]))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.num_events = {}".format(PADDING * 2, msub_sequence_obj,
                                                                int(parts[2])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.num_max_missed = {}".format(PADDING * 2, msub_sequence_obj,
                                                                    int(parts[3])))
                self.lines.append(os.linesep)
                time_interval = self.time_interval_format(parts[4])
                self.lines.append("{}{}.time_interval = {}".format(PADDING * 2, msub_sequence_obj,
                                                                   time_interval))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.time_window_start = {}".format(PADDING * 2, msub_sequence_obj,
                                                                       float(parts[5])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.time_window_max = {}".format(PADDING * 2, msub_sequence_obj,
                                                                     float(parts[6])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.time_window_end = {}".format(PADDING * 2, msub_sequence_obj,
                                                                     float(parts[7])))
                self.lines.append(os.linesep)
                self.lines.append("{}{}.time_weight = {}".format(PADDING * 2, msub_sequence_obj,
                                                                 float(parts[8])))
                self.lines.append(os.linesep)

                # Handle nested sub-sequences
                nsub_sequence_names = self.reformat_string(parts[1]).split(',')
                nsub_sequence_list = []
                nsub_sequence_index = 0
                for nsub_sequence in nsub_sequences:
                    nparts = nsub_sequence.split(',')
                    if nparts[0] in nsub_sequence_names:
                        nsub_sequence_obj = "sseq{}".format(nsub_sequence_count)
                        nsub_sequence_list.append((str(nsub_sequence_index), nsub_sequence_obj))
                        nsub_sequence_index += 1

                        self.lines.append("{}{} = SubSequence()".format(PADDING * 2, nsub_sequence_obj))
                        self.lines.append(os.linesep)
                        self.lines.append("{}{}.name = \"{}\"".format(PADDING * 2, nsub_sequence_obj,
                                                                      nparts[0]))
                        self.lines.append(os.linesep)
                        self.lines.append("{}{}.filters = [{}]".format(PADDING * 2, nsub_sequence_obj,
                                                                       self.reformat_string(nparts[1])))
                        self.lines.append(os.linesep)
                        self.lines.append("{}{}.visits_per_filter = [{}]".
                                          format(PADDING * 2, nsub_sequence_obj,
                                                 self.reformat_string(nparts[2])))
                        self.lines.append(os.linesep)
                        self.lines.append("{}{}.num_events = {}".format(PADDING * 2, nsub_sequence_obj,
                                                                        int(nparts[3])))
                        self.lines.append(os.linesep)
                        self.lines.append("{}{}.num_max_missed = {}".format(PADDING * 2, nsub_sequence_obj,
                                                                            int(nparts[4])))
                        self.lines.append(os.linesep)

                        time_interval = self.time_interval_format(nparts[5])
                        self.lines.append("{}{}.time_interval = {}".format(PADDING * 2, nsub_sequence_obj,
                                                                           time_interval))
                        self.lines.append(os.linesep)
                        self.lines.append("{}{}.time_window_start = {}".format(PADDING * 2, nsub_sequence_obj,
                                                                               float(nparts[6])))
                        self.lines.append(os.linesep)
                        self.lines.append("{}{}.time_window_max = {}".format(PADDING * 2, nsub_sequence_obj,
                                                                             float(nparts[7])))
                        self.lines.append(os.linesep)
                        self.lines.append("{}{}.time_window_end = {}".format(PADDING * 2, nsub_sequence_obj,
                                                                             float(nparts[8])))
                        self.lines.append(os.linesep)
                        self.lines.append("{}{}.time_weight = {}".format(PADDING * 2, nsub_sequence_obj,
                                                                         float(nparts[9])))
                        self.lines.append(os.linesep)
                        nsub_sequence_count += 1
                    else:
                        continue

                nsub_sequence_spec = self.format_dictionaries(nsub_sequence_list,
                                                              padding_size=PADDING * 8)
                self.lines.append("{}{}.sub_sequences = {}{}{}".format(PADDING * 2, msub_sequence_obj,
                                                                       "{",
                                                                       nsub_sequence_spec, "}"))
                self.lines.append(os.linesep)

            msub_sequence_spec = self.format_dictionaries(msub_sequence_list,
                                                          padding_size=PADDING * 9 + " ")
            self.lines.append("{}self.master_sub_sequences = {}{}{}".format(PADDING * 2, "{",
                                                                            msub_sequence_spec, "}"))
            self.lines.append(os.linesep)

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

    def reformat_string(self, istr):
        """Convert a parentheses str into a comma-delimited str.

        This function takes a string like: (a b c d) and formats it to
        a string like: a,b,c,d.

        Parameters
        ----------
        istr : str
            The string to reformat.

        Returns
        -------
        str
            The formatted string.
        """
        return ",".join(istr.strip('(').strip(')').split(' '))

    def time_interval_format(self, ti):
        """Handle time interval as formula or number.

        Parameters
        ----------
        ti : str
            The time interval as a string.

        Returns
        -------
        str
            The appropriately formatted time interval.
        """
        math_ops = "+,-,*,/".split(',')
        check_math = [op for op in math_ops if op in ti]
        if len(check_math):
            time_interval_format = ti
        else:
            time_interval_format = float(ti)
        return time_interval_format
