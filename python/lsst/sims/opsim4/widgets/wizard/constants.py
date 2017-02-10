from enum import IntEnum

__all__ = ["WizardPages", "PADDING"]

PADDING = "    "

class WizardPages(IntEnum):
    """Page numbers of the pick-a-path proposal creation.
    """
    PageProposalType = 1,
    PageSkyRegions = 2,
    PageSkyUserRegions = 3,
    PageGeneralSkyExclusions = 4,
    PageSequenceSkyExclusions = 5,
    PageSkyNightlyBounds = 6,
    PageSkyConstraints = 7,
    PageSubSequences = 8,
    PageMasterSubSequences = 9,
    PageNestedSubSequences = 10,
    PageGeneralScheduling = 11,
    PageSequenceScheduling = 12,
    PageGeneralFilters = 13,
    PageSequenceFilters = 14
