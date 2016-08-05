import unittest

from lsst.sims.ocs.configuration.proposal import AreaDistribution

from opsim4.model import AreaDistributionPropModel

class AreaDistributionModelTest(unittest.TestCase):

    def setUp(self):
        self.model = AreaDistributionPropModel(AreaDistribution())
        self.num_params = 7
