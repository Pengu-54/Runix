import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import*
from ui_runix_flag_ui import Ui_FlagWindow
import shutil
import json
class flagwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FlagWindow()
        self.ui.setupUi(self)
        self.ui.cancelbutton.clicked.connect(self.closeprogram)
        self.file = None
        self.path = os.path.expanduser("~/.config/runix")
        self.cppcompiler = None
        self.ccompiler = None
        self.compilercommand = []
        self.lmstatus = False
        self.ui.lmcheckbox.toggled.connect(self.lm)
        self.ui.savebutton.clicked.connect(self.savesetting)
        self.stdstatus = False



    def loadfile(self,file):
        self.file = file
        self.filename = os.path.splitext(os.path.basename(self.file))[0]
        self.compilercommand = []
        self.lmstatus = self.ui.lmcheckbox.isChecked()
        os.makedirs(self.path, exist_ok=True)
        if self.file.lower().endswith(".cpp"):
            if shutil.which("g++"):
                self.cppcompiler = "g++"
            elif shutil.which("clang++"):
                self.cppcompiler = "clang++"
            else:
                QMessageBox.critical(self, "Compiler error", "g++ or clang++ was not found.")
                return
            if os.path.exists(f"{self.path}/default_compiler.json"):
                try:
                    with open(f"{self.path}/default_compiler.json", "r", encoding="utf8") as f:
                        cppcompilerdata = json.load(f)
                    selected = cppcompilerdata.get("CPP_COMPILER")
                    if selected and shutil.which(selected):
                        self.cppcompiler = selected
                except (OSError, json.JSONDecodeError):
                    pass
            self.compilercommand.append(self.cppcompiler)
        elif self.file.lower().endswith(".c"):
            if shutil.which("gcc"):
                self.ccompiler = "gcc"
            elif shutil.which("clang"):
                self.ccompiler = "clang"
            else:
                QMessageBox.critical(self, "Compiler error", "gcc or clang was not found.")
                return
            if os.path.exists(f"{self.path}/default_compiler.json"):
                try:
                    with open(f"{self.path}/default_compiler.json", "r", encoding="utf8") as a:
                        ccompilerdata = json.load(a)
                    selected = ccompilerdata.get("C_COMPILER")
                    if selected and shutil.which(selected):
                        self.ccompiler = selected
                except (OSError, json.JSONDecodeError):
                    pass
            self.compilercommand.append(self.ccompiler)

        self.compilercommand.append(self.file)
        self.compilercommand.append("-o")
        self.compilercommand.append(self.filename)

    def closeprogram(self):
        self.hide()

    def lm(self):
        self.lmstatus = self.ui.lmcheckbox.isChecked()

    def savesetting(self):
        if not self.file:
            return None

        file = self.file
        self.compilercommand = []
        self.loadfile(file)
        if len(self.compilercommand) < 4:
            return None

        flags = []
        std = self.ui.stdlineedit.text().strip()
        include_path = self.ui.Ilineedit.text().strip()
        include_file = self.ui.includelineedit.text().strip()

        if std:
            flags.append(f"-std={std.removeprefix('-std=').removeprefix('-std ')}")
        if include_path:
            flags.append(f"-I{include_path.removeprefix('-I')}")
        if include_file:
            flags.extend(["-include", include_file])
        self.compilercommand[1:1] = flags
        if self.ui.lmcheckbox.isChecked():
            self.compilercommand.append("-lm")
        self.getcompilercommand()
        QMessageBox.information(self,"Flag Setting","The settings were saved successfully")
        self.hide()
        return self.compilercommand.copy()

    def getcompilercommand(self):
        commnd = ""
        if not self.compilercommand:
            with open(f"{self.path}/flag_cpp_c_code.txt","w") as f:
                f.write("None")
            return None
        with open(f"{self.path}/flag_cpp_c_code.txt", "w", encoding="utf8") as f:
            commnd = " ".join(self.compilercommand)
            f.write(commnd)
            
                
                
        return self.compilercommand.copy()







        
                    
            








def main():
    app = QApplication(sys.argv)
    win = flagwindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
