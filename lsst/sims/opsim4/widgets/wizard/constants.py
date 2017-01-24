from enum import IntEnum

__all__ = ["WizardPages"]

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
    PageGeneralScheduling = 10,
    PageSequenceScheduling = 11,
    PageGeneralFilters = 12,
    PageSequenceFilters = 13

