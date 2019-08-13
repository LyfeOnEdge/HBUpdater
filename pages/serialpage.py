from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.serial_checker as sc
import modules.webhandler as webhandler
import modules.locations as locations
import os, shutil, sys, subprocess, json
from zipfile import ZipFile

import tkinter as tk
from tkinter.constants import *

import pages.errorpage as errorpage

serialboxheight = 90
serialboxwidth = 500

page_name = "serialPage"

class serialPage(cw.ThemedFrame):
	def __init__(self, parent, controller,page_name,back_command):
		self.back_command = back_command
		self.controller = controller
		self.activestatus = False

		cw.ThemedFrame.__init__(self,parent,background_color= light_color)
		self.bind("<<ShowFrame>>", self.on_show_frame) #Bind on_show_frame to showframe event

		self.outerframe = cw.ThemedFrame(self, background_color = light_color)
		self.outerframe.place(x=0,y=0,relwidth=1,relheight=1)

		self.returnimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)
		self.returnbutton = cw.navbutton(self.outerframe,command_name=self.back,image_object=self.returnimage)
		self.returnbutton.place(relx=1,rely=1,x=-2*navbuttonheight,y=-2*navbuttonheight,width=navbuttonheight,height=navbuttonheight)

		self.serialentry = cw.entrybox(self.outerframe, command=self.check, entry_font=mondoboldtext, placeholder="Enter Switch Serial Number",justification="center")
		self.serialentry.place(relx=0.5,rely=.5, x=-0.5*serialboxwidth, y=-0.5*serialboxheight, width=serialboxwidth, height=serialboxheight)
		self.serialentry.entry.bind("<KeyRelease>", self.on_key)

		self.serialstatus = cw.ThemedLabel(self,None,anchor="center",label_font=hugeboldtext)
		self.serialstatus.place(relx=0.5,rely=.5, x=-0.5*serialboxwidth, y=+0.5*serialboxheight,width=serialboxwidth)


	def on_show_frame(self,event):
		self.serialentry.enable()
		self.activestatus = True

	def on_key(self,event):
		if self.activestatus:
			entrytext = self.serialentry.get()
			self.check(entrytext)

	def check(self,serial):
		status = checkserial(serial)
		self.serialstatus.set("Serial Status - {}".format(status))

	def back(self):
		self.serialentry.disable()
		self.activestatus = False
		self.back_command()

def checkserial(serial):
	status = sc.checkserial(serial)
	print(status)
	return status