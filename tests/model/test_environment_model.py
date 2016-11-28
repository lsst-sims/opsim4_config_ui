import unittest

from lsst.sims.ocs.configuration import Environment

from lsst.sims.opsim4.model import EnvironmentModel

class EnvironmentModelTest(unittest.TestCase):

    def setUp(self):
        self.model = EnvironmentModel()

    def test_basic_information_after_creation(self):
        self.assertIsInstance(self.model.config_obj, Environment)
        self.assertEqual(len(self.model.params), 7)
