from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.homebrewcore as homebrewcore
import modules.webhandler as webhandler

import tkinter as tk
from tkinter.constants import *
from tkinter import messagebox

import subprocess, sys, json, os

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
	def __init__(self, parent, controller,back_command):
		pt.page.__init__(self,
			parent=parent, 
			controller=controller,
			back_command=back_command,
			primary_button_command=self.selfinstallcfw,
			secondary_button_command=self.selfinstallcfw,
			status_column="INSTALLED",
			page_title="CFW MANAGER",
			softwaregroup="cfw"
			)

		self.setlist(guicore.cfwlist)

		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)
		self.sdimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"sd.png")).zoom(2).subsample(4)

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

		
		self.uninstall_button.setcommand(self.selfuninstallcfw)

		self.console = cw.consolebox(self.content_frame)
		self.console.place(relx=0,rely=.7,relwidth=1, relheight=.3)
		self.console.print(details_guide_text)
		self.setguidetext(details_guide_text)

	def getCFWkey(self,software,key):
		cfwinfo = HBUpdater.getlogitem("cfw",software)
		if cfwinfo == None or cfwinfo == "not installed":
			return "not installed"
		return cfwinfo[key]

	def selfinstallcfw(self):
		if HBUpdater.sdpathset:
			software, cfwpackageurl, filename, version = self.getSoftwareURLbyPattern()
			if cfwpackageurl == None:
				print("No data, not installing")
				return
			installcfw(self, software, cfwpackageurl, filename, version)
			self.updatetable(None)
		else:
			self.setSDpath()
			if HBUpdater.sdpathset:
				self.selfinstallcfw()
			else:
				print("SD Path Not set, not installing")

	def selfuninstallcfw(self):
		if HBUpdater.sdpathset:
			software = self.softwarelist[self.currentselection]["software"]
			uninstallcfw(self, software)
			self.updatetable(None)
		else:
			self.setSDpath()
			if HBUpdater.sdpathset:
				self.selfuninstallcfw()
			else:
				print("SD Path Not set, not installing")


	def getSoftwareURLbyPattern(self):
		with open(self.softwarelist[self.currentselection]["githubjson"],encoding="utf-8") as json_file:
			jfile = json.load(json_file)
			softwarename = self.softwarelist[self.currentselection]["software"]
			version = jfile[self.currenttagselection]["tag_name"]

			assetindex = None
			pattern = self.softwarelist[self.currentselection]["pattern"]
			for asset in jfile[self.currenttagselection]["assets"]:
				asseturl = asset["browser_download_url"]
				assetname = asseturl.rsplit("/",1)[1].lower()
				assetwithoutfiletype = assetname.split(".")[0]
				for firstpartpattern in pattern[0]:
					if assetwithoutfiletype.startswith(firstpartpattern):
						if assetname.endswith(pattern[1].lower()):
							print("found asset: {}".format(assetname))
							print("asset url: {}".format(asseturl))
							return(softwarename,asseturl,assetname,version)
			print("No asset data found")
			return(None)


def installcfwtosd(filename,subfolder):
	if not subfolder == None:
		subdir = homebrewcore.joinpaths(HBUpdater.chosensdpath,subfolder)
	else: 
		subdir = HBUpdater.chosensdpath

	sdlocation = homebrewcore.joinpaths(subdir, filename)

	if not homebrewcore.direxist(subdir):
		os.mkdir(subdir)

	if filename.endswith(".zip"):
		#fw should always come in .zip
		with ZipFile(filename, 'r') as zipObj:
			# try:
				zipObj.extractall(subdir)
				sdlocation = zipObj.namelist()
				namelist = []
				for location in sdlocation:
					namelist.append(homebrewcore.joinpaths(subdir,location))
				print("files copied: \n {}".format(namelist))
				print("Sucessfully installed custom firmware {} to SD".format(filename))
				print(subdir)
				return namelist
	else:
		print("file handling method not found, file: {}".format(filename))
		return None


def installcfw(self, software, cfwpackageurl, filename, version):
	location = HBUpdater.getlogvalue("cfw", software, "location")

	print("installing {} version {}".format(software,version))
	downloadedfile = webhandler.downloadFileAs(cfwpackageurl,filename)

	if not downloadedfile == None:
		if not location == "not installed":
			#If previous install location is empty do nothing (this means it was never installed before)
			#This method also skips deleting folders to prevent folder structure damage
			removefiles(location)
			

		installlocation = installcfwtosd(downloadedfile, self.softwarelist[self.currentselection]["install_subfolder"])
		
		if not (installlocation) == None:
			newentry = {
				"software": software,
				"version": version,
				"location": installlocation,
			}
			print("updating installation tracker file with {}".format(json.dumps(newentry),indent=4))
			HBUpdater.updatelog("cfw",newentry)

def uninstallcfw(self, software):
	version = self.getlogvalue("cfw", software, "version")
	if version == None or version == "not installed":
		print("CFW not found, not uninstalling")
		return

	location = self.getlogvalue("cfw", software, "location")
	print("removing {}".format(software))

	if not removefiles(location):
		print("No files found to remove, this is probably a bug")

	newentry = {
		"software": software,
		"version": "not installed",
		"location": None,
	}

	print("updating installation tracker file with {}".format(json.dumps(newentry),indent=4))
	HBUpdater.updatelog("cfw",newentry)

#Removes a file or a list of files, returns false if nothing was found to remove
def removefiles(fileOrFiles):
	if not fileOrFiles == None:
		if type(fileOrFiles) is list:
			for loc in fileOrFiles:
				if  os.path.isfile(loc):
					os.remove(loc)
					print("removed old file {}".format(loc))
				else:
					if not os.path.isdir(loc):
						print("Could not find file to remove: {}".format(loc))
		elif type(fileOrFiles) is str:
			if  os.path.isfile(fileOrFiles):
				os.remove(fileOrFiles)
				print("removed {}".format(fileOrFiles))
			else:
				if not os.path.isdir(fileOrFiles):
					print("Could not find file to remove: {}".format(fileOrFiles))
	else:
		return False
	return True


