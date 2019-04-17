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
		self.infobox.place(relx=1, x=-infoframewidth, rely=0.0, relheight=.999, width=infoframewidth)


		self.installimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"installbutton.png")).zoom(3).subsample(5)
		self.infoimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"info.png")).zoom(3).subsample(5)
		self.previousimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"prev.png")).zoom(3).subsample(5)
		self.nextimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"next.png")).zoom(3).subsample(5)
		self.backbutton = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"back.png")).zoom(3).subsample(5)
		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)

		self.injector_navigation =cw.navbox(self.infobox,
			primary_button_image = self.installimage,
			primary_button_command = None,
			etc_button_image = self.returnimage,
			etc_button_command = lambda: controller.show_frame("mainPage"),
			left_context_image = self.previousimage,
			left_context_command = None,
			right_context_image = self.nextimage,
			right_context_command = None,
			)
		self.injector_navigation.place(relx=.5, rely=1, x=-100, y=-87.5, height= 75, width=200)



		self.textoutheight = 10
		self.textoutputwidth = 50
		self.textoutput = tk.Text(self.outer_frame, height=self.textoutheight, width = 50, font=smalltext)
		self.textoutput.place(relx=0,rely=.7,relwidth=.6,relheight=.3)
		self.textoutput.configure(background = b)
		self.textoutput.configure(foreground = w)
		self.textoutput.configure(state=DISABLED)
		self.textoutput.configure(borderwidth = 0)

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