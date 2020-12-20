import os.path
path = os.path.dirname(os.path.abspath(".\\"))

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QTextCursor


class wFind(QDialog):
    def __init__(self, parent):
        super(wFind, self).__init__(parent)
        uic.loadUi(path + "\\dist\\winUI\\find.ui", self)
        self.parent = parent
        self.setFixedSize(self.width(), self.height())
        self.setSizePolicy(0, 0 )
        self.find_bNext.clicked.connect(self.next)
        self.find_bPrev.clicked.connect(self.prev)
        self.find_bCancel.clicked.connect(self.close)
        self.show()

    def keyReleaseEvent(self, event):
        if self.find_str_text.text():
            self.find_bPrev.setEnabled(True)
            self.find_bNext.setEnabled(True)
        else:
            self.find_bPrev.setEnabled(False)
            self.find_bNext.setEnabled(False)

    def next(self):
        self.parent.next(self.find_str_text.text(), self.check_capital.isChecked())

    def prev(self):
        self.parent.prev(self.find_str_text.text(), self.check_capital.isChecked())


