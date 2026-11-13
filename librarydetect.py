import os
import shutil
import json

class library:
    def __init__(self):
        self.confdir = os.path.expanduser("~/.config/runix")
        self.librarydict = {"library":["#include <QApplication>","#include <GLFW/glfw3.h>","#include <vulkan/vulkan.h>","#include <gtk/gtk.h>","#include <math.h>","#include <curl/curl.h>"
        ,"#include <SFML/Graphics.hpp>","#include <SDL2/SDL.h>","#include <ncurses.h>"],
        "library-command":["pkg-config:Qt6Widgets|Qt5Widgets","-lglfw  -lGL  -ldl","-lvulkan","pkg-config:gtk4|gtk+-3.0","-lm","pkg-config:libcurl","pkg-config:sfml-all|sfml-graphics",
        "pkg-config:sdl2","pkg-config:ncurses|-lncurses"],"file_ext_(-Fpic)":(".cpp",".c")}

        self.createfile()


    def createfile(self,jsondata=None):
        if not os.path.exists(self.confdir):
            os.mkdir(self.confdir)
        if not os.path.exists(f"{self.confdir}/librarys.json"):
            try:
                with open(f"{self.confdir}/librarys.json","w",encoding="utf8") as b:
                    json.dump(self.librarydict,b) 
            except (OSError,json.JSONDecodeError,KeyError):
                return
        if jsondata != None:
            try:
                with open(f"{self.confdir}/librarys.json","a") as n:
                    json.dump(jsondata,n)
            except (OSError,json.JSONDecodeError,KeyError):
                return

    def detectlibrary(self,file):
        try:
            confdir = os.path.expanduser("~/.config/runix")
            result = []
            with open(f"{confdir}/librarys.json","r") as f:
                raw_data = json.load(f)
            filelibrary = raw_data["library"]
            filelibrarycommand = raw_data["library-command"]
            with open(file,"r") as b:
                filedata = b.read()
            for i, item in enumerate(filelibrary):
                if item in filedata:
                    result.append(filelibrarycommand[i])
            return result
                        

        except (FileNotFoundError,json.JSONDecodeError,KeyError,OSError):
            return None
    def addcustomlibrary(self,libraryname,library_command,fileexntFpic=None):
        try:
            if os.path.exists(f"{self.confdir}/librarys.json"):
                with open(f"{self.confdir}/librarys.json","r") as s:
                    rawdata = json.load(s)
                file_library_name = rawdata["library"]
                file_library_command = rawdata["library-command"]
                file_library_name.append(libraryname)
                file_library_command.append(library_command)
                file_ext_fpiclist = rawdata["file_ext_(-Fpic)"]
                if fileexntFpic != None:
                    file_ext_fpiclist.append(fileexntFpic)
                librarydict = {"library":file_library_name,"library-command":file_library_command,"file_ext_(-Fpic)":file_ext_fpiclist}
                with open(f"{self.confdir}/librarys.json","w") as m:
                    json.dump(librarydict,m)
        except (FileNotFoundError,json.JSONDecodeError,KeyError,OSError):
            return None

    def getfpicfileext(self):
        try:
            if os.path.exists(f"{self.confdir}/librarys.json"):
                with open(f"{self.confdir}/librarys.json","r") as n:
                    rawdata = json.load(n)
                data = rawdata["file_ext_(-Fpic)"]
                return data
        except (FileNotFoundError,json.JSONDecodeError,KeyError,OSError):
            return None



            
