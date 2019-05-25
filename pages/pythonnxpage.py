from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.homebrewcore as homebrewcore
import modules.locations as locations
import modules.webhandler as webhandler


import tkinter as tk
from tkinter.constants import *

pynxsubfolder = "switch\\PyNX"

import pages.pagetemplate as pt

class pynxPage(pt.page):
	def __init__(self, parent, controller,back_command):
		pt.page.__init__(self,parent=parent, controller=controller,back_command=back_command)
		self.setlist(guicore.nxpylist)

		self.pythonimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder, "python.png")).zoom(3).subsample(5)
		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)

		buttonlist = [
			{
			"image" : self.returnimage,
			"callback" : back_command,
			"tooltip" : "Back to main screen",
			}
		]

		self.setbuttons(buttonlist)