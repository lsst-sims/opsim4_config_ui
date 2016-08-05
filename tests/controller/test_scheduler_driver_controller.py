try:
    from unittest import mock
except ImportError:
    import mock
import unittest
import sys

from PyQt4 import QtGui

from opsim4.controller import SchedulerDriverController

class SchedulerDriverControllerTest(unittest.TestCase):

    app = QtGui.QApplication(sys.argv)

    @classmethod
    def setupClass(cls):
        patcher1 = mock.patch("opsim4.widgets.SchedulerDriverWidget", spec=True)
        cls.addCleanup(patcher1.stop)
        cls.mock_widget = patcher1.start()

    def setUp(self):
        self.controller = SchedulerDriverController("scheduler_driver")

    def test_basic_information_after_creation(self):
        self.assertIsNotNone(self.controller.model)
