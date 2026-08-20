import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import*
from PyQt6.QtGui import *
from runixsettingui import Ui_SettingWindow
import os 
import subprocess

def host_which(cmd):
    try:
        return subprocess.run(["flatpak-spawn", "--host", "which", cmd],
                            capture_output=True, text=True).returncode == 0
    except FileNotFoundError:
        return False

class setting(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settingui = Ui_SettingWindow()
        self.settingui.setupUi(self)
        self.settingui.applybutton.clicked.connect(self.apply)
        self.setcurrentterminalcbox()
        self.setFixedSize(800,600)

    def setcurrentterminalcbox(self):
        path = os.path.expanduser("~/.config/runix")
        if not os.path.exists(path):
            return
        else:
            try:
                with open(f"{path}/default_terminal.txt","r") as f:
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

        if not host_which(terminal1) and terminal != "Auto":
            QMessageBox.critical(self,"Error",f"{terminal} Not found. Please install the {terminal}.")
            return
        path = os.path.expanduser("~/.config/runix")
        if not os.path.exists(path):
            os.mkdir(path)
        with open(f"{path}/default_terminal.txt","w") as f:
            f.write(terminal)
        QMessageBox.information(self,"Setting","The settings were successfully applied")

def main():
    app = QApplication(sys.argv)
    win = setting()
    win.show()
    sys.exit(app.exec())
