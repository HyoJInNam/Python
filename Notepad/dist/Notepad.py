#QTPY

#참조
# https://www.youtube.com/watch?v=Ss7dDDS-DhU&list=PLnIaYcDMsScwsKo1rQ18cLHvBdjou-kb5&ab_channel=%EC%9E%AC%EC%A6%90%EB%B3%B4%ED%94%84
# https://wikidocs.net/35478
# https://appia.tistory.com/298

import os.path
import sys
from PyQt5 import uic
path = os.path.dirname(os.path.abspath(".\\"))
winNotepad = uic.loadUiType(path + "\\dist\\winUI\\main.ui")[0]

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, QTime, QRegExp, Qt
from PyQt5.QtGui import QTextCursor
import npfind, npreplace, nphelp

class Notepad(QMainWindow, winNotepad):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(path + 'dist\\icon\\notepad32.png'))

        self.action_clear.triggered.connect(self.clear)
        self.action_new.triggered.connect(self.new)
        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)
        self.action_saveAs.triggered.connect(self.saveAs_file)
        self.action_close.triggered.connect(self.close)

        self.stack = []
        self.temp = ''
        self.action_undo.triggered.connect(self.undo)
        self.action_cut.triggered.connect(self.cut)
        self.action_copy.triggered.connect(self.copy)
        self.action_paste.triggered.connect(self.paste)
        self.action_delete.triggered.connect(self.delete)
        self.action_find.triggered.connect(self.dialog_find)
        self.action_findNext.triggered.connect(self.findNext)
        self.action_findPrev.triggered.connect(self.findPrev)
        self.action_replace.triggered.connect(self.dialog_replace)
        self.action_selectAll.triggered.connect(self.textEdit.selectAll)
        self.action_time_date.triggered.connect(self.time_date)

        self.action_wordwrap.triggered.connect(self.linewrap)
        self.action_font.triggered.connect(self.font)

        self.zoom = 0
        self.action_zoomIn.triggered.connect(self.zoomIn)
        self.action_zoomOut.triggered.connect(self.zoomOut)
        self.action_zoomRestoreDefault.triggered.connect(self.zoomRestoreDefault)
        self.action_statusBar.triggered.connect(self.statusBar)

        self.action_help.triggered.connect(self.help)

        self.opened = False
        self.file_name = '제목 없음'
        self.file_path = ''

    # ================== MENU FILE======================
    def clear(self):
        if self.is_changed_data() == True:
            self.clear()
        self.textEdit.clear()

    def new(self):
        os.system(path + '\\dist\\Notepad.exe')

    def save(self, fname):
        data = self.textEdit.toPlainText()
        with open(fname, 'w', encoding='UTF8') as f:
            f.write(data)
        
        print("save {}!!".format(fname))
        self.file_name = fname[fname.rfind('/') + 1:]
        self.setWindowTitle(self.file_name)
        self.stack.clear()
    def save_file(self):
        if self.opened:
            self.save(self.file_path)
        else:
            self.saveAs_file()
    def saveAs_file(self):
        fname = QFileDialog.getSaveFileName(self)
        if fname[0]:
            self.save(fname[0])
            self.open(fname[0])

    def open(self, fname):
        print("open {}!!".format(fname))
        self.opened = True
        self.file_path = fname
        self.file_name = self.file_path[self.file_path.rfind('/') + 1:]
        self.setWindowTitle(self.file_name)
    def open_file(self):
        fname = QFileDialog.getOpenFileName(self)
        if fname[0]:
            with open(fname[0], encoding='UTF8') as f:
                data = f.read()
            self.textEdit.setPlainText(data)
            self.open(fname[0])

    def is_changed_data(self):
        if self.opened == True:
            with open(self.file_path, encoding='UTF8') as ofp:
                data = ofp.read()
            return False if (self.textEdit.toPlainText() == data) else True
        else:
            return False if (self.textEdit.toPlainText() == '') else True
    def closeMsgBox(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('메모장')
        msgBox.setText("변경 내용을 {}에 저장하시겠습니까?".format(self.file_name))
        msgBox.addButton('저장(S)',QMessageBox.YesRole)
        msgBox.addButton('저장 안 함(N)',QMessageBox.NoRole)
        msgBox.addButton('취소',QMessageBox.RejectRole)
        return msgBox.exec_()
    def closeMsgBoxEvent(self, event, bignore, ret):
        if ret == 0:
            self.save_file()
            event.ignore()
        elif ret == 1:
            if bignore:
                event.ignore()
            return
        elif ret == 2:
            event.ignore()
    def closeEvent(self, event,bignore = False):
        if self.is_changed_data() == False:
            if bignore:
                event.ignore()
            return
        self.closeMsgBoxEvent(event, bignore, self.closeMsgBox())

    # ================== MENU EDIT======================
    def undo(self):
        if not self.stack:
            return

        print('undo!')
        event = self.stack[-1]
        self.stack.pop()

        if event['event'] == 'cut':
            self.textEdit.textCursor().setPosition(event['pos'])
            self.textEdit.textCursor().insertHtml(event['text'])
        elif event['event'] == 'delete':
            self.textEdit.textCursor().setPosition(event['pos'])
            self.textEdit.textCursor().insertHtml(event['text'])
    def cut(self):
        print('cut!')
        text = self.textEdit.toPlainText()
        start = self.textEdit.textCursor().selectionStart()
        end = self.textEdit.textCursor().selectionEnd()

        self.temp = text[start:end]
        self.stack.append({'event': 'cut', 'pos': start, 'text': self.temp})
        self.textEdit.textCursor().removeSelectedText()
    def copy(self):
        print('copy!')
        text = self.textEdit.toPlainText()
        start = self.textEdit.textCursor().selectionStart()
        end = self.textEdit.textCursor().selectionEnd()

        self.temp = text[start:end]
        self.stack.append({'event': 'cut', 'pos': start, 'text': self.temp})
    def paste(self):
        print('paste!')
        if self.temp == '':
            return
        pos = self.textEdit.textCursor().position()
        self.textEdit.textCursor().insertHtml(self.temp)
        self.stack.append({'event': 'paste', 'pos': pos, 'text': self.temp})
    def delete(self):
        print('delete!')
        text = self.textEdit.toPlainText()
        if self.textEdit.textCursor().hasSelection():
            start = self.textEdit.textCursor().selectionStart()
            end = self.textEdit.textCursor().selectionEnd()
            self.stack.append({'event': 'delete', 'pos': start, 'text': self.temp})
            self.textEdit.textCursor().removeSelectedText()
        else:
            pos = self.textEdit.textCursor().position()
            self.temp = text[pos]
            self.stack.append({'event': 'delete', 'pos': pos, 'text': self.temp})
            self.textEdit.textCursor().deleteChar()

    def notFoundMsgbox(self, str):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('메모장')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('''"{}"을 찾을 수 없습니다.'''.format(str))
        msgBox.addButton('확인', QMessageBox.YesRole)
        return msgBox.exec_()
    def setCursor(self, dir, start, end, err):
        print('cursor: (', start, end, ')', dir)
        if start != -1:  ## 검색결과 있음
            cursor = self.textEdit.textCursor()
            cursor.setPosition(start)
            cursor.movePosition(dir, QTextCursor.KeepAnchor, abs(end - start))
            self.textEdit.setTextCursor(cursor)
        else:
            self.notFoundMsgbox(err)
    def case_sensitive(self, find_str, isCheck):
        if isCheck:
            cs = Qt.CaseSensitive
        else:
            cs = Qt.CaseInsensitive

        rx = QRegExp(find_str)
        rx.setCaseSensitivity(cs)
        return rx
    def next(self, find_str, isCheck):
        rx = self.case_sensitive(find_str, isCheck)
        pos = self.textEdit.textCursor().position()
        text = self.textEdit.toPlainText() + ' '

        start = rx.indexIn(text, pos)
        end = start + len(find_str)
        self.setCursor(QTextCursor.Right, start, end, find_str)
    def prev(self, find_str, isCheck):
        rx = self.case_sensitive(find_str, isCheck)
        pos = self.textEdit.textCursor().position()
        text = self.textEdit.toPlainText() + ' '

        end = rx.lastIndexIn(text, pos, rx.CaretAtOffset)
        start = end - len(find_str)
        self.setCursor(QTextCursor.Left, end, start, find_str)

    def dialog_find(self):
        self.wFind = npfind.wFind(self)
    def findNext(self):
        print('next!')
        self.wFind.next()
    def findPrev(self):
        print('prev!')
        self.wFind.prev()

    def dialog_replace(self):
        npreplace.wReplace(self)

    def time_date(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        str = time.toString('ap h:mm') + ' ' + date.toString('yyyy-MM-dd')

        cursor = self.textEdit.textCursor()
        cursor.insertText(str)
        cursor.setPosition(cursor.position() + len(str))
        self.textEdit.setTextCursor(cursor)

    # ================== MENU FORMAT======================
    def linewrap(self):
        if self.textEdit.lineWrapMode() == QTextEdit.NoWrap:
            self.textEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        elif self.textEdit.lineWrapMode() == QTextEdit.WidgetWidth:
            self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

    def font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    # ================== MENU FORMAT======================
    def zoomIn(self):
        self.textEdit.zoomIn(10)
        self.zoom -= 10

    def zoomOut(self):
        self.textEdit.zoomOut(10)
        self.zoom += 10

    def zoomRestoreDefault(self):
        self.textEdit.zoomIn(self.zoom)
        self.zoom = 0

    def updateStatus(self):
        cs = self.textEdit.textCursor();
        str = 'Line '+ str(cs.blockNumber())+', Colum '+ str(cs.columnNumber() + 1)+ ', zoom '+ str(100 + self.zoom), '%'
        print(str)
        #self.statusbar.showMessage(str);
    def statusBar(self):
        self.statusbar.hideOrShow()

    # ================== MENU HELP======================
    def help(self):
        nphelp.wHelp(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    app.exec_()
