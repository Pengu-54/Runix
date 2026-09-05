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


class pyg(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(815,482)
        self.ui.decompilebutton.hide()
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
        self.shortcuts()
        self.ui.decompilebutton.clicked.connect(self.decompile)
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

    def file(self):
        self.drag = False
        self.path = QFileDialog.getOpenFileName(self,"Select a file","","(*.py *.c *.cpp *.sh *.js *.java *.php *.lua *.pl *.rb *.go *.rs *.dart *.swift *.cs *.asm *.ts *.kt *.jar)")
        if f"{self.path[0]}" != "":
            short_path = os.path.basename(f"{self.path[0]}")
            self.ui.Filebutton.setText(short_path)
            self.setWindowTitle(f"Runix-{short_path}")
            self.ui.Runbutton.setEnabled(True)
            self.enabledcompilebutton(f"{self.path[0]}")
            self.enableddecompilebutton(f"{self.path[0]}")
            
        else:
            self.path = None
            self.ui.Runbutton.setEnabled(False)

    def closefile(self):
        self.path = None
        self.drag = False
        self.ui.Filebutton.setText("Drop The File Here")
        self.enabledcompilebutton("test.py")
        self.setWindowTitle("Runix")
        self.ui.Runbutton.setEnabled(False)
        self.ui.decompilebutton.hide()
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
        self.searchbar = QLineEdit(self.rfwindow)
        self.searchbar.setPlaceholderText("Search.")
        if os.path.exists(f"{path}/Mrrf.txt"):
            with open(f"{path}/Mrrf.txt","r",encoding="utf8") as f:
                self.reading = f.read().splitlines()
            self.data.extend(self.reading[::-1])
            self.listmodel.setStringList(self.data)
        self.rflayout.addWidget(self.searchbar)
        self.rflayout.addWidget(self.view)
        self.view.clicked.connect(self.selectedfile)
        self.clearbutton = QPushButton("Clear",self.rfwindow)
        self.rflayout.addWidget(self.clearbutton)
        self.clearbutton.clicked.connect(self.clearmrrf)
        self.searchbar.textChanged.connect(self.searchrf)

        self.rfwindow.show()

    def searchrf(self):
        self.searchdata = []
        self.textveri = self.searchbar.text()
        if self.textveri == "":
            self.listmodel.setStringList(self.data)
            return
        for i in self.reading[::-1]:
            if self.textveri in i:
                self.searchdata.append(i)
        self.listmodel.setStringList(self.searchdata)

    def selectedfile(self,index):
        data = index.data()
        self.filedata = data
        self.path = self.filedata
        self.ui.Filebutton.setText(self.path)
        self.ui.Runbutton.setEnabled(True)
        self.enabledcompilebutton(self.path)
        self.enableddecompilebutton(self.path)
        self.drag = True
        self.rfwindow.accept()

    def clearmrrf(self):
        path = os.path.expanduser("~/.config/runix")
        with open(f"{path}/Mrrf.txt","w") as f:
            f.write("")
        self.data = []
        self.searchdata = []
        self.listmodel.setStringList(self.data)

    def enableddecompilebutton(self,file):
        klasor = os.path.dirname(file)
        elf = subprocess.run(["file",file],capture_output=True,text=True,cwd=klasor)
        if "ELF" in elf.stdout or file.endswith(".jar"):
            self.ui.decompilebutton.show()
        else:
            self.ui.decompilebutton.hide()

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
    compilestatus = False
    decompilestatus = False
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
                if file == "--compile":
                    compilestatus = True
                    decompilestatus = False
                    continue
                elif file == "--decompile":
                    compilestatus = False
                    decompilestatus = True
                    continue
                elif decompilestatus == True:
                    decompilefile(file,ui=False)
                else:
                    runfile(file,compilestatus)
    else:
        main()


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
        subprocess.Popen([terminal]+writeflag+[f"File not found:{file}"])
        return
        
    filename = os.path.splitext(os.path.basename(file))[0]
    elf = subprocess.run(["file",file],capture_output=True,text=True,cwd=klasor)
    if "ELF" in elf.stdout:
        subprocess.Popen([terminal]+flag+[klasor]+[file])
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

    if os.path.exists(f"{path}/default_compiler.json"):
        with open(f"{path}/default_compiler.json","r",encoding="utf8") as f:
            cjsondata = json.load(f)
            C_compiler_name = cjsondata["C_COMPILER"]
            CPP_compiler_name = cjsondata["CPP_COMPILER"]
    
    if file.endswith(".py"):
        interpreterlanguage("python3",["python3",file],terminal,klasor,flag,writeflag)
    elif file.endswith(".cpp"):
        compilerlanguea(CPP_compiler_name, [CPP_compiler_name, file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".c"):
        compilerlanguea(C_compiler_name, [C_compiler_name, file, "-o", filename], ui, compile, file, klasor, terminal, flag, writeflag)
    elif file.endswith(".sh"):
        subprocess.Popen([terminal]+flag+[klasor]+["bash"]+[file])
    elif file.endswith(".js"):
        interpreterlanguage("node",["node",file],terminal,klasor,flag,writeflag)
    elif file.endswith(".java"):
        if shutil.which("javac") and shutil.which("java"):
            filename = os.path.splitext(os.path.basename(file))[0]
            java = subprocess.run(["javac",file],capture_output=True,text=True,cwd=klasor)
            if ui == True and compile == True and java.returncode == 0:
                QMessageBox.information(None,"Compile","Successfully compiled")
            elif java.returncode == 0 and compile == False:
                subprocess.Popen([terminal]+flag+[klasor]+["java",filename])
            elif java.returncode != 0:
                javaerror = java.stderr
                subprocess.Popen([terminal]+writeflag+[javaerror])
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
            subprocess.Popen([terminal]+flag+[klasor]+["dotnet","run",file])
        else:
            subprocess.Popen([terminal]+writeflag+["ERROR dotnet not found Please install dotnet"])
    elif file.endswith(".asm"):
        filename = os.path.splitext(os.path.basename(file))[0]
        if not shutil.which("nasm"):
            subprocess.Popen([terminal]+writeflag+["ERROR nasm not found Please install nasm "])
            return
        if not shutil.which("ld"):
            subprocess.Popen([terminal]+writeflag+["ERROR ld linker not found. Please install binutils."])
        assembly = subprocess.run(["nasm","-f","elf64",file,"-o",f"{filename}.o"],capture_output=True,text=True,cwd=klasor)
        if assembly.returncode == 0:
            ldassmebly = subprocess.run(["ld",f"{filename}.o","-o",filename],capture_output=True,text=True,cwd=klasor)
            if ldassmebly.returncode == 0 and compile ==False:
                subprocess.Popen([terminal]+flag+[klasor]+[f"./{filename}"])
            elif ldassmebly.returncode == 0 and compile == True and ui == True:
                QMessageBox.information(None,"Compile","Successfully compiled")
            elif ldassmebly.returncode != 0:
                lderror = ldassmebly.stderr
                subprocess.Popen([terminal]+writeflag+[klasor]+[lderror])
        else:
            assemblyerror = assembly.stderr
            subprocess.Popen([terminal]+writeflag+[assemblyerror])
    elif file.endswith(".ts"):
        interpreterlanguage("node",["npx","tsx",file],terminal,klasor,flag,writeflag)

    elif file.endswith(".kt"):
        compilerlanguea("kotlinc",["kotlinc",file,"-include-runtime","-d",f"{filename}.jar"],ui,compile,file,klasor,terminal,flag,writeflag,["java","-jar",f"{filename}.jar"])

    elif file.endswith(".jar"):
        if shutil.which("java"):
            subprocess.Popen([terminal]+flag+[klasor]+["java","-jar",file])
        else:
            subprocess.Popen([terminal]+writeflag+["ERROR java not found. Please install the JRE/JDK."])
    

        


    else:
        if ui is True:
            QMessageBox.critical(None,"File Type",f"unsupported file type:{file}")
        else:
            subprocess.Popen([terminal]+writeflag+[f"unsupported file type:{file}"])

def interpreterlanguage(langname,command,terminal,klasor,flag,writeflag):
    if shutil.which(langname):
        subprocess.Popen([terminal]+flag+[klasor]+command)
    else:
        subprocess.Popen([terminal]+writeflag+[f"Error {langname} not found Please install {langname}"])

def compilerlanguea(languagename,command,ui,compile,file,klasor,terminal,flag,writeflag,runcommand=None):
    filename = os.path.splitext(os.path.basename(file))[0]
    if runcommand == None:
        runcommand = [f"./{filename}"]
    if not shutil.which(languagename):
        subprocess.Popen([terminal]+writeflag+[f"ERROR {languagename} not found Please install {languagename}"])
        return
    language = subprocess.run(command,capture_output=True,text=True,cwd=klasor)
    if language.returncode == 0 and compile == False:
        subprocess.Popen([terminal]+flag+[klasor]+runcommand)
    elif compile == True and language.returncode == 0 and ui == True:
        QMessageBox.information(None,"Compile","Successfully compiled")
    elif language.returncode != 0:
        languageerror = language.stderr
        subprocess.Popen([terminal]+writeflag+[languageerror])

def decompilefile(file,ui=True):
    decompilercommand = []
    decompiler = "objdump"
    spath = os.path.expanduser("~/.config/runix")
    if not os.path.exists(spath):
        os.mkdir(spath)
    if os.path.exists(f"{spath}/Default_decompiler.txt"):
        with open(f"{spath}/Default_decompiler.txt","r",encoding="utf8") as f:
            decompiler = f.read()
    if decompiler == "retdec" and shutil.which("retdec-decompiler"):
        decompilercommand = ["retdec-decompiler"]
    else:
        outputfile = f"{file}.asm"
        decompilercommand = ["bash", "-c", f"objdump -d {file} > {outputfile}"]

    klasor = os.path.dirname(file)
    elf = subprocess.run(["file",file],capture_output=True,text=True,cwd=klasor)
    if "ELF" in elf.stdout:
        result = subprocess.run(decompilercommand+[file])
        if result.returncode == 0:
            subprocess.run(["notify-send","Decompile","The decompilation was successful"])
        elif result.returncode != 0:
            subprocess.run(["notify-send","Decompile","The decompilation process completed with errors"])
        
    elif file.endswith(".jar"):
        if shutil.which("jadx"):
            filename = os.path.splitext(os.path.basename(file))[0]
            outputfolder = f"{filename}_decompiled"
            jde = subprocess.run(["jadx",file,"-d",outputfolder],cwd=klasor)
            if jde.returncode != 0:
                subprocess.run(["notify-send","Decompile","The decompilation process completed with errors"])
            elif jde.returncode == 0:
                subprocess.run(["notify-send","Decompile","The decompilation was successful"])
        else:
            subprocess.run(["notify-send","Error","Jadx not found Please install Jadx"])
    else:
        subprocess.run(["notify-send","File type","This file type is not supported"])
        
        


            
        
        
    
if __name__ == "__main__":
    checkstartup()