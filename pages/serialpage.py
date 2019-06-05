from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
# import modules.HBUpdater as HBUpdater
import modules.webhandler as webhandler
import modules.locations as locations
import os, shutil, sys, subprocess, json
from zipfile import ZipFile

import tkinter as tk
from tkinter.constants import *

import pages.installerhelperpage as installerhelperpage
import pages.errorpage as errorpage

serialboxheight = 90
serialboxwidth = 500

page_name = "serialPage"

class serialPage(cw.themedframe):
	def __init__(self, parent, controller,back_command):
		self.back_command = back_command
		self.controller = controller
		self.activestatus = False

		cw.themedframe.__init__(self,parent,background_color= light_color)
		self.bind("<<ShowFrame>>", self.on_show_frame) #Bind on_show_frame to showframe event

		self.outerframe = cw.themedframe(self, background_color = light_color)
		self.outerframe.place(x=0,y=0,relwidth=1,relheight=1)

		self.returnimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"returnbutton.png")).zoom(3).subsample(5)
		self.returnbutton = cw.navbutton(self.outerframe,command_name=self.back,image_object=self.returnimage)
		self.returnbutton.place(relx=1,rely=1,x=-2*navbuttonheight,y=-2*navbuttonheight,width=navbuttonheight,height=navbuttonheight)

		self.serialentry = cw.entrybox(self.outerframe, command=self.check, entry_font=mondoboldtext, placeholder="Enter Switch Serial Number",justification="center")
		self.serialentry.place(relx=0.5,rely=.5, x=-0.5*serialboxwidth, y=-0.5*serialboxheight, width=serialboxwidth, height=serialboxheight)
		self.serialentry.entry.bind("<KeyRelease>", self.on_key)

		self.serialstatus = cw.themedguidelabel(self,None,anchor="center",label_font=hugeboldtext)
		self.serialstatus.place(relx=0.5,rely=.5, x=-0.5*serialboxwidth, y=+0.5*serialboxheight,width=serialboxwidth)


	def on_show_frame(self,event):
		self.serialentry.enable()
		self.activestatus = True

	def on_key(self,event):
		if self.activestatus:
			entrytext = self.serialentry.get_text()
			self.check(entrytext)

	def check(self,serial):
		status = checkserial(serial)
		status = ssnc_output_to_friendly(status)
		self.serialstatus.set("Serial Status - {}".format(status))

	def back(self):
		self.serialentry.disable()
		self.activestatus = False
		self.back_command()

def checkserial(serial):
	if len(serial) < 10:
		status =  "Too short"
		return status

	if len(serial) > 5 and len(serial) < 14:
		status = "Error"

	if len(serial) > 14:
		status =  "Too long"
		return status

	with open(guicore.checkguisetting("ssnc","serials")) as f:
		serials = json.load(f)

	import tools.ssnc.serial_checker as sc

	status = sc.check(serials, serial)
	print(status)
	return status

def ssnc_output_to_friendly(ssncoutput):
	outputmap = {
		None : "Unknown",
		"safe" : "Not Patched :D",
		"warning" : "Possibly Patched :|",
		"patched" : "Patched :(",
		"incorrect" : "incorrect / incomplete",
		"Too long" : "Too long",
		"Too short" : "Too short",
	}
	return outputmap.get(ssncoutput, "Error")

def checkifSSNCinstalled():
	return guicore.checkguisetting("ssnc", "version")

def downloadSSNCandinstalldependencies():
	if not os.path.isdir(locations.ssncfolder):
		os.mkdir(locations.ssncfolder)
		print("initializing ssnc folder")
	
	jsonfile = webhandler.getJson("ssnc", locations.serialcheckerdict["githubapi"])
	with open(jsonfile, encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
		jfile = json.load(json_file)
		if jfile == [] or jfile == None:
			print("Error: empty json nut file")
			return

		zipurl = jfile[0]["zipball_url"]
		version = jfile[0]["tag_name"]
		if zipurl == None:
			print("zip file url invalid, can't download nut assets")

		zip = webhandler.download(zipurl)
		zip = os.path.join(locations.downloadsfolder, zip)

		extractedfiles = []
		with ZipFile(zip) as zip_file:
		    for member in zip_file.namelist():
		        filename = os.path.basename(member)
		        if not filename:
		            continue

		        source = zip_file.open(member)
		        targetfile = os.path.join(locations.ssncfolder, filename)
		        target = open(targetfile, "wb")
		        with source, target:
		            shutil.copyfileobj(source, target)
		        extractedfiles.append(targetfile)
		print("Sucessfully extracted {} to {} folder\n".format(zip,locations.ssncfolder))

		try:
			dependencies = locations.serialcheckerdict["dependencies"]
			webhandler.installmodulelist(dependencies)
		except Exception as e:
			print("failed to download dependencies, error: {}".format(e))

		print("downloading serials.json for Switch Serial Number Checker")

		try:
			import configparser
			config = configparser.ConfigParser()

			try:
				configfile = os.path.join(locations.ssncfolder,"config.ini")
				config.read(configfile)
				serials_url = config.get("SSNC", "SerialsURL")
				serials = webhandler.getJson("serials", serials_url)

			except Exception as e:
				print("error: {}".format(e))
				print("failed to obtain serials json") 
				serials = None
		except:
			self.controller.seterrorstate("some required modules failed to install, software will be unavailable")
			self.controller.event_generate("<<error>>")
			return

		newentry = {
			"ssnc" : {
				"version": version,
				"location": extractedfiles,
				"serials" : serials
			}
		}
		print(newentry)


		guicore.setguisetting(newentry)


	


