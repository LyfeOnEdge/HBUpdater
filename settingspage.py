import HBUpdater
from format import * 
import homebrewcore
import webhandler

import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog
import customwidgets as cw

# import json



class settingsPage(tk.Frame):
	def __init__(self, parent, controller,back_command):
		tk.Frame.__init__(self,parent)

		#Full window frame, holds everything
		self.outer_frame = cw.themedframe(self)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

		#back to main page button
		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)
		self.backtomain_button = cw.navbutton(self.outer_frame, image_object=self.returnimage, command_name=lambda: controller.show_frame("mainPage"))
		self.backtomain_button.place(relx=1, rely=1, x=-(self.returnimage.width() + 20), y=-(self.returnimage.height()+20), height=self.returnimage.height(), width=self.returnimage.width())

		