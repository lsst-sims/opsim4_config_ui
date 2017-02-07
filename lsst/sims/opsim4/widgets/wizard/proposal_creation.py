import os
import re

from PyQt5 import QtGui, QtWidgets

from lsst.sims.opsim4.widgets.wizard import BandFiltersPage, MasterSubSequencesPage, ProposalTypePage
from lsst.sims.opsim4.widgets.wizard import SchedulingPage
from lsst.sims.opsim4.widgets.wizard import SkyConstraintsPage, SkyExclusionPage
from lsst.sims.opsim4.widgets.wizard import SkyNightlyBoundsPage, SkyRegionPage, SkyUserRegionsPage
from lsst.sims.opsim4.widgets.wizard import SubSequencesPage, WizardPages
from lsst.sims.opsim4.widgets.wizard import GeneralWriter, SequenceWriter
from lsst.sims.opsim4.widgets.wizard import band_filters_params, master_sub_sequences_params
from lsst.sims.opsim4.widgets.wizard import nested_sub_sequences_params, scheduling_params
from lsst.sims.opsim4.widgets.wizard import sky_constraints_params
from lsst.sims.opsim4.widgets.wizard import sky_exclusion_params
from lsst.sims.opsim4.widgets.wizard import sky_nightly_bounds_params
from lsst.sims.opsim4.widgets.wizard import sky_region_params, sky_user_regions_params
from lsst.sims.opsim4.widgets.wizard import sub_sequences_params

__all__ = ["ProposalCreationWizard"]

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

        self.setPage(WizardPages.PageProposalType, ProposalTypePage())
        self.setPage(WizardPages.PageSkyRegions, SkyRegionPage())
        self.setPage(WizardPages.PageSkyUserRegions, SkyUserRegionsPage())
        self.setPage(WizardPages.PageGeneralSkyExclusions, SkyExclusionPage())
        self.setPage(WizardPages.PageSequenceSkyExclusions, SkyExclusionPage(is_general=False))
        self.setPage(WizardPages.PageSkyNightlyBounds, SkyNightlyBoundsPage())
        self.setPage(WizardPages.PageSkyConstraints, SkyConstraintsPage())
        self.setPage(WizardPages.PageSubSequences, SubSequencesPage())
        self.setPage(WizardPages.PageMasterSubSequences, MasterSubSequencesPage())
        self.setPage(WizardPages.PageNestedSubSequences, SubSequencesPage(is_nested=True))
        self.setPage(WizardPages.PageGeneralScheduling, SchedulingPage())
        self.setPage(WizardPages.PageSequenceScheduling, SchedulingPage(is_general=False))
        self.setPage(WizardPages.PageGeneralFilters, BandFiltersPage())
        self.setPage(WizardPages.PageSequenceFilters, BandFiltersPage(is_general=False))

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

        is_general = self.field("general_choice")
        is_subseq = self.field("sequence_choice")
        prop_type = None
        prop_reg_type = None
        if is_general:
            prop_type = "General"
            prop_reg_type = "general_prop_reg"
        if is_subseq:
            prop_type = "Sequence"
            prop_reg_type = "sequence_prop_reg"

        full_prop_name = self.field("proposal_name")
        m = re.compile(r'[A-Z][^A-Z]+')
        name_parts = [x.lower() for x in m.findall(full_prop_name)]
        prop_file_name = "{}.py".format("_".join(name_parts))

        file_def_dict = {"full_prop_name": full_prop_name,
                         "prop_type": prop_type,
                         "prop_reg_type": prop_reg_type}

        writer = None
        if is_general:
            writer = GeneralWriter()
            writer.file_def(file_def_dict)
            pdict = self.create_field_parameters(sky_region_params())
            writer.sky_regions(pdict)
            pdict = self.create_field_parameters(sky_exclusion_params())
            writer.sky_exclusions(pdict)
            pdict = self.create_field_parameters(sky_nightly_bounds_params())
            writer.sky_nightly_bounds(pdict)
            pdict = self.create_field_parameters(sky_constraints_params())
            writer.sky_constraints(pdict)
            pdict = self.create_field_parameters(scheduling_params())
            writer.scheduling(pdict)
            pdict = self.create_field_parameters(band_filters_params())
            writer.band_filters(pdict)
        if is_subseq:
            writer = SequenceWriter()
            writer.file_def(file_def_dict)
            pdict = self.create_field_parameters(sky_user_regions_params())
            writer.sky_user_regions(pdict)
            pdict = self.create_field_parameters(sky_exclusion_params(False))
            writer.sky_exclusions(pdict)
            pdict = self.create_field_parameters(sky_nightly_bounds_params())
            writer.sky_nightly_bounds(pdict)
            pdict = self.create_field_parameters(sky_constraints_params())
            writer.sky_constraints(pdict)
            pdict = self.create_field_parameters(sub_sequences_params())
            writer.sub_sequences(pdict)
            pdict = self.create_field_parameters(master_sub_sequences_params())
            pdict1 = self.create_field_parameters(nested_sub_sequences_params())
            writer.master_sub_sequences(pdict, pdict1)
            pdict = self.create_field_parameters(scheduling_params(False))
            writer.scheduling(pdict)
            pdict = self.create_field_parameters(band_filters_params(False))
            writer.band_filters(pdict)

        prop_file_lines = writer.lines

        with open(os.path.join(prop_save_dir, prop_file_name), 'w') as ofile:
            for prop_file_line in prop_file_lines:
                ofile.write(prop_file_line)

        QtWidgets.QDialog.accept(self)

    def create_field_parameters(self, param_list):
        """Create parameter dictionary from registered fields.

        Parameters
        ----------
        param_list : list
            The names of the registered fields.

        Returns
        -------
        dict
            The parameter dictionary.
        """
        parameter_dict = {}
        for param in param_list:
            parameter_dict[param] = self.field(param)
        return parameter_dict
