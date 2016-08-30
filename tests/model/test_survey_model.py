import unittest

from lsst.sims.ocs.configuration import Survey

from lsst.sims.opsim4.model import SurveyModel

class SurveyModelTest(unittest.TestCase):

    def setUp(self):
        self.model = SurveyModel()

    def test_basic_information_after_creation(self):
        self.assertIsInstance(self.model.config_obj, Survey)
        self.assertEqual(len(self.model.params), 5)
        self.assertEqual(len(self.model.proposals), 1)
        self.assertEqual(len(self.model.proposals["AD"]), 3)

    def test_is_proposal_active(self):
        self.assertTrue(self.model.is_proposal_active("GalacticPlane"))
        self.assertFalse(self.model.is_proposal_active("TestTheProp"))

    def test_get_parameters(self):
        self.assertEqual(len(self.model.get_parameter("survey/ad_proposals")), 3)
