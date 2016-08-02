import unittest

from lsst.sims.ocs.configuration.instrument import Telescope
from opsim4.model import TelescopeModel

class TelescopeModelTest(unittest.TestCase):

    def setUp(self):
        self.model = TelescopeModel()

    def test_basic_information_after_creation(self):
        self.assertTrue(isinstance(self.model.config_obj, Telescope))
        self.assertEqual(len(self.model.params), 11)
        #print(self.model.params)
