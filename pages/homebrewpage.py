from modules.format import * 
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import pages.pagetemplate as pt

import os

import tkinter as tk
from tkinter.constants import *

details_guide_text = """This menu will allow you to install older versions of apps, uninstall software, and go to the software's project page. Project pages are not currently supported for user-added content. 
""" 

class homebrewPage(pt.page):
    def __init__(self, parent, controller,page_name,back_command):
        pt.page.__init__(self,parent=parent, 
            controller=controller,
            back_command=back_command,
            softwaregroup = "homebrew",
            page_title="HOMEBREW APPS",
            page_name=page_name,
            )

        hblist = locations.softwarelist
        repodict = guicore.makerepodict()
        hblist.extend(repodict)

        hblist = self.populatesoftwarelist(hblist)
        self.setlist(hblist)


        self.addrepoimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"plus.png")).subsample(2)
        self.sdimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"sd.png")).zoom(2).subsample(4)
        

        buttonlist = [
            {
            "image" : self.returnimage,
            "callback" : back_command,
            "tooltip" : "Back to home screen",
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

        self.setguidetext(details_guide_text)







        
        



