import unittest

from opsim4.model import ObservatoryModel

class ObservatoryModelTest(unittest.TestCase):

    def setUp(self):
        self.obs_model = ObservatoryModel()
        self.num_parameters = 7

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.obs_model.config_obj)

    def test_make_parameter_dictionary(self):
        pd = self.obs_model.make_parameter_dictionary()
        self.assertEqual(len(pd), self.num_parameters)
        self.assertEqual(pd.keys()[0], self.obs_model.tab_order[0])
        self.assertEqual(pd.keys()[self.num_parameters - 1],
                         self.obs_model.tab_order[self.num_parameters - 1])
