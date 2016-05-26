import unittest

from opsim4.model import ScienceModel

class ScienceModelTest(unittest.TestCase):

    def setUp(self):
        self.sci_model = ScienceModel()
        self.num_parameters = 4
        self.num_proposals = 1

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.sci_model.config_obj)
        self.assertIsNotNone(self.sci_model.ad_objs)
        self.assertEqual(len(self.sci_model.ad_objs), self.num_proposals)
        self.assertIsNotNone(self.sci_model.ad_cls)

    def test_make_parameter_dictionary(self):
        pd = self.sci_model.make_parameter_dictionary()
        self.assertEqual(len(pd), self.num_proposals)
        pdd = pd.values()[0]
        self.assertEqual(len(pdd), self.num_parameters)
        self.assertEqual(pdd["name"]["value"], "UniversalWeak")
        self.assertEqual(pdd["sky_region"]["value"]["dec_window"]["value"], 90.0)
        self.assertEqual(pdd["scheduling"]["value"]["max_num_targets"]["value"], 100)
        self.assertEqual(len(pdd["sky_region"]["value"]["limit_selections"]["value"]), 2)
        self.assertEqual(len(pdd["filters"]["value"][0].keys()), 6)
