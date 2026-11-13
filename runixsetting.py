import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from runixsettingui import Ui_SettingWindow
from runix_library import library_ui
import os 
import shutil
import json
from runix_al import alwindow

class setting(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settingui = Ui_SettingWindow()
        self.settingui.setupUi(self)
        self.settingui.applybutton.clicked.connect(self.apply)
        self.settingui.Applydcompiler.clicked.connect(self.default_decompiler)
        self.libui = library_ui()
        self.libui.hide()
        self.settingui.add_lib_button.clicked.connect(lambda:self.libui.show())
        self.setcurrentterminalcbox()
        self.setcurrentextdefault_decompilercombobox()
        self.settingui.applycompilebutton.clicked.connect(self.setcompile)
        self.setFixedSize(800,600)
        self.setcurrenttext_compile_combobox()
        self.confdir = os.path.expanduser("~/.config/runix")
        self.conffilecontroller()
        self.settingui.Resetsettings_button.clicked.connect(self.resetsetting)
        self.settingui.applyrunixsetting_button.clicked.connect(self.DPaply)
        self.setcurrentDBcombobox()
        self.settingui.Runix_help_button.clicked.connect(self.runixhelp)
        self.al = alwindow()
        self.settingui.addlangbutton.clicked.connect(lambda:self.al.show())
    def runixhelp(self):
        rhwindow = QDialog(self)
        rhwindow.setWindowTitle("Help")
        rhwindow.setMinimumSize(600,400)
        rhlayout = QVBoxLayout(rhwindow)
        helptexedit = QTextEdit(rhwindow)
        helptexedit.setReadOnly(True)
        helptexedit.setPlainText("Runix User Guide\n\n"
            "• Shortcuts: \n"
            "  - Ctrl+O: Open File\n"
            "  - Ctrl+H: Most Recently Run Files\n"
            "  - Esc: Close File\n"
            "  - F5: Run\n"
            "  - F6: Compile\n"
            "  - Ctrl+.: Settings\n\n"
            "• Right-Click Menus: \n"
            "  - Right-click the Run button to add arguments,\n"
            "  - Right-click the Compile button to configure C/C++ flags.\n"
            "  - Right-click the File button to open the Most Recently Run Files menu\n")
        rhlayout.addWidget(helptexedit)
        rhcancelbutton = QPushButton(rhwindow)
        rhcancelbutton.setText("Cancel")
        rhlayout.addWidget(rhcancelbutton)
        rhwindow.setLayout(rhlayout)
        rhcancelbutton.clicked.connect(lambda:rhwindow.accept())
        rhwindow.show()

    def conffilecontroller(self,Detectfile=None,writefile=None,read=False):
        if not os.path.exists(self.confdir):
            os.mkdir(self.confdir)
        if Detectfile != None and read == False:
            with open(f"{self.confdir}/{Detectfile}","w") as f:
                f.write(writefile)
        elif Detectfile != None and read == True:
            data = None
            if os.path.exists(f"{self.confdir}/{Detectfile}"):
                with open(f"{self.confdir}/{Detectfile}","r") as n:
                    data = n.read()
            return data
            
    def DPaply(self):
        DB = self.settingui.DPcombobox.currentText()
        self.conffilecontroller(Detectfile="DB.txt",writefile=DB)
        QMessageBox.information(self,"Setting","The program must be restarted for the settings to take effect.")
    def setcurrentDBcombobox(self):
        DB = self.conffilecontroller(Detectfile="DB.txt",read=True)
        if DB == "X11":
            self.settingui.DPcombobox.setCurrentText("X11")
        elif DB == "Wayland":
            self.settingui.DPcombobox.setCurrentText("Wayland")
        else:
            self.settingui.DPcombobox.setCurrentText("X11")



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
    def resetsetting(self):
        Question = QMessageBox.question(self,"Sure?","Are you sure?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if Question == QMessageBox.StandardButton.Yes:
            shutil.rmtree(self.confdir,ignore_errors=True)
        


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
            if shutil.which("retdec-decompiler"):
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
        try:
            with open(f"{self.path}/default_compiler.json","r",encoding="utf8") as f:
                veri = json.load(f)
            self.settingui.c_combobox.setCurrentText(veri["C_COMPILER"].capitalize())
            self.settingui.cpp_combobox.setCurrentText(veri["CPP_COMPILER"].capitalize())
        except (json.JSONDecodeError, KeyError):
            return


        

        

    
            

    
        

def main():
    app = QApplication(sys.argv)
    win = setting()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()