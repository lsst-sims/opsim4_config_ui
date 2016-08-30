import unittest

from lsst.sims.ocs.configuration import Downtime

from lsst.sims.opsim4.model import DowntimeModel

class DowntimeModelTest(unittest.TestCase):

    def setUp(self):
        self.model = DowntimeModel()

    def test_basic_information_after_creation(self):
        self.assertIsInstance(self.model.config_obj, Downtime)
        self.assertEqual(len(self.model.params), 3)
