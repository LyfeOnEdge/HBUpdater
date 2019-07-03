from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations

import os

import tkinter as tk
from tkinter.constants import *

pynxsubfolder = "switch\\PyNX"

import pages.pagetemplate as pt

class gamesPage(pt.page):
    def __init__(self, parent, controller,page_name,back_command):
        pt.page.__init__(self,parent=parent, 
            controller=controller,
            back_command=back_command,
            page_title="HOMEBREW GAMES",
            softwaregroup="game",
            page_name=page_name,
            )

        gameslist = self.populatesoftwarelist(locations.gameslist)
        self.setlist(gameslist)

        buttonlist = [
            {
            "image" : self.returnimage,
            "callback" : back_command,
            "tooltip" : "Back to main screen",
            },

            {
            "image" : self.sdimage,
            "callback" : self.setSDpath,
            "tooltip" : "Select SD card",
            },

            {
            "image" : self.addrepoimage,
            "callback" : lambda: self.controller.raiseRepo(self.page_name, self.softwaregroup),
            "tooltip" : "Add github repo",
            },
        ]

        self.setbuttons(buttonlist)