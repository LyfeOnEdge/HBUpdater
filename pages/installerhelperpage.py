from modules.format import *
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.homebrewcore as homebrewcore
import modules.locations as locations
import modules.webhandler as webhandler

from zipfile import ZipFile
import sys, os, json, subprocess, imp, shutil, threading
import tkinter as tk


nutfolder = homebrewcore.get_path("nut")
if not os.path.isdir(nutfolder):
    os.mkdir(nutfolder)
    print("initializing nut folder")

fluffyfolder = homebrewcore.get_path("fluffy")
if not os.path.isdir(fluffyfolder):
    os.mkdir(fluffyfolder)
    print("initializing fluffy folder")

errorstate = None

class installerHelperPage(tk.Frame,):
    def __init__(self, parent, controller,back_command):
        tk.Frame.__init__(self,parent)
        self.bind("<<ShowFrame>>", self.on_show_frame)
        self.controller=controller

        self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)

        #page for warning users that nut isn't installed and asking if they want to install it
        self.installerwarningframe = cw.themedframe(self,)
        self.installerwarningframe.place(relwidth=1,relheight=1)
        self.returnbutton = cw.navbutton(self.installerwarningframe, image_object=self.returnimage, command_name=self.controller.show_frame("mainPage"))
        self.returnbutton.place(relx=1, rely=1, x=-(separatorwidth+navbuttonheight), y=-(separatorwidth+navbuttonheight), height=navbuttonheight, width=navbuttonheight)

        self.nutnotdownloadedwarningframe= cw.themedframe(self.installerwarningframe)
        self.nutnotdownloadedwarningframe.place(relheight=1,relwidth=1)
        self.nutnotdownloadedwarning = cw.themedguidelabel(self.nutnotdownloadedwarningframe,"IT LOOKS LIKE YOU DON'T HAVE NUT DOWNLOADED YET,\n WOULD YOU LIKE TO DOWNLOAD IT AND INSTALL ITS DEPENDENCIES?",anchor="center")
        self.nutnotdownloadedwarning.place(relx=0.5,rely=0.5,x=-250, width=500,height=3*navbuttonheight,y=-(1.5*navbuttonheight))
        self.installnutbutton = cw.navbutton(self.nutnotdownloadedwarningframe, command_name=self.getnut,text_string="YES")
        self.installnutbutton.place(relx=0.5,rely=0.5,y=+(2*navbuttonheight + separatorwidth),width=100,x=-50)
        self.nutcancelbutton = cw.navbutton(self.nutnotdownloadedwarningframe, command_name=lambda: self.controller.show_frame("mainPage"),text_string="NO")
        self.nutcancelbutton.place(relx=0.5,rely=0.5,y=+(3*navbuttonheight + separatorwidth),width=100,x=-50)


        self.fluffynotdownloadedwarningframe= cw.themedframe(self.installerwarningframe)
        self.fluffynotdownloadedwarningframe.place(relheight=1,relwidth=1)
        self.fluffynotdownloadedwarning = cw.themedguidelabel(self.fluffynotdownloadedwarningframe,"IT LOOKS LIKE YOU DON'T HAVE FLUFFY DOWNLOADED YET,\n WOULD YOU LIKE TO DOWNLOAD IT AND INSTALL ITS DEPENDENCIES?",anchor="center")
        self.fluffynotdownloadedwarning.place(relx=0.5,rely=0.5,x=-250, width=500,height=3*navbuttonheight,y=-(1.5*navbuttonheight))
        self.installfluffybutton = cw.navbutton(self.fluffynotdownloadedwarningframe, command_name=self.getfluffy,text_string="YES")
        self.installfluffybutton.place(relx=0.5,rely=0.5,y=+(2*navbuttonheight + separatorwidth),width=100,x=-50)
        self.fluffycancelbutton = cw.navbutton(self.fluffynotdownloadedwarningframe, command_name=lambda: self.controller.show_frame("mainPage"),text_string="NO")
        self.fluffycancelbutton.place(relx=0.5,rely=0.5,y=+(3*navbuttonheight + separatorwidth),width=100,x=-50)

       
        self.nutnotdownloadedwarningframe.tkraise()


    def on_show_frame(self,event):
        global errorstate
        if errorstate == "nut":
            self.nutnotdownloadedwarningframe.tkraise()
        if errorstate == "fluffy":
            self.fluffynotdownloadedwarningframe.tkraise()


    def getnut(self):
        downloadNUTandinstalldependencies()

        self.controller.show_frame("mainPage")
        starthelper("nut")

    def getfluffy(self):
        downloadFLUFFYandinstalldependencies()
        self.controller.show_frame("mainPage")
        starthelper("fluffy")

def seterrorstate(state):
    global errorstate
    errorstate = state

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

def installmodulelist(modules):
    threads = []
    for module in modules:
        if not checkifmoduleinstalled(module):
            modulethread = threading.Thread(target=installpipmodule, args=(module,))
            threads.append(modulethread)

    # Start all threads
    if not threads == []:
        for thread in threads:
            thread.start()
        # Wait for all of them to finish
        for thread in threads:
            thread.join()


def checkifhelperdownloaded(helper):
    if guicore.checkguisetting(helper, "version") == "not installed" or guicore.checkguisetting(helper, "version") == None:
        return False
    else:
        print(guicore.checkguisetting(helper, "version"))
        return True
    return False

def starthelper(helper):
    if not checkifhelperdownloaded(helper):
        nutnotdownloadedwarningframe.tkraise()
        print("not installed")
        return
    script_path = guicore.checkguisetting(helper, "location")
    print("starting {} server at {}".format(helper,script_path))
    if script_path == None:
        print("invalid path")
        return
    subprocess.Popen([sys.executable,script_path])

def downloadNUTandinstalldependencies():
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
        guicore.setguisetting(newentry)

    print("checking nut dependencies")

    dependencies = locations.nutserverdict["dependencies"]
    installmodulelist(dependencies)

def downloadFLUFFYandinstalldependencies():
    fluffyjson = webhandler.getJson("fluffy", locations.fluffydict["githubapi"])
    with open(fluffyjson) as json_file: #jsonfile is path, json_file is file obj
        jfile = json.load(json_file)
        if jfile == [] or jfile == None:
            print("Error: empty json nut file")
            return

        scripturl = jfile[0]["assets"][0]["browser_download_url"]
        licenseurl = jfile[0]["assets"][1]["browser_download_url"]
        version = jfile[0]["tag_name"]

        #download and move fluffy and license
        script = webhandler.download(scripturl)
        license = webhandler.download(licenseurl)
        scriptpath = homebrewcore.joinpaths(homebrewcore.downloadsfolder, script)
        licensepath = homebrewcore.joinpaths(homebrewcore.downloadsfolder, license)
        newscriptpath = homebrewcore.joinpaths(fluffyfolder, script)
        newlicensepath = homebrewcore.joinpaths(fluffyfolder, license)
        shutil.move(scriptpath,newscriptpath)
        shutil.move(licensepath,newlicensepath)

        newentry = {
            "fluffy" : {
                "version": version,
                "location": newscriptpath,
            }
        }
        guicore.setguisetting(newentry)

    print("checking and installing fluffy dependencies")

    threads = []
    dependencies = locations.fluffydict["dependencies"]
    installmodulelist(dependencies)
