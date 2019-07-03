from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.webhandler as webhandler
import modules.locations as locations

import tkinter as tk
from tkinter.constants import *
from tkinter import messagebox

import sys, subprocess, os, json

#archive handling
from zipfile import ZipFile

import pages.pagetemplate as pt

details_guide_text = """Welcome to the HBU CFW manager alpha. Use at your own risk.
This might wipe your SD card. It might kill your cat. It might cut up your driver's license.
Don't use this on anything but a fresh SD card for now.
I HAVE NOT TESTED COMPATIBILITY WHEN INSTALLING MORE THAN ONE PRIMARY FIRMWARE.

One of the big goals here is to allow easy updates or downgrades to custom firmwares while preserving patches and game mods.
""" 

class cfwPage(pt.page):
	def __init__(self, parent, controller,page_name,back_command):
		pt.page.__init__(self,
			parent=parent, 
			controller=controller,
			back_command=back_command,
			status_column="INSTALLED",
			page_title="CFW MANAGER",
			softwaregroup="cfw",
			page_name=page_name
			)

		cfwlist = self.populatesoftwarelist(locations.customfirmwarelist)
		self.setlist(cfwlist)

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
            "callback" : lambda: self.controller.raiseRepo(self.page_name,self.softwaregroup),
            "tooltip" : "Add github repo",
            },
		]

		self.setbuttons(buttonlist)

		self.console = cw.consolebox(self.content_frame)
		self.console.place(relx=0,rely=.7,relwidth=1, relheight=.3)
		self.console.print(details_guide_text)
		self.setguidetext(details_guide_text)