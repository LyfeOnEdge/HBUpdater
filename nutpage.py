import webhandler, homebrewcore, HBUpdater, locations, guicore
from zipfile import ZipFile
import sys, os, json, subprocess,imp
import threading
import tkinter as tk
import customwidgets as cw
from format import *

nutfolder = homebrewcore.get_path("nut")
if not os.path.isdir(nutfolder):
    os.mkdir(nutfolder)
    print("initializing nut folder")

class nutPage(tk.Frame,):
    def __init__(self, parent, controller,back_command):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)

        #page for warning users that nut isn't installed and asking if they want to install it
        self.nutinstallframe = cw.themedframe(self,frame_borderwidth=0,frame_highlightthickness=0)
        self.nutinstallframe.place(relwidth=1,relheight=1)
        self.nutreturnbutton = cw.navbutton(self.nutinstallframe, image_object=self.returnimage, command_name=self.controller.show_frame("mainPage"))
        self.nutreturnbutton.place(relx=1, rely=1, x=-(separatorwidth+navbuttonheight), y=-(separatorwidth+navbuttonheight), height=navbuttonheight, width=navbuttonheight)

        self.nutnotdownloadedwarningframe= cw.themedframe(self.nutinstallframe,frame_highlightthickness=0,frame_borderwidth=0)
        self.nutnotdownloadedwarningframe.place(relheight=1,relwidth=1)
        self.nutnotdownloadedwarning = cw.themedguidelabel(self.nutnotdownloadedwarningframe,"IT LOOKS LIKE YOU DON'T HAVE NUT DOWNLOADED YET,\n WOULD YOU LIKE TO DOWNLOAD IT AND INSTALL ITS DEPENDENCIES?",anchor="center")
        self.nutnotdownloadedwarning.place(relx=0.5,rely=0.5,x=-250, width=500,height=3*navbuttonheight,y=-(1.5*navbuttonheight))
        self.installnutbutton = cw.navbutton(self.nutnotdownloadedwarningframe, command_name=self.getnut,text_string="YES")
        self.installnutbutton.place(relx=0.5,rely=0.5,y=+(2*navbuttonheight + separatorwidth),width=100,x=-50)

        self.cancelbutton = cw.navbutton(self.nutnotdownloadedwarningframe, command_name=lambda: self.controller.show_frame("mainPage"),text_string="NO")
        self.cancelbutton.place(relx=0.5,rely=0.5,y=+(3*navbuttonheight + separatorwidth),width=100,x=-50)


        self.nutnotdownloadedwarningframe.tkraise()

    def getnut(self):
        downloadthread = threading.Thread(target=downloadnutandinstalldependencies)
        downloadthread.start()
        downloadthread.join()

        self.controller.show_frame("mainPage")
        startnut()



def installpipmodule(module):
    try:
        print("installing {} via pip".format(module))
        print(subprocess.call([sys.executable, "-m", "pip", "install", module]))
        return(True)
    except:
        print("Error installing module")
        return(False)
   
def checkifmoduleinstalled(module):
        try:
            imp.find_module(module)
            return True
        except ImportError:
            print("module {} not installed".format(module))
            return False

def checkifnutdownloaded():
    if guicore.checkguitag("nut", "version") == "not installed" or guicore.checkguitag("nut", "version") == "none":
        return False

    return True

def downloadnutandinstalldependencies():
    nutjson = webhandler.getJson("nut", locations.nutserverdict["githubapi"])
    with open(nutjson) as json_file: #jsonfile is path, json_file is file obj
        jfile = json.load(json_file)
        if jfile == [] or jfile == None:
            print("Error: empty json nut file")
            return

        zipurl = jfile[0]["zipball_url"]
        version = jfile[0]["tag_name"]
        if zipurl == None:
            print("zip file url invalid, can't download nut assets")

        nutzip = webhandler.download(zipurl)
        nutzip = homebrewcore.joinpaths(homebrewcore.downloadsfolder, nutzip)

        with ZipFile(nutzip, 'r') as zipObj:
            zipObj.extractall(nutfolder)
            print("Sucessfully extracted {} to nut folder\n".format(nutzip))

            extractedfiles = zipObj.namelist()

            serverfile = None
            for possibleserverfile in extractedfiles:
                if possibleserverfile == extractedfiles[0] + "server.py":
                    serverfile = possibleserverfile
            if serverfile == None:
                print("Could not find server file in extracted files")
                return 

            serverfile = homebrewcore.joinpaths(nutfolder, serverfile)

        newentry = {
            "nut" : {
                "version": version,
                "location": serverfile,
            }
        }
        guicore.updateguilog(newentry)

    print("checking nut dependencies")


    threads = []
    for dependency in locations.nutserverdict["dependencies"]:
        if not checkifmoduleinstalled(dependency):
            modulethread = threading.Thread(target=installpipmodule, args=(dependency,))
            threads.append(modulethread)

    # Start all threads
    if not threads == []:
        for thread in threads:
            thread.start()
        # Wait for all of them to finish
        for thread in threads:
            thread.join()

def startnut():
    if not checkifnutdownloaded():
        nutnotdownloadedwarningframe.tkraise()
        return
    script_path = guicore.checkguitag("nut", "location")
    print("starting nut server")
    subprocess.Popen([sys.executable,script_path])