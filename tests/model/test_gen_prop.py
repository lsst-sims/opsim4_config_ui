import unittest

from lsst.sims.ocs.configuration.proposal import General

from lsst.sims.opsim4.model import GeneralPropModel

class GeneralModelTest(unittest.TestCase):

    def setUp(self):
        self.model = GeneralPropModel(General())
        self.num_params = 7
