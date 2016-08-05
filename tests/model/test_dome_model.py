import unittest

from lsst.sims.ocs.configuration.instrument import Dome
from opsim4.model import DomeModel

class DomeModelTest(unittest.TestCase):

    def setUp(self):
        self.model = DomeModel()

    def test_basic_information_after_creation(self):
        self.assertTrue(isinstance(self.model.config_obj, Dome))
        self.assertEqual(len(self.model.params), 7)
