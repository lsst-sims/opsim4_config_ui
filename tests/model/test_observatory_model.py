import unittest

from opsim4.model import ObservatoryModel

class ObservatoryModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ObservatoryModel()

    def test_basic_information_after_creation(self):
        self.assertEqual(len(self.model.params), 8)
