import unittest

from lsst.sims.ocs.configuration.instrument import Filters

from lsst.sims.opsim4.model import FiltersModel

class FiltersModelTest(unittest.TestCase):

    def setUp(self):
        self.model = FiltersModel()

    def test_basic_information_after_creation(self):
        self.assertIsInstance(self.model.config_obj, Filters)
        self.assertEqual(len(self.model.params), 6)
