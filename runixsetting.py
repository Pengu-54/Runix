import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from runixsettingui import Ui_SettingWindow
import os 
import shutil
import json

class setting(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settingui = Ui_SettingWindow()
        self.settingui.setupUi(self)
        self.settingui.applybutton.clicked.connect(self.apply)
        self.settingui.Applydcompiler.clicked.connect(self.default_decompiler)
        self.setcurrentterminalcbox()
        self.setcurrentextdefault_decompilercombobox()
        self.settingui.applycompilebutton.clicked.connect(self.setcompile)
        self.setFixedSize(800,600)
        self.setcurrenttext_compile_combobox()


    def setcurrentterminalcbox(self):
        self.path = os.path.expanduser("~/.config/runix")
        if not os.path.exists(self.path):
            return
        else:
            try:
                with open(f"{self.path}/default_terminal.txt","r") as f:
                    veri = f.read()
                self.settingui.Terminalcombobox.setCurrentText(veri)
            except FileNotFoundError:
                return

    def apply(self):
        terminal = self.settingui.Terminalcombobox.currentText()
        terminal1 = ""
        if terminal == "Xfce-Terminal":
            terminal1 = "xfce4-terminal"
        elif terminal == "Gnome-console":
            terminal1 = "kgx"
        else:
            terminal1 = terminal.lower()
        
        if not shutil.which(terminal1) and terminal != "Auto":
            QMessageBox.critical(self,"Error",f"{terminal} Not found. Please install the {terminal}.")
            return
        path = os.path.expanduser("~/.config/runix")
        if not os.path.exists(path):
            os.mkdir(path)
        with open(f"{path}/default_terminal.txt","w") as f:
            f.write(terminal)
        QMessageBox.information(self,"Setting","The settings were successfully applied")

    def default_decompiler(self):
        path = os.path.expanduser("~/.config/runix")
        decompiler = self.settingui.Decompiler_comboBox.currentText()
        if not os.path.exists(path):
            os.mkdir(path)
        if decompiler == "Objdump":
            with open(f"{path}/Default_decompiler.txt","w",encoding="utf8") as f:
                f.write("objdump")
        elif decompiler == "Retdec":
            if shutil.which("retdec"):
                with open(f"{path}/Default_decompiler.txt","w",encoding="utf8") as a:
                    a.write("retdec")
            else:
                QMessageBox.critical(self,"Error","Retdec not found Please install retdec")
                return
        QMessageBox.information(self,"Setting","The settings were successfully applied")

    def setcurrentextdefault_decompilercombobox(self):
        try:
            if os.path.exists(self.path):

                with open(f"{self.path}/Default_decompiler.txt","r",encoding="utf8") as f:
                    self.ddcmpler = f.read()
                    self.ddcmpler = self.ddcmpler.capitalize()
                    self.settingui.Decompiler_comboBox.setCurrentText(self.ddcmpler)
        except FileNotFoundError:
            return


    def setcompile(self):
        self.cppcomboboxdata = self.settingui.cpp_combobox.currentText()
        self.ccomboboxdata = self.settingui.c_combobox.currentText()
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if shutil.which(self.cppcomboboxdata.lower()) and shutil.which(self.ccomboboxdata.lower()):
            cppveri = {"CPP_COMPILER":self.cppcomboboxdata.lower(),"C_COMPILER":self.ccomboboxdata.lower()}
            with open(f"{self.path}/default_compiler.json","w",encoding="utf8") as f:
                json.dump(cppveri,f,ensure_ascii=False)
            QMessageBox.information(self,"Setting","The settings were successfully applied")
        else:
            QMessageBox.critical(self,"ERROR","The setting could not be applied because some compilers are not installed.")

    def setcurrenttext_compile_combobox(self):
        if not os.path.exists(self.path):
            return
        if not os.path.exists(f"{self.path}/default_compiler.json"):
            return
        with open(f"{self.path}/default_compiler.json") as f:
        
            veri = json.load(f)
        self.settingui.c_combobox.setCurrentText(veri["C_COMPILER"].capitalize())
        self.settingui.cpp_combobox.setCurrentText(veri["CPP_COMPILER"].capitalize())


        

        

    
            

    
        

def main():
    app = QApplication(sys.argv)
    win = setting()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()