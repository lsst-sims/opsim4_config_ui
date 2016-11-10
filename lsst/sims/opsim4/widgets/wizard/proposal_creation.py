import os
import re

from PyQt5 import QtGui, QtWidgets

from lsst.sims.opsim4.widgets.wizard import BandFiltersPage, ProposalTypePage, SchedulingPage
from lsst.sims.opsim4.widgets.wizard import SkyConstraintsPage
from lsst.sims.opsim4.widgets.wizard import SkyExclusionPage, SkyNightlyBoundsPage, SkyRegionPage

__all__ = ["ProposalCreationWizard"]

PADDING = "    "

class ProposalCreationWizard(QtWidgets.QWizard):
    """Main class for proposal creation wizard.
    """

    def __init__(self, parent=None):
        """Initialize class.

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtWidgets.QWizard.__init__(self, parent)
        self.save_directory = None
        self.setWindowTitle("Proposal Creation Wizard")
        self.setWizardStyle(QtWidgets.QWizard.MacStyle)
        self.setPixmap(QtWidgets.QWizard.BackgroundPixmap, QtGui.QPixmap(":/skymap.png"))

        self.addPage(ProposalTypePage())
        self.addPage(SkyRegionPage())
        self.addPage(SkyExclusionPage())
        self.addPage(SkyNightlyBoundsPage())
        self.addPage(SkyConstraintsPage())
        self.addPage(SchedulingPage())
        self.addPage(BandFiltersPage())

    def set_save_directory(self, save_dir):
        """Set the save directory to the wizard.

        Parameters
        ----------
        save_dir : str
            The location to add the new proposal to.
        """
        if save_dir is None:
            save_dir = os.curdir
        self.save_directory = save_dir

    def accept(self):
        """Process the given information.
        """
        prop_save_dir = os.path.join(str(self.save_directory), "new_props")
        if not os.path.exists(prop_save_dir):
            os.mkdir(prop_save_dir)

        is_ad = self.field("area_dist_choice")
        is_td = self.field("time_dep_choice")
        prop_type = None
        prop_reg_type = None
        if is_ad:
            prop_type = "AreaDistribution"
            prop_reg_type = "area_dist_prop_reg"
        if is_td:
            prop_type = "TimeDependent"
            prop_reg_type = "time_dep_prop_reg"

        full_prop_name = self.field("proposal_name")
        m = re.compile(r'[A-Z][^A-Z]+')
        name_parts = [x.lower() for x in m.findall(full_prop_name)]
        prop_file_name = "{}.py".format("_".join(name_parts))

        prop_file_lines = []
        prop_file_lines.append("import lsst.pex.config as pexConfig")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("from lsst.sims.ocs.configuration.proposal import {}, BandFilter, "
                               "Selection".format(prop_type))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("from lsst.sims.ocs.configuration.proposal import {}, "
                               "SELECTION_LIMIT_TYPES".format(prop_reg_type))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("__all__ = [\"{}\"]".format(full_prop_name))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("@pexConfig.registerConfig(\"{}\", {}, {})".format(full_prop_name,
                                                                                  prop_reg_type, prop_type))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("class {}({}):".format(full_prop_name, prop_type))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}def setDefaults(self):".format(PADDING))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}self.name = \"{}\"".format(PADDING * 2, full_prop_name))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# -------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# Sky Region specifications".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# -------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)

        sky_regions_selections = str(self.field("sky_region_selections")).strip()
        selection_list = []
        for i, sky_region_selection in enumerate(sky_regions_selections.split(os.linesep)):
            selection_obj = "sel{}".format(i)
            selection_list.append("{}: {}".format(i, selection_obj))
            parts = sky_region_selection.split(',')
            prop_file_lines.append("{}{} = Selection()".format(PADDING * 2, selection_obj))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("{}{}.limit_type = \"{}\"".format(PADDING * 2, selection_obj, parts[0]))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("{}{}.minimum_limit = {}".format(PADDING * 2, selection_obj,
                                                                    float(parts[1])))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("{}{}.maximum_limit = {}".format(PADDING * 2, selection_obj,
                                                                    float(parts[2])))
            prop_file_lines.append(os.linesep)
            try:
                prop_file_lines.append("{}{}.bounds_limit = {}".format(PADDING * 2, selection_obj,
                                                                       float(parts[3])))
                prop_file_lines.append(os.linesep)
            except IndexError:
                pass

        prop_file_lines.append("{}self.sky_region.selections = {}{}{}".format(PADDING * 2, "{",
                                                                              ", ".join(selection_list),
                                                                              "}"))
        prop_file_lines.append(os.linesep)

        sky_region_combiners = str(self.field("sky_region_combiners"))
        if sky_region_combiners != "":
            prop_file_lines.append("{}self.sky_region.combiners = "
                                   "{}".format(PADDING * 2, sky_region_combiners.split(',')))
            prop_file_lines.append(os.linesep)

        prop_file_lines.append("{}# ----------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# Sky Exclusion specifications".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# ----------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("{}self.sky_exclusion.dec_window "
                               "= {}".format(PADDING * 2,
                                             str(self.field("sky_exclusions_dec_window"))))
        prop_file_lines.append(os.linesep)

        sky_exclusion_selections = str(self.field("sky_exclusion_selections")).strip()
        if sky_exclusion_selections != "":
            selection_obj = "excl0"
            parts = sky_exclusion_selections.split(',')
            prop_file_lines.append("{}{} = Selection()".format(PADDING * 2, selection_obj))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("{}{}.limit_type = \"{}\"".format(PADDING * 2, selection_obj, parts[0]))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("{}{}.minimum_limit = {}".format(PADDING * 2, selection_obj,
                                                                    float(parts[1])))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("{}{}.maximum_limit = {}".format(PADDING * 2, selection_obj,
                                                                    float(parts[2])))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("{}{}.bounds_limit = {}".format(PADDING * 2, selection_obj,
                                                                   float(parts[3])))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("{}self.sky_exclusion.selections = {}0: {}{}".format(PADDING * 2, "{",
                                                                                        selection_obj,
                                                                                        "}"))
            prop_file_lines.append(os.linesep)

        prop_file_lines.append("{}# ---------------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# Sky Nightly Bounds specifications".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# ---------------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("{}self.sky_nightly_bounds.twilight_boundary = {}"
                               .format(PADDING * 2, str(self.field("sky_nightly_bounds_twilight_boundary"))))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("{}self.sky_nightly_bounds.delta_lst = {}"
                               .format(PADDING * 2, str(self.field("sky_nightly_bounds_delta_lst"))))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("{}# ------------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# Sky Constraints specifications".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# ------------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("{}self.sky_constraints.max_airmass = {}"
                               .format(PADDING * 2,
                                       str(self.field("sky_constraints_max_airmass"))))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}self.sky_constraints.max_cloud = {}"
                               .format(PADDING * 2, str(self.field("sky_constraints_max_cloud"))))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("{}# ----------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# Scheduling information".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# ----------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)

        max_num_targets = str(self.field("scheduling_max_num_targets"))
        if max_num_targets == "":
            max_num_targets = "100"
        prop_file_lines.append("{}self.scheduling.max_num_targets "
                               "= {}".format(PADDING * 2, max_num_targets))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}self.scheduling.accept_serendipity "
                               "= {}".format(PADDING * 2,
                                             self.field("scheduling_accept_serendipity")))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}self.scheduling.accept_consecutive_visits "
                               "= {}".format(PADDING * 2,
                                             self.field("scheduling_accept_consecutive_visits")))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}self.scheduling.airmass_bonus = {}"
                               .format(PADDING * 2, str(self.field("scheduling_airmass_bonus"))))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("{}# --------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# Band Filter specifications".format(PADDING * 2))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("{}# --------------------------".format(PADDING * 2))
        prop_file_lines.append(os.linesep)

        used_filters = []
        for band_filter in "u,g,r,i,z,y".split(','):
            field_stem = "{}_filter".format(band_filter)
            use_filter = self.field("{}_use".format(field_stem))
            if use_filter:
                used_filters.append(("{}.name".format(field_stem), field_stem))
                prop_file_lines.append("{}{} = BandFilter()".format(PADDING * 2, field_stem))
                prop_file_lines.append(os.linesep)
                prop_file_lines.append("{}{}.name = \'{}\'".format(PADDING * 2, field_stem, band_filter))
                prop_file_lines.append(os.linesep)
                prop_file_lines.append("{}{}.num_visits = {}".format(PADDING * 2, field_stem,
                                       str(self.field("{}_num_visits".format(field_stem)))))
                prop_file_lines.append(os.linesep)
                prop_file_lines.append("{}{}.bright_limit = {}".format(PADDING * 2, field_stem,
                                       str(self.field("{}_bright_limit".format(field_stem)))))
                prop_file_lines.append(os.linesep)
                prop_file_lines.append("{}{}.dark_limit = {}".format(PADDING * 2, field_stem,
                                       str(self.field("{}_dark_limit".format(field_stem)))))
                prop_file_lines.append(os.linesep)
                prop_file_lines.append("{}{}.max_seeing = {}".format(PADDING * 2, field_stem,
                                       str(self.field("{}_max_seeing".format(field_stem)))))
                prop_file_lines.append(os.linesep)
                prop_file_lines.append("{}{}.exposures = [{}]".format(PADDING * 2, field_stem,
                                       str(self.field("{}_exposures".format(field_stem)))))
                prop_file_lines.append(os.linesep)

        filters = []
        for i, used_filter in enumerate(used_filters):
            if i != 0:
                line_padding = PADDING * 6
            else:
                line_padding = ""
            filters.append("{}{}: {},".format(line_padding, used_filter[0], used_filter[1]))

        filters[-1] = filters[-1].strip(',')
        filters_spec = os.linesep.join(filters)

        prop_file_lines.append("{}self.filters = {}{}{}".format(PADDING * 2, "{", filters_spec, "}"))

        with open(os.path.join(prop_save_dir, prop_file_name), 'w') as ofile:
            for prop_file_line in prop_file_lines:
                ofile.write(prop_file_line)

        QtWidgets.QDialog.accept(self)
