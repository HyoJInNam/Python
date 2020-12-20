import os.path
path = os.path.dirname(os.path.abspath(".\\"))

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class wHelp(QDialog):
    def __init__(self, parent):
        super(wHelp, self).__init__(parent)
        uic.loadUi(path + "\\dist\\winUI\\help.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.setSizePolicy(0, 0)

        self.help_bCheck.clicked.connect(self.close)
        self.show()