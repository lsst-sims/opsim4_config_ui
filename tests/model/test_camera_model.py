import unittest

from lsst.sims.ocs.configuration.instrument import Camera
from opsim4.model import CameraModel

class CameraModelTest(unittest.TestCase):

    def setUp(self):
        self.model = CameraModel()

    def test_basic_information_after_creation(self):
        self.assertIsInstance(self.model.config_obj, Camera)
        self.assertEqual(len(self.model.params), 8)
