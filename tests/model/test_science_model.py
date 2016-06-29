import unittest

from opsim4.model import ScienceModel

class ScienceModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ScienceModel()
        self.num_proposals = 3

    def test_basic_information_after_creation(self):
        ad_params = self.model.ad_params
        self.assertEqual(len(ad_params), self.num_proposals)
        self.assertEqual(len(ad_params[ad_params.keys()[0]]), 7)
        self.assertEqual(len(self.model.get_proposal_names()), self.num_proposals)
