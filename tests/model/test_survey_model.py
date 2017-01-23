import unittest

from lsst.sims.ocs.configuration import Survey

from lsst.sims.opsim4.model import SurveyModel

class SurveyModelTest(unittest.TestCase):

    def setUp(self):
        self.model = SurveyModel()
        self.num_general_proposals = 4
        self.num_sequence_proposals = 1

    def test_basic_information_after_creation(self):
        self.assertIsInstance(self.model.config_obj, Survey)
        self.assertEqual(len(self.model.params), 6)
        self.assertEqual(len(self.model.proposals), 2)
        self.assertEqual(len(self.model.proposals["GEN"]), self.num_general_proposals)
        self.assertEqual(len(self.model.proposals["SEQ"]), self.num_sequence_proposals)

    def test_is_proposal_active(self):
        self.assertTrue(self.model.is_proposal_active("GalacticPlane"))
        self.assertTrue(self.model.is_proposal_active("DeepDrillingCosmology1"))
        self.assertFalse(self.model.is_proposal_active("TestTheProp"))

    def test_get_parameters(self):
        self.assertEqual(len(self.model.get_parameter("survey/general_proposals")),
                         self.num_general_proposals)
        self.assertEqual(len(self.model.get_parameter("survey/sequence_proposals")),
                         self.num_sequence_proposals)
