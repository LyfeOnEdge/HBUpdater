from modules.format import * 
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import pages.pagetemplate as pt

import os

import tkinter as tk
from tkinter.constants import *

details_guide_text = """This menu will allow you to install expermental content. These mat require additional setup. Please visit the homebrew's project page or github for more information.". 
""" 

class experimentalPage(pt.page):
    def __init__(self, parent, controller,back_command):
        pt.page.__init__(self,parent=parent, 
            controller=controller,
            back_command=back_command,
            softwaregroup = "experimental",
            page_title="EXPERIMENTAL",
            )

        experimentaldict = locations.experimentallist
        experimentaldict = self.populatesoftwarelist(experimentaldict)
        self.setlist(experimentaldict)

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

        ]

        self.setbuttons(buttonlist)

        self.setguidetext(details_guide_text)







        
        



