import unittest

from lsst.sims.ocs.configuration.instrument import ObservatoryVariation

from lsst.sims.opsim4.model import ObservatoryVariationModel

class ObservatoryVariationModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ObservatoryVariationModel()

    def test_basic_information_after_creation(self):
        self.assertIsInstance(self.model.config_obj, ObservatoryVariation)
        self.assertEqual(len(self.model.params), 3)
