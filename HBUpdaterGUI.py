#This file sets up a frame manager that can be called by its children.
#It works by importing each primary frame as its own module, and stacking all of those frames
#A lower frame can be accessed by calling frame.tkraise()
#It also populates the arrays used by many of the pages
import os, sys, platform
import json
print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
	sys.exit("Python 3.6 or greater is required to run this program.")

version = "0.9 (Beta)"
print("HBUpdaterGUI version {}".format(version))

#My modules
from modules.format import * #We import format in this manner for simplicity's sake
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater #import backend, will not run standalone
import modules.locations as locations
import modules.webhandler as webhandler

#Need to check if pil and set status before importing customwidgets
if webhandler.checkifmoduleinstalled("PIL"):
	print("pillow detected, using improved scaling method")
	guicore.setpilstatus(True)
else:
	print("pillow not detected, using standard picture scaling method")
	guicore.setpilstatus(False)
import modules.customwidgets as cw #Custom tkinter widgets

import threading
import tkinter as tk
from tkinter import filedialog
from tkinter.constants import *
print("using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))

errorstate = None

#Main frame handler, raises and pages in z layer
class FrameManager(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# self.resizable(False,False)
		self.geometry("790x510")   #startup size 720p
		self.minsize(width=790, height=510) #minimum size currently supported
		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = cw.themedframe(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#import pages
		import pages.injectorpage as ip
		import pages.mainpage as mp
		import pages.settingspage as sp
		import pages.addrepopage as ar
		import pages.pythonnxpage as py
		import pages.cfwpage as fw
		import pages.errorpage as ep
		import pages.homepage as lp
		import pages.gamespage as gp
		import pages.serialpage as cp

		self.frames = {}
		#Add frames to dict, with keyword being the name of the frame
		for F in (mp.mainPage,ip.injectorScreen,sp.settingsPage,ar.addRepoScreen,py.pynxPage,fw.cfwPage,ep.errorPage,lp.homePage,gp.gamesPage,cp.serialPage):
			page_name = F.__name__
			frame = F(parent=container, controller=self,back_command = lambda: self.show_frame("homePage")) 
			self.frames[page_name] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		if platform.system() == 'Windows':
			try:
				print("Windows detected, setting icon")
				self.iconbitmap(os.path.join(locations.assetfolder, 'HBUpdater.ico'))
			except:
				print("Failed to set icon")
		elif platform.system() == "Linux":
			try:
				print("Linux detected, setting icon")
				self.iconbitmap(os.path.join(locations.assetfolder, 'HBUpdater.xbm'))
			except:
				print("Failed to set icon")

		self.bind("<<error>>", self.on_error)
		self.show_frame("homePage") #Show the main page frame

	def on_error(self,event):
		global errorstate
		self.frames["errorPage"].raiseError(errorstate)
		self.show_frame("errorPage")

	def seterrorstate(self,state):
		global errorstate
		errorstate = state

	def show_frame(self, page_name):
		#Show a frame for the given page name
		frame = self.frames[page_name]
		frame.event_generate("<<ShowFrame>>")
		frame.tkraise()
	
def stripversion(string):
	characterstostrip = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz()-"
	for character in characterstostrip:
		string = string.replace(character,"")
	return string

def CheckForUpdates():
	updatefile = webhandler.getJson("HBUpdater", locations.updateapi)
	if updatefile == None:
		print("Failed to download HBU update file. A new version may be avaialable.")
	else:
		with open(updatefile,encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
			newestversion = jfile[0]["tag_name"]
		if float(stripversion(newestversion)) > float(stripversion(version)):
			print("A new update to HBUpdater is avaialable, go to https://www.github.com/LyfeOnEdge/HBUpdater/releases to download it.")
		else:
			print("HBUpdater is up to date")

# def HandleUserAddedRepos():
if __name__ == '__main__':  
	if guicore.checkguisetting("guisettings","automatically_check_for_updates"):
		CheckForUpdates()
	else:
		print("Update checking diabled")

	gui = FrameManager()
	gui.title("HBUpdater {}".format(version))
	gui.mainloop()
