import unittest

from lsst.sims.ocs.configuration import ObservingSite
from opsim4.model import ObservingSiteModel

class SurveyModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ObservingSiteModel()

    def test_basic_information_after_creation(self):
        self.assertTrue(isinstance(self.model.config_obj, ObservingSite))
        self.assertEqual(len(self.model.params), 7)
