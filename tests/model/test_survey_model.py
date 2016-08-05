import unittest

from lsst.sims.ocs.configuration import Survey
from opsim4.model import SurveyModel

class SurveyModelTest(unittest.TestCase):

    def setUp(self):
        self.model = SurveyModel()

    def test_basic_information_after_creation(self):
        self.assertTrue(isinstance(self.model.config_obj, Survey))
        self.assertEqual(len(self.model.params), 5)
