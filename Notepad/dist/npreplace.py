import os
path = os.path.dirname(os.path.abspath(".\\"))

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QTextCursor

class wReplace(QDialog):
    def __init__(self, parent):
        super(wReplace, self).__init__(parent)
        uic.loadUi(path + "\\dist\\winUI\\replace.ui", self)
        self.parent = parent
        self.pTextEdit = parent.textEdit
        self.setFixedSize(self.width(), self.height())
        self.setSizePolicy(0, 0)

        self.replace_bPrev.clicked.connect(self.prev)
        self.replace_bNext.clicked.connect(self.next)
        self.replace_bReplace.clicked.connect(self.replace)
        self.replace_bReplaceAll.clicked.connect(self.replace_all)
        self.replace_bCheck.clicked.connect(self.close)
        self.replace_bCancel.clicked.connect(self.close)
        self.show()

    def keyReleaseEvent(self, event):
        if self.replace_find_str_text.text():
            self.replace_bPrev.setEnabled(True)
            self.replace_bNext.setEnabled(True)
            self.replace_bReplace.setEnabled(True)
            self.replace_bReplaceAll.setEnabled(True)
        else:
            self.replace_bPrev.setEnabled(False)
            self.replace_bNext.setEnabled(False)
            self.replace_bReplace.setEnabled(False)
            self.replace_bReplaceAll.setEnabled(False)

    def replace(self):
        if self.replace_find_str_text.text() and self.replace_str_text.text():
            self.pTextEdit.textCursor().removeSelectedText()
            self.pTextEdit.textCursor().insertHtml(self.replace_str_text.text())

    def replace_all(self):
        text = self.pTextEdit.toPlainText()
        text = text.replace(self.replace_find_str_text.text(), self.replace_str_text.text())
        self.pTextEdit.setPlainText(text)

    def next(self):
        self.parent.next(self.replace_find_str_text.text(), self.replace_capital.isChecked())

    def prev(self):
        self.parent.prev(self.replace_find_str_text.text(), self.replace_capital.isChecked())