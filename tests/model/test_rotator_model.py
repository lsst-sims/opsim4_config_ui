import unittest

from lsst.sims.ocs.configuration.instrument import Rotator
from opsim4.model import RotatorModel

class RotatorModelTest(unittest.TestCase):

    def setUp(self):
        self.model = RotatorModel()

    def test_basic_information_after_creation(self):
        self.assertTrue(isinstance(self.model.config_obj, Rotator))
        self.assertEqual(len(self.model.params), 8)
