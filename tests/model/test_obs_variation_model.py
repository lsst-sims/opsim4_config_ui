import unittest

from lsst.sims.ocs.configuration.instrument import ObservatoryVariation
from opsim4.model import ObservatoryVariationModel

class ObservatoryVariationModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ObservatoryVariationModel()

    def test_basic_information_after_creation(self):
        self.assertTrue(isinstance(self.model.config_obj, ObservatoryVariation))
        self.assertEqual(len(self.model.params), 3)
        #print(self.model.params)
