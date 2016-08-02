import unittest

from lsst.sims.ocs.configuration.instrument import OpticsLoopCorr
from opsim4.model import OpticsLoopCorrModel

class OpticsLoopCorrModelTest(unittest.TestCase):

    def setUp(self):
        self.model = OpticsLoopCorrModel()

    def test_basic_information_after_creation(self):
        self.assertTrue(isinstance(self.model.config_obj, OpticsLoopCorr))
        self.assertEqual(len(self.model.params), 3)
        #print(self.model.params)
