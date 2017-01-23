import unittest

from lsst.sims.ocs.configuration.proposal import Sequence

from lsst.sims.opsim4.model import SequencePropModel

class SequenceModelTest(unittest.TestCase):

    def setUp(self):
        self.model = SequencePropModel(Sequence())
        self.num_params = 9
