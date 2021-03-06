import unittest

from lsst.sims.ocs.configuration.instrument import Park

from lsst.sims.opsim4.model import ParkModel

class ParkModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ParkModel()

    def test_basic_information_after_creation(self):
        self.assertIsInstance(self.model.config_obj, Park)
        self.assertEqual(len(self.model.params), 6)
