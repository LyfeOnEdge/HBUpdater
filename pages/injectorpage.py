from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import modules.webhandler as webhandler


import tkinter as tk
from tkinter.constants import *
from tkinter import messagebox

import os, sys, subprocess, json

#archive handling
from zipfile import ZipFile

import pages.pagetemplate as pt




details_guide_text = """This menu will allow you to install older versions of payload, and go to the payloads's project page.
""" 

class injectorScreen(pt.page):
	def __init__(self, parent, controller,page_name,back_command):
		pt.page.__init__(self, parent=parent, 
			controller=controller,
			back_command=back_command,
			primary_button_command=self.injectpayload,
			primary_button_text="INJECT",
			secondary_button_command=self.downloadpayload,
			secondary_button_text="DOWNLOAD",
			version_function=self.checkpayloadversion,
			status_column="DOWNLOADED",
			page_title="PAYLOAD INJECTOR",
			page_name=page_name
			)

		self.ijlist = self.populatesoftwarelist(locations.payloadlist)
		self.setlist(self.ijlist)

		self.pjlist = self.populatesoftwarelist(locations.payloadinjector)

		buttonlist = [
			{
			"image" : self.returnimage,
			"callback" : back_command,
			"tooltip" : "Back to home screen",
			}
		]

		self.setbuttons(buttonlist)

		#hacky hiding of uninstall button and move in project page button to fill
		self.uninstall_button.place(relx=2,rely=2)
		self.project_page_button.place(relx=0, rely=1, y=-3*(navbuttonheight+separatorwidth), height=navbuttonheight, x=+separatorwidth,relwidth=1, width=-(2*separatorwidth))

		self.console = cw.consolebox(self.content_frame)
		self.console.place(relx=0,rely=.7,relwidth=1, relheight=.3)
		self.printtoconsolebox("Connect switch, select payload, and press inject.\nThe payload and injector will be downloaded from github if they haven't been already.\n")
		self.printtoconsolebox("Injector backend: fusee-launcher, written by ktempkin\n")

		#Check if fusee launcher is download, display status for user
		fuseestatus = guicore.checkguisetting("fusee-launcher","version")
		notinstalled = [None, "not installed"]
		if fuseestatus in notinstalled:
			fuseestatus = "needs downloaded"
		else:
			fuseestatus = "downloaded"

		self.printtoconsolebox("Injector status: {}\n".format(fuseestatus))




		self.updatetable(None)

		self.setguidetext(details_guide_text)


	def printtoboth(self,stringtoprint):
		self.console.print(stringtoprint)
		print(stringtoprint)

	def printtoconsolebox(self,stringtoprint):
		self.console.print(stringtoprint)

	def injectpayload(self,event=None):
		if not webhandler.checkifmoduleinstalled("pyusb"):
			resp =  tk.messagebox.askyesno("Install PyUSB?", "PyUSB is required for fusee-launcher to work, install?")
			if resp:
				try:
					webhandler.installpipmodule("pyusb")
				except:
					self.printtoboth("Unknown error installing PyUSB")
					return
			else:
				self.printtoboth("Got answer: no, not installing")
				return

		payload = self.getordownloadpayload()


		injectpayload(self,payload)

	def checkpayloadversion(self,softwarename):
		version = guicore.checkguisetting(softwarename,"version")
		if version == None or version =="not installed":
			return("needs download")
		else:
			return version
		return version

	def getordownloadpayload(self):
		if not os.path.isdir(locations.payloadsfolder):
				os.mkdir(locations.payloadsfolder)

		softwarename = self.softwarelist[self.currentselection]["software"]
		if guicore.checkguisetting(softwarename,"version") == None or guicore.checkguisetting(softwarename,"version") =="not installed":
			self.printtoboth("payload not yet downloaded, downloading...")
			try:
				with open(self.softwarelist[self.currentselection]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
					jfile = json.load(json_file)
					version = jfile[self.currenttagselection]["tag_name"]
			except:
				print("Failed to find repo json file, can't install.")
				return

			#default asset number
			assetnumber = 0
			if not self.softwarelist[self.currentselection]["github_asset"] == None:
				#if the asset we are going for is not the default (eg it is set in locations.py under github_asset) update the assetnumber
				assetnumber = self.softwarelist[self.currentselection]["github_asset"]

			#get the download url for the payload we are going for
			downloadurl = jfile[self.currenttagselection]["assets"][assetnumber]["browser_download_url"]
			self.printtoboth("downloading payload from {}".format(downloadurl))

			#file yielded by the download
			file = webhandler.download(downloadurl)
			file = os.path.join(locations.downloadsfolder, file) #get absolute path to it
				
			#if downloaded file is already .bin, set the payload path to it.
			if file.endswith(".bin"):
				payload = file
				
			elif file.endswith(".zip"):
				#if file is zip, unzip it and find the payload based on the pattern set in its entry in #locations
				with ZipFile(file, 'r') as zipObj:
					zipObj.extractall(locations.payloadsfolder)
					self.printtoboth("Sucessfully extracted {} to payloads folder\n\n".format(file))
					files = zipObj.namelist()
					payload = None
					for possiblepayloadfile in files:
						if possiblepayloadfile.startswith(self.softwarelist[self.currentselection]["zip_items"]):
							payload = possiblepayloadfile
					if payload == None:
						self.printtoboth("Could not find payload in extracted files")
						return 
				payload = os.path.join(locations.payloadsfolder,payload)

			else:
				self.printtoboth("file handling method not found")
				return

			#prep new entry to the gui log
			newentry = {
						softwarename: {
							"version": version,
							"location": payload,
						}
					}
			guicore.setguisetting(newentry)
			self.updatetable(None)

		#If payload is already downloaded and up-to-date
		else:
			payload = guicore.checkguisetting(softwarename,"location")

		return payload

	def downloadpayload(self):
		if not os.path.isdir(locations.payloadsfolder):
				os.mkdir(locations.payloadsfolder)

		with open(self.softwarelist[self.currentselection]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
			softwarename = self.softwarelist[self.currentselection]["software"]
			version = jfile[self.currenttagselection]["tag_name"]
			self.printtoboth("Downloading {}".format(softwarename))

			#default asset number
			assetnumber = 0

			if not self.softwarelist[self.currentselection]["github_asset"] == None:
				#if the asset we are going for is not the default (eg it is set in locations.py under github_asset) update the assetnumber
				assetnumber = self.softwarelist[self.currentselection]["github_asset"]

			#get the download url for the payload we are going for
			downloadurl = jfile[self.currenttagselection]["assets"][assetnumber]["browser_download_url"]
			self.printtoboth("downloading payload from {}".format(downloadurl))

			#file yielded by the download
			file = webhandler.download(downloadurl)
			file = os.path.join(locations.downloadsfolder, file) #get absolute path to it
				
			#if downloaded file is already .bin, set the payload path to it.
			if file.endswith(".bin"):
				payload = file
				
			elif file.endswith(".zip"):
				#if file is zip, unzip it and find the payload based on the pattern set in its entry in #locations
				with ZipFile(file, 'r') as zipObj:
					zipObj.extractall(locations.payloadsfolder)
					self.printtoboth("Sucessfully extracted {} to payloads folder\n\n".format(file))
					files = zipObj.namelist()
					payload = None
					for possiblepayloadfile in files:
						if possiblepayloadfile.startswith(self.softwarelist[self.currentselection]["zip_items"]):
							payload = possiblepayloadfile
					if payload == None:
						self.printtoboth("Could not find payload in extracted files")
						return 

				payload = os.path.join(locations.payloadsfolder,payload)

			else:
				self.printtoboth("file handling method not found")
				return

			#prep new entry to the gui log
			newentry = {
						softwarename: {
							"version": version,
							"location": payload,
						}
					}
			guicore.setguisetting(newentry)
			self.updatetable(None)






#Redefinitions of class functions for page specific stuff
#This is so the gui remembers the last selected payload
	#Update page whenever it is raised
	def on_show_frame(self,event):
		self.currentselection = guicore.checkguisetting("last_payload", "selection")

		#Update with user repos
		if self.softwaregroup:
			self.softwarelist = self.basesoftwarelist[:]
			user_repos = self.controller.user_repos
			user_repos = guicore.getreposbygroupfromlist(self.softwaregroup, user_repos)
			#Add repos if they are found
			if user_repos:
				self.softwarelist.extend(user_repos)
			

		self.refreshwindow()
		self.updateinfobox()




	#movement button / cursor callbacks, moves up or down main list
	#get current selection from list box
	def CurSelet(self, event):
		try:
			widget = event.widget
			selection=widget.curselection()
			picked = widget.get(selection[0])
			self.currentselection = widget.get(0, "end").index(picked)
			self.currenttagselection = 0
			self.updateinfobox()
			self.refreshdetailwindow()
			guicore.setguisetting({"last_payload": {"selection": self.currentselection}},silent = True)
		except:
			pass
	def pageup(self):
		if self.currentselection < len(self.softwarelist)-1:
			self.currentselection += 1
			self.currenttagselection = 0
			self.updateinfobox()
			self.refreshdetailwindow()
			guicore.setguisetting({"last_payload": {"selection": self.currentselection}},silent = True)
	def pagedown(self):
		if self.currentselection > 0:
			self.currentselection -= 1
			self.currenttagselection = 0
			self.updateinfobox()
			self.refreshdetailwindow()
			guicore.setguisetting({"last_payload": {"selection": self.currentselection}},silent = True)

















#Payload is a file path to a switch payload
def injectpayload(self,payload):
	if not os.path.isdir(locations.injectorfolder):
		print("initializing folder {}".format(locations.injectorfolder))
		os.mkdir(locations.injectorfolder)

	fuseestatus = guicore.checkguisetting("fusee-launcher", "version")
	if fuseestatus == "not installed" or fuseestatus == "none" or fuseestatus == None:
		# self.printtoboth("fusee-launcher not installed, downloading")
		with open(self.pjlist[0]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
			downloadurl = jfile[0]["zipball_url"]
			file = webhandler.download(downloadurl)
			file = os.path.join(locations.downloadsfolder, file)
			version = jfile[0]["tag_name"]
			with ZipFile(file, 'r') as zipObj:
				zipObj.extractall(locations.injectorfolder)
				self.printtoboth("Sucessfully extracted {} to payloads folder".format(file))
				files = zipObj.namelist()
				injector = None
				for possiblepayloadfile in files:
					if possiblepayloadfile.startswith(files[0] + "fusee"):
						injector = possiblepayloadfile
				if injector == None:
					self.printtoboth("Could not find injector in extracted files")
					return 
			newentry = {
				"fusee-launcher" : {
					"version": version,
					"location": injector,
				}
			}
			guicore.setguisetting(newentry)

	script_path = guicore.checkguisetting("fusee-launcher", "location")
	script_path = os.path.join(locations.injectorfolder, script_path)
	payload_file = payload
	p = subprocess.Popen([sys.executable, '-u', script_path, payload_file],
	          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

	with p.stdout:
	    for line in iter(p.stdout.readline, b''):
	    	self.printtoboth(line)
	p.wait()






#Returns true if switch found
def detect_rcm():
	import usb.core
	dev=usb.core.find(idVendor=0x0955, idProduct=0x7321)
	if dev:
		return True

def enable_auto_injection():
	guicore.setguisetting({"guisettings" : settings})

