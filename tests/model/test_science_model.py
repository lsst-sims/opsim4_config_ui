import unittest

from lsst.sims.opsim4.model import ScienceModel

class ScienceModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ScienceModel()
        self.num_proposals = 3

    def test_basic_information_after_creation(self):
        ad_params = self.model.ad_params
        self.assertEqual(len(ad_params), self.num_proposals)
        self.assertEqual(len(ad_params[ad_params.keys()[0]]), 7)
        self.assertEqual(len(self.model.get_proposal_names()), self.num_proposals)

        for k, v in self.model.ad_params.items():
            if k == "SouthCelestialPole":
                self.assertIsNotNone(v["sky_exclusion"])

        for k, v in self.model.ad_modules.items():
            if k == "SouthCelestialPole":
                self.assertEqual(v, "lsst.sims.ocs.configuration.science.south_celestial_pole")
