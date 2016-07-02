import unittest

from lsst.sims.ocs.configuration.proposal import AreaDistribution

from opsim4.model import AreaDistributionPropModel

class AreaDistributionModelTest(unittest.TestCase):

    def setUp(self):
        self.model = AreaDistributionPropModel(AreaDistribution())
        self.num_params = 7

    # def xtest_basic_information_after_creation(self):
    #     self.assertEqual(len(self.model.parameter_order), self.num_params)
    #     self.assertEqual(len(self.model.params), self.num_params)
