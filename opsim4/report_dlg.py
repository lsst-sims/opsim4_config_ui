import collections
import os

from PyQt4 import QtCore, QtGui

from opsim4.utilities import title

__all__ = ["ReportDialog"]

class ReportDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ReportDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Difference Report")
        self.setMinimumSize(400, 300)

        self.report = []
        self.report_text = QtGui.QTextEdit(self)
        self.report_text.setReadOnly(True)
        self.button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.report_text)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def _make_css(self):
        self.report.append("<style>")
        self.report.append("h1 {color:blue;}")
        self.report.append("th, td {padding: 5px;}")
        self.report.append("th {text-align: left; background-color: #4CAF50; color: white;}")
        self.report.append("</style>")

    def _make_table_title(self):
        self.report.append("<tr>")
        self.report.append("<th>Property</th>")
        self.report.append("<th>Default</th>")
        self.report.append("<th>Change To</th>")
        self.report.append("</tr>")

    def _make_heading(self, text, level=1):
        self.report.append("<h{0}>{1}</h{0}>".format(level, text))

    def _make_rows(self, v):
        for j, (k, i) in enumerate(v.iteritems()):
            if j % 2 == 0:
                row_color = "#BDBDBD"
            else:
                row_color = "#FFFFFF"
            self.report.append("<tr bgcolor=\"{}\">".format(row_color))
            self.report.append("<td>{}</td>".format(k))
            self.report.append("<td>{}</td>".format(i[1]))
            self.report.append("<td>{}</td>".format(i[0]))
            self.report.append("</tr>")

    def _make_table(self, value):
            self.report.append("<table border=\"1\">")
            #self.report.append("<table>")
            self._make_table_title()
            #print("F:", value)
            self._make_rows(value)
            self.report.append("</table>")

    def make_report(self, ddict):
        headings = collections.defaultdict(list)
        for name in ddict.keys():
            if "/" in name:
                h1, h2 = name.split('/')
                headings[h1].append(h2)
            else:
                headings[name]
        #print(headings)
        #print(ddict)

        self.report = []
        self._make_css()

        for heading, sub_headings in headings.iteritems():
            self._make_heading(title(heading))
            if len(sub_headings) == 0:
                self._make_table(ddict[heading])
            else:
                for sub_heading in sub_headings:
                    self._make_heading(title(sub_heading), 2)
                    self._make_table(ddict[heading + "/" + sub_heading])

        final_report = os.linesep.join(self.report)
        #print(final_report)
        self.report_text.setHtml(final_report)
