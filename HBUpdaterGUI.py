#This file sets up a frame manager that can be called by its children.
#It works by importing each primary frame as its own module, and stacking all of those frames
#A lower frame can be accessed by calling frame.tkraise()
#It also populates the arrays used by many of the pages
import os, sys, platform
import json
print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    sys.exit("Python 3.6 or greater is required to run this program.")

version = "0.5 (BETA)"
print("HBUpdaterGUI version {}".format(version))

#My modules
import webhandler 
import homebrewcore
import guicore
import locations 
from format import * #We import format in this manner for simplicity's sake
import customwidgets as cw #Custom tkinter widgets
import HBUpdater #import backend, will not run standalone

import threading
import tkinter as tk
from tkinter.constants import *
print("using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))

#import pages for appManager (Needs to be done after dict is populated)
import injectorpage as ip
import mainpage as mp
import settingspage as sp
import addrepopage as ar
import installerhelperpage as hp
#Main frame handler, raises and pages in z layer
class FrameManager(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		if platform.system() == 'Windows':
			try:
				print("Windows detected, setting icon")
				self.iconbitmap(homebrewcore.joinpaths(homebrewcore.assetfolder, 'HBUpdater.ico'))
			except:
				print("Failed to set icon")
		elif platform.system() == "Linux":
			try:
				print("Linux detected, setting icon")
				self.iconbitmap(homebrewcore.joinpaths(homebrewcore.assetfolder, 'HBUpdater.xbm'))
			except:
				print("Failed to set icon")


		# self.resizable(False,False)
		self.geometry("790x510")   #startup size 720p
		self.minsize(width=790, height=510) #minimum size currently supported
		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self,
			borderwidth = 0,
			highlightthickness = 0
			)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		#Add frames to dict, with keyword being the name of the frame
		for F in (mp.mainPage,ip.injectorScreen,sp.settingsPage,ar.addRepoScreen,hp.installerHelperPage):
			page_name = F.__name__
			frame = F(parent=container, controller=self,back_command = lambda: self.controller.show_frame("mainPage")) 
			self.frames[page_name] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("mainPage") #Show the main page frame

	def show_frame(self, page_name):
		#Show a frame for the given page name
		frame = self.frames[page_name]
		frame.event_generate("<<ShowFrame>>")
		frame.tkraise()

def UseCachedJson():
	hbdict = webhandler.getJsonSoftwareLinks(locations.softwarelist)
	repodict = webhandler.getJsonSoftwareLinks(guicore.makerepodict())
	hbdict.extend(repodict)
	guicore.setDict(hbdict)
	guicore.setIJDict(webhandler.getJsonSoftwareLinks(locations.payloadlist))
	guicore.setPayloadInjector(webhandler.getJsonSoftwareLinks(locations.payloadinjector))

def GetUpdatedJson():
	hbdict = webhandler.getUpdatedSoftwareLinks(locations.softwarelist)
	repodict = webhandler.getUpdatedSoftwareLinks(guicore.makerepodict())
	hbdict.extend(repodict)
	guicore.setDict(hbdict)
	guicore.setIJDict(webhandler.getUpdatedSoftwareLinks(locations.payloadlist))
	guicore.setPayloadInjector(webhandler.getUpdatedSoftwareLinks(locations.payloadinjector))

# def HandleUserAddedRepos():
if __name__ == '__main__':  
	UseCachedJson() #use this to use only pre-downloaded json files
	#GetUpdatedJson() #use this to download new json (required to get updates)
	
	for softwarechunk in guicore.hbdict:
		softwarechunk["photopath"] = None

	gui = FrameManager()
	gui.title("HBUpdater")
	gui.mainloop()