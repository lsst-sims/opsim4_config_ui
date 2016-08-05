import unittest

from lsst.sims.ocs.configuration import SchedulerDriver
from opsim4.model import SchedulerDriverModel

class SchedulerDriverModelTest(unittest.TestCase):

    def setUp(self):
        self.model = SchedulerDriverModel()

    def test_basic_information_after_creation(self):
        self.assertTrue(isinstance(self.model.config_obj, SchedulerDriver))
        self.assertEqual(len(self.model.params), 5)
