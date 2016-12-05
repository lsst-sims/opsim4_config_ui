import unittest

from lsst.sims.opsim4.model import ScienceModel

class ScienceModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ScienceModel()
        self.num_proposals = 4

    def test_basic_information_after_creation(self):
        gen_params = self.model.gen_params
        self.assertEqual(len(gen_params), self.num_proposals)
        self.assertEqual(len(gen_params[gen_params.keys()[0]]), 7)
        self.assertEqual(len(self.model.get_proposal_names()), self.num_proposals)

        for k, v in self.model.gen_params.items():
            if k == "SouthCelestialPole":
                self.assertIsNotNone(v["sky_exclusion"])

        for k, v in self.model.gen_modules.items():
            if k == "SouthCelestialPole":
                self.assertEqual(v, "lsst.sims.ocs.configuration.science.south_celestial_pole")
