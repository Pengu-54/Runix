import sys
import json
import os
import shutil
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import*
from ui_runix_language_ui import Ui_MainWindow
class alwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.langtype = ""
        self.ui.inter_radiob.toggled.connect(self.interlang)
        self.ui.compileradiob.toggled.connect(self.complang)
        self.ui.BB_radiob.hide()
        self.ui.applybutton.clicked.connect(self.apply)
        self.confdir = os.path.expanduser("~/.config/runix")

    def interlang(self,check):
        if not check:
            return
        self.langtype = "interpreter"
        self.ui.execute_command_lineedit.hide()
        self.ui.Cfe_lineedit.hide()
        self.ui.FileextensionLineedit.show()
    def complang(self,chek):
        if not chek:
            return
        self.langtype = "compile"
        self.ui.execute_command_lineedit.show()
        self.ui.Cfe_lineedit.show()
        self.ui.FileextensionLineedit.show()

    def apply(self):
        execdata = self.ui.execLineEdit.text()
        namedata = self.ui.Namelineedit.text()
        fileextensiondata = self.ui.FileextensionLineedit.text()
        cfedata = self.ui.Cfe_lineedit.text()
        executecommanddata = self.ui.execute_command_lineedit.text()
        if not fileextensiondata.startswith("."):
            fileextensiondata = f".{fileextensiondata}"
        fileextensiondata = fileextensiondata.strip().lower()
        if not os.path.exists(self.confdir):
            os.mkdir(self.confdir)
        if not os.path.exists(f"{self.confdir}/custom_lang"):
            os.mkdir(f"{self.confdir}/custom_lang")
        if os.path.exists(f"{self.confdir}/custom_lang/{fileextensiondata}.json"):
            filequ = QMessageBox.question(self,"File","This file already exists. Do you want to overwrite it?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if filequ == QMessageBox.StandardButton.No:
                return
            
        langvalue = {}
        if self.langtype == "interpreter":
            langvalue["type"] = "interpreter"
        elif self.langtype == "compile":
            langvalue["type"] = "compile"
            if not cfedata.strip():
                self.ui.Cfe_lineedit.setText("ERROR ERROR THIS IS EMPTY")
                return
            elif not executecommanddata.strip():
                self.ui.execute_command_lineedit.setText("ERROR ERROR THIS IS EMPTY")
                return
            if cfedata.strip() and executecommanddata.strip():
                if cfedata.strip().upper() == "ELF":
                    cfedata = cfedata.strip().upper()
                else:
                    cfedata = cfedata.strip()
                    if not cfedata.startswith("."):
                        cfedata = f".{cfedata}"
                    if ".." in cfedata or "/" in cfedata or cfedata == ".":
                        QMessageBox.critical(self,"Error","Invalid Compiled file extension")
                        return
                    cfedata = cfedata.lower()
                langvalue.update({"cfe":cfedata,"executecommand":executecommanddata})
        if execdata.strip() and namedata.strip() and fileextensiondata.strip() and self.langtype.strip():
            if not fileextensiondata.startswith("."):
                fileextensiondata = f".{fileextensiondata}"
            
            fileextensiondata = fileextensiondata.lower()
            if ".." in fileextensiondata or "/" in fileextensiondata or fileextensiondata == ".":
                QMessageBox.critical(self,"Error","Invalid File extension setting")
                return
            langvalue.update({"execdata":execdata,"namedata":namedata,"fileextension":fileextensiondata})
            with open(f"{self.confdir}/custom_lang/{fileextensiondata}.json","w") as b:
                json.dump(langvalue,b)
            QMessageBox.information(self,"Language","The language has been successfully added")
            self.ui.execLineEdit.clear()
            self.ui.FileextensionLineedit.clear()
            self.ui.Namelineedit.clear()

        else:
            QMessageBox.warning(self,"Language","Invalid setting")




            








if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = alwindow()
    win.show()
    sys.exit(app.exec())
