import unittest

from opsim4.model import ScienceModel

class ScienceModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ScienceModel()
        self.num_proposals = 3

    def test_basic_information_after_creation(self):
        self.assertEqual(len(self.model.ad_params), self.num_proposals)
        self.assertEqual(len(self.model.get_proposal_names()), self.num_proposals)
