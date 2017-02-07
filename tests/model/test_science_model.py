import unittest

from lsst.sims.opsim4.model import ScienceModel

class ScienceModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ScienceModel()
        self.num_general_proposals = 4
        self.num_sequence_proposals = 1

    def test_basic_information_after_creation(self):
        self.assertEqual(len(self.model.get_proposal_names()),
                         self.num_general_proposals + self.num_sequence_proposals)
        general_params = self.model.general_params
        self.assertEqual(len(general_params), self.num_general_proposals)
        self.assertEqual(len(general_params[general_params.keys()[0]]), 7)
        sequence_params = self.model.sequence_params
        self.assertEqual(len(sequence_params), self.num_sequence_proposals)
        self.assertEqual(len(sequence_params[sequence_params.keys()[0]]), 9)

        for k, v in self.model.general_params.items():
            if k == "SouthCelestialPole":
                self.assertIsNotNone(v["sky_exclusion"])
                self.assertIsNotNone(v["filters"]["value"]["u"])

        for k, v in self.model.general_modules.items():
            if k == "SouthCelestialPole":
                self.assertEqual(v, "lsst.sims.ocs.configuration.science.south_celestial_pole")

        for k, v in self.model.sequence_modules.items():
            if k == "DeepDrillingCosmology1":
                self.assertEqual(v, "lsst.sims.ocs.configuration.science.deep_drilling_cosmology1")
