import collections
import unittest

from lsst.sims.ocs.configuration import ObservingSite
from opsim4.model import ModelHelper

class ModelHelperTest(unittest.TestCase):

    def setUp(self):
        self.mh = ModelHelper(ObservingSite())

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.mh.config_obj)
        self.assertIsNotNone(self.mh.config_cls)
        self.assertIsNotNone(self.mh.paren_match)
        self.assertIsNotNone(self.mh.params)

    def test_blank_helper_basic_information_after_creation(self):
        blank_mh = ModelHelper()
        self.assertIsNone(blank_mh.config_obj)
        self.assertIsNone(blank_mh.config_cls)
        self.assertIsNotNone(blank_mh.paren_match)
        self.assertIsNone(blank_mh.params)

    def test_make_parameter(self):
        # Setup top-level information for one parameter
        param_dict = collections.defaultdict(dict)
        fields = self.mh.config_cls._fields
        key = "name"
        value = fields[key]
        pdict = param_dict[key]
        self.mh.make_parameter(pdict, key, value)
        self.assertEqual(pdict["dtype"], "Str")
        self.assertEqual(pdict["value"], "Cerro Pachon")
        self.assertIsNone(pdict["units"])

    def test_make_parameter_dictionary(self):
        param_dict = self.mh.make_parameter_dictionary()
        self.assertEqual(len(param_dict), 7)

    def test_check_parameter(self):
        self.assertTrue(self.mh.check_parameter("name", "Sierra Madre"))
        self.assertFalse(self.mh.check_parameter("height", "2650.0"))

    def test_get_parameter(self):
        self.assertEquals(self.mh.get_parameter("name"), "Cerro Pachon")
        self.assertEquals(self.mh.get_parameter("height"), 2650.0)
