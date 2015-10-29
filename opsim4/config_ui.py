from PyQt4 import QtCore, QtGui

class OpsimConfigDlg(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)

        self.buttonbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Cancel)
        self.connect(self.buttonbox, QtCore.SIGNAL("rejected()"), self, QtCore.SLOT("reject()"))

def run():
    import sys
    app = QtGui.QApplication(sys.argv)
    form = OpsimConfigDlg()
    form.show()
    app.exec_()
