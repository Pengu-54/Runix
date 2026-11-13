import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ui_runix_library import Ui_MainWindow
import os
import librarydetect


class library_ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hidestatus = True
        self.setWindowTitle("Library")
        self.ui.fpic_label.hide()
        self.ui.file_ext_lineedit.hide()
        self.ui.fpic_checkbox.toggled.connect(self.fpic_check)
        self.ui.edit_json_button.clicked.connect(self.editjson)
        self.confdir = os.path.expanduser("~/.config/runix")
        self.lib = librarydetect.library()
        self.ui.savebutton.clicked.connect(self.savelibsetting)

    def savelibsetting(self):
        headertext = self.ui.header_lineedit.text()
        flagtext = self.ui.flag_lineedit.text()
        file_ext_text = self.ui.file_ext_lineedit.text()
        if not headertext.strip() or not flagtext.strip():
            QMessageBox.critical(self,"Error","Invalid Settings")
            return
        if not file_ext_text.strip():
            file_ext_text = None
        self.lib.addcustomlibrary(headertext,flagtext,fileexntFpic=file_ext_text)
        QMessageBox.information(self,"Info","Successfully saved!")
        self.ui.header_lineedit.clear()
        self.ui.file_ext_lineedit.clear()
        self.ui.flag_lineedit.clear()
        self.ui.fpic_checkbox.setChecked(False)


    def editjson(self):
        ejwindow = QDialog(self)
        ejwindow.setWindowTitle("Json file")
        ejwindow.setMinimumSize(1000,400)
        ejlayout = QVBoxLayout(ejwindow)
        self.ejtextedit = QTextEdit(ejwindow)
        ejsavebutton = QPushButton("Save",ejwindow)
        ejlayout.addWidget(self.ejtextedit)
        ejlayout.addWidget(ejsavebutton)
        ejwindow.setLayout(ejlayout)
        ejwindow.show()
        if os.path.exists(f"{self.confdir}/librarys.json"):
            with open(f"{self.confdir}/librarys.json","r") as r:
                jtextdata = r.read()
            self.ejtextedit.setPlainText(jtextdata)
        else:
            self.lib.createfile()
        ejsavebutton.clicked.connect(self.ejsave)

    def ejsave(self):
        try:
            data = self.ejtextedit.toPlainText()
            with open(f"{self.confdir}/librarys.json","w") as w:
                w.write(data)
            QMessageBox.information(self,"Info","Successfully saved!")

        except FileNotFoundError:
            QMessageBox.critical(self,"Error","librarys.json file not found.")
            return
    def fpic_check(self,check):
        if check == False:
            self.ui.fpic_label.hide()
            self.ui.file_ext_lineedit.hide()
            self.hidestatus = False
            self.ui.file_ext_lineedit.clear()
        else:
            self.ui.fpic_label.show()
            self.ui.file_ext_lineedit.show()
            self.hidestatus = True










def main():
    app = QApplication(sys.argv)
    win = library_ui()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()