import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Runixui import *
from runixsetting import setting
import subprocess
import os


class pyg(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(815,482)
        self.ui.Filebutton.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.Filebutton.customContextMenuRequested.connect(self.recentylfiles)
        self.setting = setting()
        self.ui.Settingbutton.clicked.connect(lambda:self.setting.show())
        self.ui.Filebutton.clicked.connect(self.file)
        self.ui.Runbutton.clicked.connect(self.run)
        self.ui.CompileButton.clicked.connect(self.compile)
        self.ui.Runbutton.setText("Run")
        self.path = None
        self.ui.CompileButton.hide()
        self.setAcceptDrops(True)
        self.ui.Runbutton.setEnabled(False)
        self.setWindowTitle("Runix")
        self.drag = False

    def dragEnterEvent(self,event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self,event):
        urls = event.mimeData().urls()
        if urls:
            self.path = urls[0].toLocalFile()
            self.ui.Runbutton.setEnabled(True)
            self.ui.Filebutton.setText(os.path.basename(self.path))
            self.drag = True
            self.enabledcompilebutton(self.path)

    def file(self):
        self.path = QFileDialog.getOpenFileName(self,"Select a file","","(*.py *.c *.cpp *.sh *.js *.java *.php *.lua *.pl *.rb *.go *.rs *.dart *.swift *.cs)")
        if f"{self.path[0]}" != "":
            short_path = os.path.basename(f"{self.path[0]}")
            self.ui.Filebutton.setText(short_path)
            self.setWindowTitle(f"Runix-{short_path}")
            self.ui.Runbutton.setEnabled(True)
            self.enabledcompilebutton(f"{self.path[0]}")
        else:
            self.path = None
            self.ui.Runbutton.setEnabled(False)

    def recentylfiles(self):
        self.data = []
        path = os.path.expanduser("~/.config/runix")
        self.rfwindow = QDialog(self)
        self.rfwindow.setMinimumSize(700,450)
        self.rfwindow.setWindowTitle("Most Recently Run Files")
        self.rflayout = QVBoxLayout()
        self.rfwindow.setLayout(self.rflayout)
        self.view = QListView(self.rfwindow)
        self.listmodel = QStringListModel()
        self.view.setModel(self.listmodel)
        if os.path.exists(f"{path}/Mrrf.txt"):
            with open(f"{path}/Mrrf.txt","r",encoding="utf8") as f:
                self.reading = f.read().splitlines()
            self.data.extend(self.reading)
            self.listmodel.setStringList(self.data)
        self.rflayout.addWidget(self.view)
        self.view.clicked.connect(self.selectedfile)
        self.clearbutton = QPushButton("Clear",self.rfwindow)
        self.rflayout.addWidget(self.clearbutton)
        self.clearbutton.clicked.connect(self.clearmrrf)
        self.rfwindow.show()

    def selectedfile(self,index):
        data = index.data()
        self.filedata = data
        self.path = self.filedata
        self.ui.Filebutton.setText(self.path)
        self.ui.Runbutton.setEnabled(True)
        self.enabledcompilebutton(self.path)
        self.drag = True
        self.rfwindow.accept()

    def clearmrrf(self):
        path = os.path.expanduser("~/.config/runix")
        with open(f"{path}/Mrrf.txt","w") as f:
            f.write("")
        self.data = []
        self.listmodel.setStringList(self.data)

    def run(self):
        if self.path != None:
            self.ui.Filebutton.setText("Drop The File Here")
            self.ui.Runbutton.setEnabled(False)
            self.ui.CompileButton.hide()
            self.ui.Runbutton.setText("Run")
            if self.drag == False:
                runfile(f"{self.path[0]}")
            else:
                runfile(f"{self.path}")
                self.drag = False
            self.path = None

    def enabledcompilebutton(self,file):
        if file.endswith(".cpp") or file.endswith(".c") or file.endswith(".java") or file.endswith((".go",".rs",".dart",".swift")):
            self.ui.CompileButton.show()
            self.ui.Runbutton.setText("Compile And Run")
        else:
            self.ui.CompileButton.hide()
            self.ui.Runbutton.setText("Run")

    def compile(self):
        if self.drag == True:
            runfile(self.path,compile=True)
        else:
            runfile(self.path[0],compile=True,ui=True)      
        self.ui.CompileButton.hide()
        self.ui.Runbutton.setText("Run")
        self.ui.Filebutton.setText("Drop The File Here")
        self.ui.Runbutton.setEnabled(False)
        self.drag = False


def main():
    app = QApplication(sys.argv)
    win = pyg()
    win.show()
    sys.exit(app.exec())


def checkstartup():
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            runfile(file)
    else:
        main()


def host_which(cmd):
    try:
        return subprocess.run(["flatpak-spawn", "--host", "which", cmd],
                            capture_output=True, text=True).returncode == 0
    except FileNotFoundError:
        return False


def runfile(file = None,compile=False,ui=False):
    terminal = ""
    flag = []
    writeflag = []
    klasor = os.path.dirname(file)
    path = os.path.expanduser("~/.config/runix")
    if not os.path.exists(path):
        os.mkdir(path)
    with open(f"{path}/Mrrf.txt","a+",encoding="utf8") as f:
        f.write(f"{file}\n")

    if host_which("kitty"):
        terminal = "kitty"
        flag = ["--hold","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--hold","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif host_which("alacritty"):
        terminal = "alacritty"
        flag = ["--hold","-e","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--hold","-e","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif host_which("konsole"):
        terminal = "konsole"
        flag = ["--noclose","-e","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--noclose","-e","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif host_which("kgx"):
        terminal = "kgx"
        flag = ["--","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif host_which("xfce4-terminal"):
        terminal = "xfce4-terminal"
        flag = ["-x","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["-x","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif host_which("gnome-terminal"):
        terminal = "gnome-terminal"
        flag = ["--","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]

    if os.path.exists(f"{path}/default_terminal.txt"):
        with open(f"{path}/default_terminal.txt","r") as f:
            veri = f.read()

    if os.path.exists(f"{path}/default_terminal.txt") and not veri == "Auto":
        if veri == "Kitty":
            terminal = "kitty"
            flag = ["--hold","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
            writeflag = ["--hold","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
        elif veri == "Konsole":
            terminal = "konsole"
            flag = ["--noclose","-e","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
            writeflag = ["--noclose","-e","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
        elif veri == "Gnome-console":
            terminal = "kgx"
            flag = ["--","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
            writeflag = ["--","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
        elif veri == "Alacritty":
            terminal = "alacritty"
            flag = ["--hold","-e","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
            writeflag = ["--hold","-e","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
        elif veri == "Xfce-Terminal":
            terminal = "xfce4-terminal"
            flag = ["-x","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
            writeflag = ["-x","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
        elif veri == "Gnome-terminal":
            terminal = "gnome-terminal"
            flag = ["--","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
            writeflag = ["--","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]

    if klasor == "":
        klasor = "."

    if not os.path.exists(file):
        subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+[f"File not found:{file}"])
        return

    filename = os.path.splitext(os.path.basename(file))[0]

    if file.endswith(".py"):
        subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+["python3"]+[file])
    elif file.endswith(".cpp"):
        compilerlanguea("g++", ["g++", file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".c"):
        compilerlanguea("gcc", ["gcc", file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".sh"):
        subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+["bash"]+[file])
    elif file.endswith(".js"):
        if host_which("node"):
            subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+["node"]+[file])
        else:
            subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+["Error Node not found please install node"])
    elif file.endswith(".java"):
        if host_which("javac") and host_which("java"):
            filename = os.path.splitext(os.path.basename(file))[0]
            java = subprocess.run(["flatpak-spawn","--host","javac",file],capture_output=True,text=True,cwd=klasor)
            if ui == True and compile == True and java.returncode == 0:
                QMessageBox.information(None,"Compile","Successfully compiled")
            elif java.returncode == 0 and compile == False:
                subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+["java",filename])
            elif java.returncode != 0:
                javaerror = java.stderr
                subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+[javaerror])
        else:
            subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+["ERROR javac or java not found. Please install the JDK."])
    elif file.endswith(".php"):
        if host_which("php"):
            subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+["php",file])
        else:
            subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+["ERROR php not found Please install php"])
    elif file.endswith(".lua"):
        if host_which("lua"):
            subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+["lua",file])
        else:
            subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+["ERROR lua not found Please install lua"])
    elif file.endswith(".rb"):
        if host_which("ruby"):
            subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+["ruby",file])
        else:
            subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+["ERROR ruby not found Please install ruby"])
    elif file.endswith(".pl"):
        if host_which("perl"):
            subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+["perl",file])
        else:
            subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+["ERROR perl not found Please install perl"])
    elif file.endswith(".go"):
        compilerlanguea("go", ["go", "build", "-o", filename, file], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".rs"):
        compilerlanguea("rustc", ["rustc", file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".dart"):
        compilerlanguea("dart", ["dart", "compile", "exe", file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".swift"):
       compilerlanguea("swiftc", ["swiftc", file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".cs"):
        if host_which("dotnet"):
            subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+["dotnet","run",file])
        else:
            subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+["ERROR dotnet not found Please install dotnet"])
    else:
        subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+[f"unsupported file type:{file}"])

def compilerlanguea(languagename,command,ui,compile,file,klasor,terminal,flag,writeflag):
    filename = os.path.splitext(os.path.basename(file))[0]
    if not host_which(languagename):
        subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+[f"ERROR {languagename} not found Please install {languagename}"])
        return
    language = subprocess.run(["flatpak-spawn","--host"]+command,capture_output=True,text=True,cwd=klasor)
    if language.returncode == 0 and compile == False:
        subprocess.Popen(["flatpak-spawn","--host",terminal]+flag+[klasor]+[f"./{filename}"])
    elif compile == True and language.returncode == 0 and ui == True:
        QMessageBox.information(None,"Compile","Successfully compiled")
    elif language.returncode != 0:
        languageerror = language.stderr
        subprocess.Popen(["flatpak-spawn","--host",terminal]+writeflag+[languageerror])

if __name__ == "__main__":
    checkstartup()
