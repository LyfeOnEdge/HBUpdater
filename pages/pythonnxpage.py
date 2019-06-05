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

class pynxPage(pt.page):
	def __init__(self, parent, controller,back_command):
		pt.page.__init__(self,parent=parent, 
			controller=controller,
			back_command=back_command,
			page_title="PYTHON SCRIPTS",
			softwaregroup="pyscripts"
			)


		nxpylist = self.populatesoftwarelist(locations.nxpythonlist)
		self.setlist(nxpylist)


		self.pythonimage = tk.PhotoImage(file=os.path.join(locations.assetfolder, "python.png")).zoom(3).subsample(5)
		self.sdimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"sd.png")).zoom(2).subsample(4)

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
		]

		self.setbuttons(buttonlist)