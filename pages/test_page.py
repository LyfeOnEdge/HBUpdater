from modules.format import * 
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import pages.pagetemplate as pt

import os

import tkinter as tk
from tkinter.constants import *

details_guide_text = """test""" 

class testPage(pt.page):
    def __init__(self, parent, controller,page_name,back_command):
        pt.page.__init__(self,parent=parent, 
            controller=controller,
            back_command=back_command,
            primary_button_command=self.test_function,
            primary_button_text="TEST",
            page_title="PUSHTHEBUTTON",
            page_name=page_name,
            # version_function=self.get_store_installed_version
            )

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


    def test_function(self):
        HBUpdater.startup_tracking_file_generation()
