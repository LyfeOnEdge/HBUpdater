import HBUpdater
from format import * 
import homebrewcore

import tkinter as tk
from tkinter.constants import *
import customwidgets as cw




class injectorScreen(tk.Frame):
	def __init__(self, parent, controller,back_command):
		tk.Frame.__init__(self,parent)

		#Full window frame, holds everything
		self.outer_frame = cw.themedframe(self)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

		self.infobox = cw.infobox(self.outer_frame)
		self.infobox.place(relx=1, x=-infoframewidth, rely=0.0, relheight=1, width=infoframewidth)

		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)

		self.injector_navigation =cw.navbox(self.infobox,
			primary_button_command = None,
			primary_button_text = "INJECT",
			etc_button_image = self.returnimage,
			etc_button_command = lambda: controller.show_frame("mainPage"),
			left_context_command = None,
			right_context_command = None,
			)
		self.injector_navigation.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)

		self.console = cw.consolebox(self)
		self.console.place(relx=0,rely=.7,relwidth=1, width =-infoframewidth,relheight=.3)

		def spewToTextOutput(self,textToSpew):
			self.textoutput.config(state=NORMAL)
			self.textoutput.insert(END, textToSpew + "\n\n")
			self.textoutput.config(state=DISABLED)
			self.textoutput.see(END)
			print(textToSpew)

		def spewBytesToTextOutput(self,textToSpew):
			self.textoutput.config(state=NORMAL)
			self.textoutput.insert(END, (textToSpew.decode("utf-8") + "\n\n"))
			self.textoutput.config(state=DISABLED)
			self.textoutput.see(END)
			print(textToSpew)