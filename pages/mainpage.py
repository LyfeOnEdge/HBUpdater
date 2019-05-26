from modules.format import * 
import modules.guicore as guicore
import modules.homebrewcore as homebrewcore
import modules.HBUpdater as HBUpdater

import pages.installerhelperpage as installerhelperpage
import pages.pagetemplate as pt

import tkinter as tk
from tkinter.constants import *

details_guide_text = """This menu will allow you to install older versions of apps, uninstall software, and go to the software's project page. Project pages are not currently supported for user-added content. 
""" 

class mainPage(pt.page):
    def __init__(self, parent, controller,back_command):
        pt.page.__init__(self,parent=parent, controller=controller,back_command=back_command,version_function=HBUpdater.checkversion)

        self.addrepoimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"plus.png")).subsample(2)
        self.sdimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"sd.png")).zoom(2).subsample(4)
        self.settingsimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"settings.png")).zoom(3).subsample(5)
        self.injectimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"injector.png")).zoom(3).subsample(5)
        self.nutimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"nut.png"))
        self.fluffyimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder, "fluffy.png")).zoom(3).subsample(5)
        self.pythonimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder, "python.png")).zoom(3).subsample(5)
        

        buttonlist = [
            {
            "image" : self.pythonimage,
            "callback" : lambda: self.controller.show_frame("pynxPage"),
            "tooltip" : "Python Homebrew for use with NX Python",
            },
            {
            "image" : self.fluffyimage,
            "callback" : self.checkfluffyandstart,
            "tooltip" : "Open fluffy server",
            },
            {
            "image" : self.nutimage,
            "callback" : self.checknutandstart,
            "tooltip" : "Open NUT server",
            },
            {
            "image" : self.injectimage,
            "callback" : lambda: self.controller.show_frame("injectorScreen"),
            "tooltip" : "Open RCM injector GUI",
            },
            {
            "image" : self.settingsimage,
            "callback" : lambda: self.controller.show_frame("settingsPage"),
            "tooltip" : "Open settings page",
            },
            {
            "image" : self.sdimage,
            "callback" : self.setSDpath,
            "tooltip" : "Select SD card",
            },
            {
            "image" : self.addrepoimage,
            "callback" : lambda: self.controller.show_frame("addRepoScreen"),
            "tooltip" : "Add github repo",
            },
        ]

        self.setbuttons(buttonlist)
        self.setlist(guicore.hblist)
        self.setguidetext(details_guide_text)

    def checknutandstart(self):
        if not installerhelperpage.checkifhelperdownloaded("nut"):
            installerhelperpage.seterrorstate("nut")
            self.controller.show_frame("installerHelperPage")
            return
        installerhelperpage.starthelper("nut")

    def checkfluffyandstart(self):
        if not installerhelperpage.checkifhelperdownloaded("fluffy"):
            installerhelperpage.seterrorstate("fluffy")
            self.controller.show_frame("installerHelperPage")
            return
        installerhelperpage.starthelper("fluffy")






        
        



