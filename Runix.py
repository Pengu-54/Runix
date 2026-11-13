#Runix is not an IDE
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Runixui import *
from runixsetting import setting
import subprocess
import os
import shutil
import json
from runix_flag_window import flagwindow
import shlex
from librarydetect import library


class pyg(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(815,482)
        self.ui.decompilebutton.hide()
        self.ui.Filebutton.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.Filebutton.customContextMenuRequested.connect(self.recentylfiles)
        self.ui.CompileButton.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.CompileButton.customContextMenuRequested.connect(self.flagwindowstartup)
        self.ui.Runbutton.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.Runbutton.customContextMenuRequested.connect(self.addaarguments)
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
        self.shortcuts()
        self.ui.decompilebutton.clicked.connect(self.decompile)
        self.flagwindow = flagwindow()
        self.compilercommand = None
        self.confdir = os.path.expanduser("~/.config/runix")
        self.getcustomcommandextension()



    def shortcuts(self):
        self.openfileshortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.openfileshortcut.activated.connect(self.file)
        self.openrfshorcut = QShortcut(QKeySequence("Ctrl+H"),self)
        self.openrfshorcut.activated.connect(self.recentylfiles)
        self.closefileshortcut = QShortcut(QKeySequence("Esc"),self)
        self.closefileshortcut.activated.connect(self.closefile)
        self.runfileshortcut = QShortcut(QKeySequence("F5"),self)
        self.compileshortcut = QShortcut(QKeySequence("F6"),self)
        self.compileshortcut.activated.connect(self.compile)
        self.runfileshortcut.activated.connect(self.run)
        self.opensettingshorcut = QShortcut(QKeySequence("Ctrl+."),self)
        self.opensettingshorcut.activated.connect(lambda:self.setting.show())


    




        
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
            self.enableddecompilebutton(self.path)
            self.detectcustomcommand()
            self.removeflagconffile()

    def file(self):
        self.drag = False
        self.customcom = self.getcustomcommandextension()
        self.path = QFileDialog.getOpenFileName(self,"Select a file","",f"(*.py *.c *.cpp *.sh *.js *.java *.php *.lua *.pl *.rb *.go *.rs *.dart *.swift *.cs *.asm *.ts *.kt *.jar \
        {self.customcom} );;All files (*)")
        if f"{self.path[0]}" != "":
            short_path = os.path.basename(f"{self.path[0]}")
            self.ui.Filebutton.setText(short_path)
            self.setWindowTitle(f"Runix-{short_path}")
            self.ui.Runbutton.setEnabled(True)
            self.enabledcompilebutton(f"{self.path[0]}")
            self.enableddecompilebutton(f"{self.path[0]}")
            self.detectcustomcommand()
            self.removeflagconffile()
            
        else:
            self.path = None
            self.ui.Runbutton.setEnabled(False)
            self.closefile()
    def detectcustomcommand(self,file=None):
        resultfile = ""
        localdrag = self.drag
        if file != None:
            localdrag = True
        if localdrag == False:
            resultfile = f"{self.path[0]}"
        else:
            resultfile = f"{self.path}"

            

        ext = os.path.splitext(os.path.basename(resultfile))[1]
        langfile = f"{self.confdir}/custom_lang/{ext}.json"
        if not os.path.exists(langfile):
            return
        try:
            with open(langfile,"r",encoding="utf8") as b:
                customcdata = json.load(b)
            if customcdata["type"] == "compile":
                self.ui.CompileButton.show()
                self.ui.Runbutton.setText("Compile And Run")
        except (OSError,KeyError,ValueError):
            return

    def getcustomcommandextension(self):
        returnvalue = ""
        if not os.path.exists(self.confdir) or not os.path.exists(f"{self.confdir}/custom_lang"):
            return ""
        for i in os.listdir(f"{self.confdir}/custom_lang"):
            if not i.endswith(".json"):
                continue
            self.ext = os.path.splitext(os.path.basename(i))[0]
            if not i.startswith("."):
                returnvalue +=f"*.{self.ext} "
            else:
                returnvalue +=f"*{self.ext} "
        return returnvalue
        



    def closefile(self):
        self.path = None
        self.drag = False
        self.ui.Filebutton.setText("Drop The File Here")
        self.enabledcompilebutton("test.py")
        self.setWindowTitle("Runix")
        self.ui.Runbutton.setEnabled(False)
        self.ui.decompilebutton.hide()
        if os.path.exists(self.confdir):
            with open(f"{self.confdir}/flag_cpp_c_code.txt","w") as m:
                m.write("None")
    def recentylfiles(self):
        path = os.path.expanduser("~/.config/runix")
        self.data = []
        self.mrrc = False
        self.rfwindow = QDialog(self)
        self.mrrcmrrfcombobox = QComboBox(self.rfwindow)
        self.mrrcmrrfcombobox.addItems(["Most Recently Run Files","Most Recently Run Command"])
        self.rfwindow.setMinimumSize(700,450)
        self.rfwindow.setWindowTitle("Most Recently Run Files")
        self.rflayout = QVBoxLayout()
        self.rfwindow.setLayout(self.rflayout)
        self.view = QListView(self.rfwindow)
        self.listmodel = QStringListModel()
        self.view.setModel(self.listmodel)
        self.searchbar = QLineEdit(self.rfwindow)
        self.searchbar.setPlaceholderText("Search.")
        self.loadhistory()
        self.rflayout.addWidget(self.mrrcmrrfcombobox)
        self.rflayout.addWidget(self.searchbar)
        self.rflayout.addWidget(self.view)
        self.view.clicked.connect(self.selectedfile)
        self.clearbutton = QPushButton("Clear",self.rfwindow)
        self.rflayout.addWidget(self.clearbutton)
        self.clearbutton.clicked.connect(self.clearmrrf)
        self.searchbar.textChanged.connect(self.searchrf)
        self.mrrcmrrfcombobox.currentIndexChanged.connect(self.mrrfc)

        self.rfwindow.show()

    def mrrfc(self):
        if self.mrrc == False:
            self.mrrc = True
            self.rfwindow.setWindowTitle("Most Recently Run Command")
            self.loadhistory()
        else:
            self.mrrc = False
            self.rfwindow.setWindowTitle("Most Recently Run Files")
            self.loadhistory()
    def flagwindowstartup(self):
        if self.drag == False:
            if f"{self.path[0]}".endswith((".cpp",".c")):
                self.flagwindow.loadfile(f"{self.path[0]}")
                self.flagwindow.show()

        else:
            if self.path.endswith((".cpp",".c")):
                self.flagwindow.loadfile(self.path)
                self.flagwindow.show()
    def loadhistory(self):
        self.data = []
        path = os.path.expanduser("~/.config/runix")
        if not os.path.exists(f"{path}"):
            self.mrrcmrrfcombobox.hide()
        else:
            self.mrrcmrrfcombobox.show()
        if self.mrrc == False:
            if os.path.exists(f"{path}/Mrrf.txt"):
                with open(f"{path}/Mrrf.txt","r",encoding="utf8") as f:
                    self.reading = f.read().splitlines()
                self.data.extend(self.reading[::-1])
                self.listmodel.setStringList(self.data)
        else:
            if os.path.exists(f"{path}/MRRC.txt"):
                with open(f"{path}/MRRC.txt","r") as b:
                    self.mrrcdata = b.read().splitlines()
                self.data.extend(self.mrrcdata[::-1])
                self.listmodel.setStringList(self.data)




    def searchrf(self):
        try:
            self.searchdata = []
            self.textveri = self.searchbar.text()
            if self.textveri == "":
                self.listmodel.setStringList(self.data)
                return
            if self.mrrc == False:
                for i in self.reading[::-1]:
                    if self.textveri in i:
                        self.searchdata.append(i)
            else:
                for b in self.mrrcdata[::-1]:
                    if self.textveri in b:
                        self.searchdata.append(b)
            self.listmodel.setStringList(self.searchdata)
        except AttributeError:
            return




    def selectedfile(self,index):
        data = index.data()
        self.filedata = data
        if self.mrrc == True:
            QApplication.clipboard().setText(data)
            QMessageBox.information(self,"Info","Successfully copied!")
            return
        self.path = self.filedata
        self.ui.Filebutton.setText(self.path)
        self.ui.Runbutton.setEnabled(True)
        self.enabledcompilebutton(self.path)
        self.detectcustomcommand(file=self.path)
        self.enableddecompilebutton(self.path)
        self.drag = True
        self.removeflagconffile()
        self.rfwindow.accept()

    def clearmrrf(self):
        path = os.path.expanduser("~/.config/runix")
        if not os.path.exists(path):
            os.mkdir(path)
        if self.mrrc == False:
            with open(f"{path}/Mrrf.txt","w") as f:
                f.write("")
        else:
            try:
                os.remove(f"{path}/MRRC.txt")
            except FileNotFoundError:
                return
        self.data = []
        self.searchdata = []
        self.listmodel.setStringList(self.data)

    def addaarguments(self):
        try:
            if not os.path.exists(self.confdir):
                os.mkdir(self.confdir)
            arguments,ok = QInputDialog.getText(self,"Argument","Enter an argument")
            if not ok:
                return
            shlex.split(arguments)
            if ok:
                if arguments.strip():
                    with open(f"{self.confdir}/runarguments.txt","w") as f:
                        f.write(arguments)
                else:
                    with open(f"{self.confdir}/runarguments.txt","w") as n:
                        n.write("None")
        except ValueError as e:
            QMessageBox.critical(self,"Error","Invalid argument")
            return
    

    def enableddecompilebutton(self,file):
        klasor = os.path.dirname(file)
        if shutil.which("file"):
            elf = subprocess.run(["file","-b",file],capture_output=True,text=True,cwd=klasor)
        try:
            if "ELF" in elf.stdout or file.endswith(".jar"):
                self.ui.decompilebutton.show()
            else:
                self.ui.decompilebutton.hide()
        except UnboundLocalError:
            QMessageBox.critical(self,"Error",'Please install "file" ')

    def removeflagconffile(self):
        if os.path.exists(self.confdir):
            with open(f"{self.confdir}/flag_cpp_c_code.txt","w") as h:
                h.write("None")
        if os.path.exists(self.confdir):
            with open(f"{self.confdir}/runarguments.txt","w") as f:
                f.write("None")
        

    def decompile(self):
        if self.ui.decompilebutton.isHidden():
            return
        
        if self.drag == True:
            decompilefile(self.path)
        else:
            decompilefile(self.path[0])
        self.ui.decompilebutton.hide()
        self.path = None
        self.ui.Filebutton.setText("Drop The File Here")
        self.ui.Runbutton.setEnabled(False)
        self.drag = False

        

        
        




            
    def run(self):
        if self.path != None:
            self.ui.Filebutton.setText("Drop The File Here")
            self.ui.Runbutton.setEnabled(False)
            self.ui.CompileButton.hide()
            self.ui.Runbutton.setText("Run")
            if self.drag == False:
                runfile(f"{self.path[0]}",compile=False,ui=True)
            else:
                runfile(f"{self.path}",compile=False,ui=True)
                self.drag = False
            self.path = None
            if not self.ui.decompilebutton.isHidden():
                self.ui.decompilebutton.hide()

                
    def enabledcompilebutton(self,file):
        if file.endswith(".cpp") or file.endswith(".c") or file.endswith(".java") or file.endswith((".go",".rs",".dart",".swift",".asm",".kt")):
            self.ui.CompileButton.show()
            self.ui.Runbutton.setText("Compile And Run")
        else:
            self.ui.CompileButton.hide()
            self.ui.Runbutton.setText("Run")


    def compile(self):
        if self.path is None:
            return
        if self.ui.CompileButton.isHidden():
            return

        if self.drag == True:
            runfile(self.path,compile=True,ui=True)
        else:
            runfile(self.path[0],compile=True,ui=True)      
        self.ui.CompileButton.hide()
        self.ui.Runbutton.setText("Run")
        self.ui.Filebutton.setText("Drop The File Here")
        self.ui.Runbutton.setEnabled(False)
        self.drag = False
        self.path = None



        



            
def main():
    path = os.path.expanduser("~/.config/runix")
    DB = "xcb;wayland"
    if os.path.exists(path):
        if os.path.exists(f"{path}/DB.txt"):
            with open(f"{path}/DB.txt","r") as b:
                DB = b.read()
            if DB == "X11":
                DB = "xcb;wayland"
            elif DB == "Wayland":
                DB = "wayland;xcb"
    os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland.textinput=false"
    os.environ["QT_QPA_PLATFORM"] = DB
    app = QApplication(sys.argv)
    win = pyg()
    win.show()
    sys.exit(app.exec())


def checkstartup():
    path = os.path.expanduser("~/.config/runix")
    if os.path.exists(path):
        with open(f"{path}/flag_cpp_c_code.txt","w") as b:
            b.write("None")
        with open(f"{path}/runarguments.txt","w") as n:
            n.write("None")
    compilestatus = False
    decompilestatus = False
    terminalsettings = False
    ccompilestatus = False
    cppcompilestatus = False
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
                if file == "--compile":
                    compilestatus = True
                    decompilestatus = False
                    continue
                elif file == "--setterminal":
                    decompilestatus = False
                    compilestatus = False
                    terminalsettings = True
                    continue
                elif file == "--setccompiler" and terminalsettings == False:
                    ccompilestatus = True
                    cppcompilestatus = False
                    decompilestatus = False
                    compilestatus = False
                    terminalsettings = False
                    continue
                elif file == "--setcppcompiler" and terminalsettings == False and ccompilestatus == False:
                    ccompilestatus = False
                    cppcompilestatus = True
                    decompilestatus = False
                    compilestatus = False
                    terminalsettings = False
                    continue
                elif file == "--decompile":
                    compilestatus = False
                    decompilestatus = True
                    continue
                elif decompilestatus == True:
                    decompilefile(file,ui=False)
                else:
                    if terminalsettings == True:
                        writeterminalsetting(file)   
                    elif ccompilestatus == True:
                        setccompiler(file)   
                    elif cppcompilestatus == True:
                        setcppcompiler(file)   
                    else:
                        runfile(file,compilestatus)
    else:
        main()

def setcppcompiler(file):
    path = os.path.expanduser("~/.config/runix")
    if not os.path.exists(path):
        os.mkdir(path)
    if os.path.exists(f"{path}/default_compiler.json"):
        with open(f"{path}/default_compiler.json","r",encoding="utf8") as f:
            data = json.load(f)
        data["CPP_COMPILER"] = file
        if not shutil.which(data["CPP_COMPILER"]):
            print(f'{data["CPP_COMPILER"]} not found')
            return
        if file != "g++" and file != "clang++":
            print("invalid compiler")
            return
        with open(f"{path}/default_compiler.json","w",encoding="utf8") as b:
            json.dump(data,b)
            print(f'The settings were saved successfully\nThe C++ compiler:{data["CPP_COMPILER"]}')
    else:
        data = {"CPP_COMPILER": "g++", "C_COMPILER": "gcc"}
        if file != "g++" and file != "clang++":
            print("invalid compiler")
            return
        if shutil.which("gcc"):
            data["C_COMPILER"] = "gcc"
        elif shutil.which("clang"):
            data["C_COMPILER"] = "clang"
        if shutil.which(file):
            data["CPP_COMPILER"] = file
        else:
            print(f"{file} not found")
            return
        with open(f"{path}/default_compiler.json","w",encoding="utf8") as m:
            json.dump(data,m)
            print(f'The settings were saved successfully\nThe C++ compiler:{data["CPP_COMPILER"]}')

def setccompiler(file):
    path = os.path.expanduser("~/.config/runix")
    if not os.path.exists(path):
        os.mkdir(path)
    if not shutil.which(file):
        print(f"{file} not found ")
        return
    if os.path.exists(f"{path}/default_compiler.json"):
        with open(f"{path}/default_compiler.json","r",encoding="utf8") as n:
            data = json.load(n)
        data["C_COMPILER"] = file
        if data["C_COMPILER"] != "clang" and data["C_COMPILER"] != "gcc":
            print("invalid compiler")
            return
        with open(f"{path}/default_compiler.json","w") as b:
            json.dump(data,b,ensure_ascii=False)
            print(f'The settings were saved successfully\nThe C compiler:{data["C_COMPILER"]}')
    else:
        data = {"CPP_COMPILER": "g++", "C_COMPILER": "gcc"}
        if file != "gcc" and file != "clang":
            print("invalid compiler")
            return
        if shutil.which("g++"):
            data["CPP_COMPILER"] = "g++"
        elif shutil.which("clang++"):
            data["CPP_COMPILER"] = "clang++"
        if shutil.which(file):
            data["C_COMPILER"] = file
        else:
            print(f"{file} not found")
            return
        with open(f"{path}/default_compiler.json","w",encoding="utf8") as m:
            json.dump(data,m)
        print(f'The settings were saved successfully\nThe C compiler:{data["C_COMPILER"]}')
        


def runfile(file = None,compile=False,ui=False):
    file = os.path.abspath(file)
    terminal = ""
    flag = []
    writeflag = []
    klasor = os.path.dirname(file)
    path = os.path.expanduser("~/.config/runix")

    if not os.path.exists(path):
        os.mkdir(path)
    with open(f"{path}/Mrrf.txt","a+",encoding="utf8") as f:
        f.write(f"{file}\n")
    
    if shutil.which("kitty"):
        terminal = "kitty"
        flag = ["--hold","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--hold","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif shutil.which("alacritty"):
        terminal = "alacritty"
        flag = ["--hold","-e","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--hold","-e","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif shutil.which("konsole"):
        terminal = "konsole"
        flag = ["--noclose","-e","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--noclose","-e","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif shutil.which("kgx"):
        terminal = "kgx"
        flag = ["--","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif shutil.which("xfce4-terminal"):
        terminal = "xfce4-terminal"
        flag = ["-x","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["-x","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    elif shutil.which("gnome-terminal"):
        terminal = "gnome-terminal"
        flag = ["--","bash","-lc",'cd "$1" || exit; shift; "$@"; echo; read -p "Press Enter to close..." _',"runix"]
        writeflag = ["--","bash","-lc",'printf "%b\n" "$1"; read -p "Press Enter to close..." _',"runix"]
    else:
        if ui == True:
            QMessageBox.critical(None,"Error","No supported terminal found.")
        else:
            subprocess.Popen(["notify-send","Error","No supported terminal found"])
        return



        
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
        if not shutil.which(terminal):
            if ui == True:
                QMessageBox.critical(None,"Error",f"{terminal} not found")
            else:
                subprocess.Popen(["notify-send","Error",f"{terminal} not found"])
            return


    if klasor == "":
        klasor = "."

    if not os.path.exists(file):
        subprocess.Popen([terminal]+writeflag+[f"File not found:{file}"])
        return
        
    filename = os.path.splitext(os.path.basename(file))[0]
    if shutil.which("file"):
        elf = subprocess.run(["file","-b",file],capture_output=True,text=True,cwd=klasor)
        if "ELF" in elf.stdout:
            elffargument = run_program_with_arguments()
            if elffargument != None:
                subprocess.Popen([terminal]+flag+[klasor]+[file]+elffargument)
            else:
                subprocess.Popen([terminal]+flag+[klasor]+[file])
            MRRCintlang([file],elffargument)
            return
    C_compiler_name = ""
    CPP_compiler_name = ""
    if shutil.which("g++"):
        CPP_compiler_name = "g++"
    elif shutil.which("clang++"):
        CPP_compiler_name = "clang++"
    if shutil.which("gcc"):
        C_compiler_name = "gcc"
    elif shutil.which("clang"):
        C_compiler_name = "clang"
    try:
        if os.path.exists(f"{path}/default_compiler.json"):
            with open(f"{path}/default_compiler.json","r",encoding="utf8") as f:
                cjsondata = json.load(f)
                C_compiler_name = cjsondata["C_COMPILER"]
                CPP_compiler_name = cjsondata["CPP_COMPILER"]
    except (json.JSONDecodeError,KeyError):
        pass


    if os.path.exists(f"{path}/flag_cpp_c_code.txt"): 
        with open(f"{path}/flag_cpp_c_code.txt","r",encoding="utf8") as i:
            flagdata = i.read()
        if flagdata != "None" and file.endswith((".cpp",".c")):
            splitedflagdata = shlex.split(flagdata)
            if file.endswith(".c"):
                compilerlanguea(C_compiler_name,splitedflagdata,ui,compile,file,klasor,terminal,flag,writeflag)
            elif file.endswith(".cpp"):
                compilerlanguea(CPP_compiler_name,splitedflagdata,ui,compile,file,klasor,terminal,flag,writeflag)
            return

            
    
    if file.endswith(".py"):
        interpreterlanguage("python3",["python3",file],terminal,klasor,flag,writeflag)
    elif file.endswith(".cpp"):
        if not CPP_compiler_name:
            subprocess.Popen([terminal]+writeflag+["ERROR No C++ compiler found. Please install g++ or clang++."])
            return
        compilerlanguea(CPP_compiler_name, [CPP_compiler_name, file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".c"):
        if not C_compiler_name:
            subprocess.Popen([terminal]+writeflag+["ERROR No C compiler found. Please install gcc or clang."])
            return
        compilerlanguea(C_compiler_name, [C_compiler_name, file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".sh"):
        shargument = run_program_with_arguments()
        if shargument != None:
            subprocess.Popen([terminal]+flag+[klasor]+["bash"]+[file]+shargument)
        else:
            subprocess.Popen([terminal]+flag+[klasor]+["bash"]+[file])
        MRRCintlang(["bash",file],shargument)

    elif file.endswith(".js"):
        interpreterlanguage("node",["node",file],terminal,klasor,flag,writeflag)
    elif file.endswith(".java"):
        if shutil.which("javac") and shutil.which("java"):
            filename = os.path.splitext(os.path.basename(file))[0]
            java = subprocess.run(["javac",file],capture_output=True,text=True,cwd=klasor)
            if ui == True and compile == True and java.returncode == 0:
                QMessageBox.information(None,"Compile","Successfully compiled")
            elif java.returncode == 0 and compile == False:
                run_with_argument(terminal,flag,klasor,["java",filename])
            elif java.returncode != 0:
                javaerror = java.stderr
                subprocess.Popen([terminal]+writeflag+[javaerror])
            MRRCcomplang(["javac",file],["java",f"{filename}"],run_program_with_arguments(),compile)
        else:
            subprocess.Popen([terminal]+writeflag+["ERROR javac or java not found. Please install the JDK."])
    elif file.endswith(".php"):
        interpreterlanguage("php",["php",file],terminal,klasor,flag,writeflag)
    elif file.endswith(".lua"):
        interpreterlanguage("lua",["lua",file],terminal,klasor,flag,writeflag)
    elif file.endswith(".rb"):
        interpreterlanguage("ruby",["ruby",file],terminal,klasor,flag,writeflag)
    elif file.endswith(".pl"):
        interpreterlanguage("perl",["perl",file],terminal,klasor,flag,writeflag)
    elif file.endswith(".go"):
        compilerlanguea("go", ["go", "build", "-o", filename, file], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".rs"):
        compilerlanguea("rustc", ["rustc", file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".dart"):
        compilerlanguea("dart", ["dart", "compile", "exe", file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".swift"):
       compilerlanguea("swiftc", ["swiftc", file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".cs"):
        if shutil.which("dotnet"):
            run_with_argument(terminal,flag,klasor,["dotnet","run",file])
            MRRCintlang(["dotnet","run",file],run_program_with_arguments())
        else:
            subprocess.Popen([terminal]+writeflag+["ERROR dotnet not found Please install dotnet"])
    elif file.endswith(".asm"):
        filename = os.path.splitext(os.path.basename(file))[0]
        if not shutil.which("nasm"):
            subprocess.Popen([terminal]+writeflag+["ERROR nasm not found Please install nasm "])
            return
        if not shutil.which("ld"):
            subprocess.Popen([terminal]+writeflag+["ERROR ld linker not found. Please install binutils."])
            return
        assembly = subprocess.run(["nasm","-f","elf64",file,"-o",f"{filename}.o"],capture_output=True,text=True,cwd=klasor)
        if assembly.returncode == 0:
            ldassmebly = subprocess.run(["ld",f"{filename}.o","-o",filename],capture_output=True,text=True,cwd=klasor)
            if ldassmebly.returncode == 0 and compile ==False:
                argument = run_with_argument(terminal,flag,klasor,[f"./{filename}"])
            elif ldassmebly.returncode == 0 and compile == True and ui == True:
                QMessageBox.information(None,"Compile","Successfully compiled")
            elif ldassmebly.returncode != 0:
                lderror = ldassmebly.stderr
                subprocess.Popen([terminal]+writeflag+[lderror])
            argument = run_program_with_arguments()
            MRRCcomplang(["nasm","-f","elf64",file,"-o",f"{filename}.o"],[f"./{filename}"],argument,compile,linkercommand=["ld",f"{filename}.o","-o",filename])
        else:
            assemblyerror = assembly.stderr
            subprocess.Popen([terminal]+writeflag+[assemblyerror])
    elif file.endswith(".ts"):
        interpreterlanguage("npx",["npx","tsx",file],terminal,klasor,flag,writeflag)

    elif file.endswith(".kt"):
        compilerlanguea("kotlinc",["kotlinc",file,"-include-runtime","-d",f"{filename}.jar"],ui,compile,file,klasor,terminal,flag,writeflag,["java","-jar",f"{filename}.jar"])

    elif file.endswith(".jar"):
        if shutil.which("java"):
            run_with_argument(terminal,flag,klasor,["java","-jar",file])
            jarargument = run_program_with_arguments()
            MRRCintlang(["java","-jar",file],jarargument)
        else:
            subprocess.Popen([terminal]+writeflag+["ERROR java not found. Please install the JRE/JDK."])

    else:
        customlanguage(path,file,filename,ui,compile,klasor,terminal,flag,writeflag)


def filenotfoundmessage(ui,file,terminal,writeflag):       
    if ui is True:
        QMessageBox.critical(None,"File Type",f"unsupported file type:{file}")
    else:
        subprocess.Popen([terminal]+writeflag+[f"unsupported file type:{file}"])

def customlanguage(path,file,filename,ui,compile,klasor,terminal,flag,writeflag):
    ext = os.path.splitext(os.path.basename(file))[1]
    langfile = f"{path}/custom_lang/{ext}.json"
    if not os.path.exists(langfile):
        filenotfoundmessage(ui,file,terminal,writeflag)
        return
    try:
        with open(langfile,"r",encoding="utf8") as m:
            data = json.load(m)
        compiledfilext = None
        if data["type"] == "compile":
            compiledfilext = data["cfe"]
        result = rccexpand(data["execdata"],file,filename,cfe=compiledfilext)
        if data["type"] == "interpreter":
            interpreterlanguage(data["namedata"],result,terminal,klasor,flag,writeflag)
        elif data["type"] == "compile":
            if data["cfe"] == "ELF":
                runcommand = [f"./{filename}"]
            else:
                runcommand = rccexpand(data["executecommand"],file,filename,cfe=data["cfe"])
            compilerlanguea(data["namedata"],result,ui,compile,file,klasor,terminal,flag,writeflag,runcommand)
        else:
            subprocess.Popen([terminal]+writeflag+[f"invalid file {ext}.json"])
    except (OSError,ValueError,KeyError):
        subprocess.Popen([terminal]+writeflag+[f"invalid file {ext}.json"])

def rccexpand(command,file,filename,cfe=None):
    result = []
    for b in shlex.split(command):
        if b == "rcc=file":
            b = file
        elif b == "rcc=compiledfile":
            if cfe is not None and cfe != "ELF" and cfe.strip():
                b = filename + cfe
            else:
                b = filename

        result.append(b)
    return result
def run_program_with_arguments():
    path = os.path.expanduser("~/.config/runix")
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(f"{path}/runarguments.txt"):
        with open(f"{path}/runarguments.txt","w") as f:
            f.write("None")
    with open(f"{path}/runarguments.txt","r") as b:
        arguments = b.read()
    
    if arguments == "None":
        return None
    splitetargument = shlex.split(arguments)
    return splitetargument

def run_with_argument(terminal,flag,klasor,command):
    argument = run_program_with_arguments()
    if argument != None:
        lang = subprocess.Popen([terminal]+flag+[klasor]+command+argument,)
    else:
        subprocess.Popen([terminal]+flag+[klasor]+command)

    

def interpreterlanguage(langname,command,terminal,klasor,flag,writeflag):
    if shutil.which(langname):
        argument = run_program_with_arguments()
        if argument != None:
            subprocess.Popen([terminal]+flag+[klasor]+command+argument)
        else:
            subprocess.Popen([terminal]+flag+[klasor]+command)
        MRRCintlang(command,argument)
        
    else:
        subprocess.Popen([terminal]+writeflag+[f"Error {langname} not found Please install {langname}"])

def resolve(cmd):
    if cmd.startswith("pkg-config:"):
        for alt in cmd.split(":", 1)[1].split("|"):      
            pkgs = alt.split()
            r = subprocess.run(["pkg-config", "--cflags", "--libs"] + pkgs, capture_output=True, text=True)
            if r.returncode == 0:
                return r.stdout.strip()
        return None
    return cmd

def compilerlanguea(languagename,command,ui,compile,file,klasor,terminal,flag,writeflag,runcommand=None):
    try:
        lib = library()
        fpcstatus = False
        fpc = tuple(lib.getfpicfileext())
        for i in lib.detectlibrary(file):
            if i.startswith("pkg-config"):
                i = resolve(i)
            if fpcstatus == False and file.endswith(fpc):
                command.insert(1,"-fPIC")
                fpcstatus = True
            command.extend(shlex.split(i))
    except TypeError:
        pass
    path = os.path.expanduser("~/.config/runix")
    filename = os.path.splitext(os.path.basename(file))[0]
    argument = run_program_with_arguments()
    if runcommand == None:
        runcommand = [f"./{filename}"]
    if not shutil.which(languagename):
        subprocess.Popen([terminal]+writeflag+[f"ERROR {languagename} not found Please install {languagename}"])
        return
    language = subprocess.run(command,capture_output=True,text=True,cwd=klasor)
    if language.returncode == 0 and compile == False:
        if argument != None:
            subprocess.Popen([terminal]+flag+[klasor]+runcommand+argument)
        else:
            subprocess.Popen([terminal]+flag+[klasor]+runcommand)
    elif compile == True and language.returncode == 0 and ui == True:
        QMessageBox.information(None,"Compile","Successfully compiled")
    elif language.returncode != 0:
        languageerror = language.stderr
        subprocess.Popen([terminal]+writeflag+[languageerror])
    if not os.path.exists(path):
        os.mkdir(path)
    if file.endswith((".cpp",".c")) and language.returncode == 0:
        with open(f"{path}/flag_cpp_c_code.txt","w",encoding="utf8") as n:
            n.write("None")
    MRRCcomplang(command,runcommand,argument,compile)


def MRRCcomplang(command,runcommand,argument,compile,linkercommand=None):
    path = os.path.expanduser("~/.config/runix")
    if os.path.exists(path):
        Most_recently_compile_command = shlex.join(command)
        Most_recently_run_command = shlex.join(runcommand)
        if argument != None:
            m_argument = shlex.join(argument)
            Most_recently_run_command += f" {m_argument}"
        if compile == False and linkercommand == None:
            MRRC = f"{Most_recently_compile_command} && {Most_recently_run_command}"
        else:
            MRRC = f"{Most_recently_compile_command}"
        if linkercommand != None:
            Most_recently_linker_command = shlex.join(linkercommand)
            if compile == False:
                MRRC = f"{Most_recently_compile_command} && {Most_recently_linker_command} && {Most_recently_run_command}"
            else:
                MRRC = f"{Most_recently_compile_command} && {Most_recently_linker_command}"
        if not os.path.exists(f"{path}/MRRC.txt"):
            with open(f"{path}/MRRC.txt","w") as b:
                b.write(f"{MRRC}")
        else:
            with open(f"{path}/MRRC.txt","a") as h:
                h.write(f"\n{MRRC}")
def MRRCintlang(command,argument):
    path = os.path.expanduser("~/.config/runix")
    if os.path.exists(path):
        MRRC = ""
        runcom = shlex.join(command)
        if argument != None:
            argumentjoin = shlex.join(argument)
            MRRC += f"{runcom} {argumentjoin}"
        else:
            MRRC = f"{runcom}"
        if not os.path.exists(f"{path}/MRRC.txt"):
            with open(f"{path}/MRRC.txt","w") as f:
                f.write(MRRC)
        else:
            with open(f"{path}/MRRC.txt","a") as b:
                b.write(f"\n{MRRC}")
def decompilefile(file,ui=True):
    file = os.path.abspath(file)
    decompiler = "objdump"
    spath = os.path.expanduser("~/.config/runix")
    if not os.path.exists(spath):
        os.mkdir(spath)
    if os.path.exists(f"{spath}/Default_decompiler.txt"):
        with open(f"{spath}/Default_decompiler.txt","r",encoding="utf8") as f:
            decompiler = f.read()

    klasor = os.path.dirname(file) or "."

    if file.endswith(".jar"):
        if shutil.which("jadx"):
            filename = os.path.splitext(os.path.basename(file))[0]
            outputfolder = f"{filename}_decompiled"
            jde = subprocess.run(["jadx",file,"-d",outputfolder],cwd=klasor)
            if jde.returncode != 0:
                subprocess.run(["notify-send","Decompile","The decompilation process completed with errors"])
            else:
                subprocess.run(["notify-send","Decompile","The decompilation was successful"])
        else:
            subprocess.run(["notify-send","Error","Jadx not found Please install Jadx"])
        return

    elf = None
    if shutil.which("file"):
        elf = subprocess.run(["file","-b",file],capture_output=True,text=True,cwd=klasor)

    if elf is not None and "ELF" in elf.stdout:
        if decompiler == "retdec" and shutil.which("retdec-decompiler"):
            result = subprocess.run(["retdec-decompiler", file])
        elif shutil.which("objdump"):
            with open(f"{file}.asm", "w", encoding="utf8") as out:
                result = subprocess.run(["objdump", "-d", file], stdout=out)
        else:
            subprocess.run(["notify-send","Error","objdump not found Please install binutils"])
            return
        if result.returncode == 0:
            subprocess.run(["notify-send","Decompile","The decompilation was successful"])
        else:
            subprocess.run(["notify-send","Decompile","The decompilation process completed with errors"])
        return

    subprocess.run(["notify-send","File type","This file type is not supported"])

def writeterminalsetting(terminal):
    terminals = ["Xfce-Terminal","Gnome-console","Kitty","Konsole","Alacritty","Gnome-terminal","Auto"]
    if terminal == "Gnome-console":
        if not shutil.which("kgx"):
            print(f"{terminal} not found")
            return
    elif terminal == "Xfce-Terminal":
        if not shutil.which("xfce4-terminal"):
            print("Invalid terminal. Only the following terminals are valid: Kitty, Konsole, Gnome-console, Xfce-Terminal, Alacritty, Gnome-terminal, Auto")
            return
    elif terminal == "Auto":
        pass
    else:
        if not shutil.which(terminal.lower()):
            print(f"{terminal} not found. Please install it")
            return
            
    timer = 0
    for i in terminals:
        timer += 1
        if i == terminal:
            break
        if timer == 7:
            print("Invalid terminal. Only the following terminals are valid: Kitty, Konsole, Gnome-console, Xfce-terminal, Alacritty, Gnome-terminal,Auto")
            return
    path = os.path.expanduser("~/.config/runix")
    if not os.path.exists(path):
        os.mkdir(path)

    with open(f"{path}/default_terminal.txt","w",encoding="utf8") as f:
        f.write(terminal)
    print("The terminal settings have been successfully saved")

        
        


            
        
        
    
if __name__ == "__main__":
    checkstartup()