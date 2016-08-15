import os
import re

from PyQt4 import QtGui

from opsim4.widgets.wizard import ProposalTypePage, SchedulingPage, SkyConstraintsPage, SkyExclusionPage
from opsim4.widgets.wizard import SkyNightlyBoundsPage, SkyRegionPage

__all__ = ["ProposalCreationWizard"]

class ProposalCreationWizard(QtGui.QWizard):
    """Main class for proposal creation wizard.
    """

    def __init__(self, parent=None):
        """Initialize class.

        Parameters
        ----------
        parent : QWidget
            The widget's parent.
        """
        QtGui.QWizard.__init__(self, parent)
        self.save_directory = None
        self.setWindowTitle("Proposal Creation Wizard")

        self.addPage(ProposalTypePage())
        self.addPage(SkyRegionPage())
        self.addPage(SkyExclusionPage())
        self.addPage(SkyNightlyBoundsPage())
        self.addPage(SkyConstraintsPage())
        self.addPage(SchedulingPage())

    def set_save_directory(self, save_dir):
        """Set the save directory to the wizard.

        Parameters
        ----------
        save_dir : str
            The location to add the new proposal to.
        """
        self.save_directory = save_dir

    def accept(self):
        """Process the given information.
        """
        prop_save_dir = os.path.join(self.save_directory, "new_props")
        if not os.path.exists(prop_save_dir):
            os.mkdir(prop_save_dir)

        is_ad = self.field("area_dist_choice").toBool()
        is_td = self.field("time_dep_choice").toBool()
        prop_type = None
        prop_reg_type = None
        if is_ad:
            prop_type = "AreaDistribution"
            prop_reg_type = "area_dist_prop_reg"
        if is_td:
            prop_type = "TimeDependent"
            prop_reg_type = "time_dep_prop_reg"

        full_prop_name = str(self.field("proposal_name").toString())
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
        prop_file_lines.append("\tdef setDefaults(self):")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\tself.name = \"{}\"".format(full_prop_name))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# -------------------------")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# Sky Region specifications")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# -------------------------")
        prop_file_lines.append(os.linesep)

        sky_regions_selections = str(self.field("sky_region_selections").toString()).strip()
        selection_list = []
        for i, sky_region_selection in enumerate(sky_regions_selections.split(os.linesep)):
            selection_obj = "sel{}".format(i)
            selection_list.append("{}: {}".format(i, selection_obj))
            parts = sky_region_selection.split(',')
            prop_file_lines.append("\t{} = Selection()".format(selection_obj))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("\t{}.limit_type = \"{}\"".format(selection_obj, parts[0]))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("\t{}.minimum_limit = {}".format(selection_obj, float(parts[1])))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("\t{}.maximum_limit = {}".format(selection_obj, float(parts[2])))
            prop_file_lines.append(os.linesep)
            try:
                prop_file_lines.append("\t{}.bounds_limit = {}".format(selection_obj, float(parts[3])))
                prop_file_lines.append(os.linesep)
            except IndexError:
                pass

        prop_file_lines.append("\tself.sky_region.selections = {}{}{}".format("{",
                                                                              ", ".join(selection_list),
                                                                              "}"))
        prop_file_lines.append(os.linesep)

        sky_region_combiners = str(self.field("sky_region_combiners").toString())
        if sky_region_combiners != "":
            prop_file_lines.append("\tself.sky_region.combiners = "
                                   "{}".format(sky_region_combiners.split(',')))
            prop_file_lines.append(os.linesep)

        prop_file_lines.append("\t# ----------------------------")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# Sky Exclusion specifications")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# ----------------------------")
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("\tself.sky_exclusion.dec_window "
                               "= {}".format(str(self.field("sky_exclusions_dec_window").toString())))
        prop_file_lines.append(os.linesep)

        sky_exclusion_selections = str(self.field("sky_exclusion_selections").toString()).strip()
        if sky_exclusion_selections != "":
            selection_obj = "excl0"
            parts = sky_exclusion_selections.split(',')
            prop_file_lines.append("\t{} = Selection()".format(selection_obj))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("\t{}.limit_type = \"{}\"".format(selection_obj, parts[0]))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("\t{}.minimum_limit = {}".format(selection_obj, float(parts[1])))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("\t{}.maximum_limit = {}".format(selection_obj, float(parts[2])))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("\t{}.bounds_limit = {}".format(selection_obj, float(parts[3])))
            prop_file_lines.append(os.linesep)
            prop_file_lines.append("\tself.sky_exclusion.selections = {}0: {}{}".format("{", selection_obj,
                                                                                        "}"))
            prop_file_lines.append(os.linesep)

        prop_file_lines.append("\t# ---------------------------------")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# Sky Nightly Bounds specifications")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# ---------------------------------")
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("\tself.sky_nightly_bounds.twilight_boundary = {}"
                               .format(str(self.field("sky_nightly_bounds_twilight_boundary").toString())))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("\tself.sky_nightly_bounds.delta_lst = {}"
                               .format(str(self.field("sky_nightly_bounds_delta_lst").toString())))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("\t# ------------------------------")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# Sky Constraints specifications")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# ------------------------------")
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("\tself.sky_constraints.max_airmass = {}"
                               .format(str(self.field("sky_constraints_max_airmass").toString())))
        prop_file_lines.append(os.linesep)

        prop_file_lines.append("\t# ----------------------")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# Scheduling information")
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\t# ----------------------")
        prop_file_lines.append(os.linesep)

        max_num_targets = str(self.field("scheduling_max_num_targets").toString())
        if max_num_targets == "":
            max_num_targets = "100"
        prop_file_lines.append("\tself.scheduling.max_num_targets "
                               "= {}".format(max_num_targets))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\tself.scheduling.accept_serendipity "
                               "= {}".format(self.field("scheduling_accept_serendipity").toBool()))
        prop_file_lines.append(os.linesep)
        prop_file_lines.append("\tself.scheduling.accept_consecutive_visits "
                               "= {}".format(self.field("scheduling_accept_consecutive_visits").toBool()))
        prop_file_lines.append(os.linesep)

        with open(os.path.join(prop_save_dir, prop_file_name), 'w') as ofile:
            for prop_file_line in prop_file_lines:
                ofile.write(prop_file_line)

        QtGui.QDialog.accept(self)
