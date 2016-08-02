import unittest

from lsst.sims.ocs.configuration.instrument import Park
from opsim4.model import ParkModel

class ParkModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ParkModel()

    def test_basic_information_after_creation(self):
        self.assertTrue(isinstance(self.model.config_obj, Park))
        self.assertEqual(len(self.model.params), 6)
        #print(self.model.params)
