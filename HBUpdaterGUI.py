#This file sets up a frame manager that can be called by its children.
#It works by importing each primary frame as its own module, and stacking all of those frames
#A lower frame can be accessed by calling frame.tkraise()
#It also populates the arrays used by many of the pages
import os, sys, platform
import json
print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
	sys.exit("Python 3.6 or greater is required to run this program.")

version = "1.3"
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

#Main frame handler, raises and pages in z layer
class FrameManager(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# self.resizable(False,False)
		width = guicore.checkguisetting("dimensions","guiwidth")
		height = guicore.checkguisetting("dimensions","guiheight")
		minwidth = guicore.checkguisetting("dimensions","minguiwidth")
		minheight = guicore.checkguisetting("dimensions","minguiheight")
		self.geometry("{}x{}".format(width,height)) 
		self.minsize(width=minwidth, height=minheight) #minimum size currently supported
		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = cw.ThemedFrame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		##Import pages

		#App pages
		import pages.addrepopage as ar
		import pages.cfwpage as fw
		import pages.emulatorpage as eu
		import pages.gamespage as gp
		import pages.homebrewpage as hb
		import pages.pythonnxpage as py

		#Functional Pages:
		import pages.backuppage as bp
		import pages.injectorpage as ip
		import pages.serialpage as cp

		#Navigation Pages
		import pages.aboutpage as ap
		import pages.errorpage as ep
		import pages.homepage as lp
		import pages.settingspage as sp

		##Test pages, 
		#Uncomment this to see what I'm working on sometimes, especially in source builds.
		# import pages.test_page as tp 
		# import pages.dbviewer as db
		# import pages.usbhelper as ub
		# import pages.nut_tk.nut_tk as nk 
		#Add pages to list
		pages = [
			ep.errorPage,	#<- Needs to be inited before most pages, used for error handling to the user
			ar.addrepoPage,	#<- Needs to be inited before list pages, used for adding repos

			ap.aboutPage,		#<- No precedence
			bp.backupPage,		#<- List Page
			cp.serialPage,		#<- No precedence
			eu.emuPage,			#<- List Page
			fw.cfwPage,			#<- List Page
			gp.gamesPage,		#<- List Page
			hb.homebrewPage,	#<- List Page
			ip.injectorScreen,	#<- List Page
			lp.homePage,		#<- No precedence
			py.pynxPage,		#<- List Page
			sp.settingsPage,	#<- No precedence

		]

		#Try to add test page
		try:
			pages.append(tp.testPage)#<- List Page
			print("Test page added")
		except:
			pass


		#Add pages as frames to dict, with keyword being the name of the frame
		self.frames = {}
		for F in (pages):
			page_name = F.__name__
			frame = F(parent=container, controller=self,page_name=page_name,back_command = lambda: self.show_frame("homePage")) 
			self.frames[page_name] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		softwarelists = [
			self.frames["homebrewPage"].softwarelist,
			self.frames["gamesPage"].softwarelist,
			self.frames["emuPage"].softwarelist,
			self.frames["cfwPage"].softwarelist,
			self.frames["pynxPage"].softwarelist
		]

		mastersoftwarelist = []
		for lixlix in softwarelists:
			for lix in lixlix:
				mastersoftwarelist.append(lix)

		self.user_repos = self.frames["addrepoPage"].softwarelist
		
		#Set icon
		if platform.system() == 'Windows':
			try:
				print("Windows detected, setting icon")
				self.iconbitmap(os.path.join(guicore.assetfolder, 'HBUpdater.ico'))
			except:
				print("Failed to set icon")
		elif platform.system() == "Linux":
			try:
				print("Linux detected, setting icon")
				self.iconbitmap(os.path.join(guicore.assetfolder, 'HBUpdater.xbm'))
			except:
				print("Failed to set icon")
		
		latest_version, latest_notes = CheckForUpdates()
		if latest_version:
			self.frames["errorPage"].getanswer("homePage", "New release version {}\n\n{}\n Would you like to update?".format(latest_version, latest_notes), update)
		else: 
			self.show_frame("homePage") #Show the main page frame

	def raiseError(self,errortext,pagename):
		self.frames["errorPage"].raiseError(errortext,pagename)
		self.show_frame("errorPage")

	#Raising and lowering page with back commands
	def raiseRepo(self, return_screen, group):
		self.frames["addrepoPage"].raiseRepo(return_screen, group)
		self.show_frame("addrepoPage")

	def show_frame(self, page_name):
		#Show a frame for the given page name
		frame = self.frames[page_name]
		frame.event_generate("<<ShowFrame>>")
		frame.tkraise()

	def set_repos(self, repos):
		self.user_repos = repos

	
def stripversion(string):
	characterstostrip = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz()[]|-_/\\"
	for character in characterstostrip:
		string = string.replace(character,"")
	return string

def CheckForUpdates():
	if guicore.checkguisetting("guisettings","check_for_app_updates"):
		try:
			updatefile = webhandler.getJson("HBUpdater", locations.updateapi)
			if not updatefile:
				print("Failed to download HBU update file. A new version may be avaialable.")
				return
			else:
				with open(updatefile,encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
					jfile = json.load(json_file)
				newestversion = jfile[0]["tag_name"]
				description = jfile[0]["body"]
				if float(stripversion(newestversion)) > float(stripversion(version)):
					# print("A new update to HBUpdater is avaialable, go to https://www.github.com/LyfeOnEdge/HBUpdater/releases to download it.")
					return newestversion, description
				else:
					print("HBUpdater is up to date")
		except Exception as e:
			print("checkforupdateserror - {}".format(e))
	else:
		"update checking disabled"
	return None, None


def update():
	import modules.HBUUpdater as HBUU
	HBUU.update()
	sys.exit("Update complete, please re-start HBUpdater")

# def HandleUserAddedRepos():
if __name__ == '__main__':  
	gui = FrameManager()
	gui.title("HBUpdater {}".format(version))
	gui.mainloop()