from modules.format import * 
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.homebrewcore as homebrewcore
import modules.webhandler as webhandler
import modules.customwidgets as cw

import tkinter as tk
from tkinter.constants import *

import json
import sys,subprocess
from zipfile import ZipFile


# #ijlist
# fuseefolder = homebrewcore.getpath("fusee-launcher")

class injectorScreen(tk.Frame):
	def __init__(self, parent, controller,back_command):
		tk.Frame.__init__(self,parent,borderwidth=0,highlightthickness= 0)

		#Full window frame, holds everything
		self.outer_frame = cw.themedframe(self,frame_borderwidth=0,frame_highlightthickness= 0)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

		self.infobox = cw.infobox(self.outer_frame)
		self.infobox.place(relx=1, x=-infoframewidth, rely=0.0, relheight=1, width=infoframewidth)

		#image for back button
		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)
		self.injector_navigation =cw.navbox(self.infobox,
			primary_button_command = self.injectpayload,
			primary_button_text = "INJECT",
			etc_button_image = self.returnimage,
			etc_button_command = lambda: controller.show_frame("mainPage"),
			left_context_command = self.pagedown,
			right_context_command = self.pageup,
			)
		self.injector_navigation.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=infoframewidth)

		self.console = cw.consolebox(self)
		self.console.place(relx=0,rely=.7,relwidth=1, width =-infoframewidth,relheight=.3)
		self.printtoconsolebox("Double-click payloads above to install other versions.\nConnect Switch, select payload, and press inject.\nThe payload and injector will be downloaded from github if they haven't been already.\n")

		self.listbox_frame = cw.themedframe(self,frame_borderwidth=0,frame_highlightthickness=0)
		self.listbox_frame.place(relx=0,rely=0,relheight=.7,relwidth=0.4)


		self.listbox_list = []

		self.payload_listbox_frame = cw.titledlistboxframe(self.listbox_frame,"Payload")
		self.payload_listbox_frame.place(relx=0,rely=0,relheight=1,relwidth=0.50)
		self.listbox_separatorA0 = cw.separator(self.payload_listbox_frame)
		self.listbox_separatorA0.place(relx=0,rely=0,y=columtitlesheight,height=injector_separator_width,relwidth=1,)
		self.payload_listbox = cw.customlistbox(self.payload_listbox_frame,)
		self.payload_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset, y=columtitlesheight+injector_separator_width,height=-(columtitlesheight+injector_separator_width))
		self.payload_listbox.bind('<<ListboxSelect>>',self.CurSelet)
		self.listbox_list.append(self.payload_listbox)
		

		self.listbox_separatorA = cw.separator(self.listbox_frame)
		self.listbox_separatorA.place(relx=.50,rely=0,relheight=1,width=injector_separator_width,)
		
		self.payload_latest_version_listbox_frame = cw.titledlistboxframe(self.listbox_frame,"Latest")
		self.payload_latest_version_listbox_frame.place(relx=0.50, x=+injector_separator_width,rely=0,relheight=1,relwidth=0.25,width=-injector_separator_width)
		self.listbox_separatorA2 = cw.separator(self.payload_latest_version_listbox_frame)
		self.listbox_separatorA2.place(relx=0,rely=0,y=columtitlesheight,height=injector_separator_width,relwidth=1,)
		self.payload_latest_version_listbox = cw.customlistbox(self.payload_latest_version_listbox_frame)
		self.payload_latest_version_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-(lbcolumnoffset), y=columtitlesheight+injector_separator_width,height=-(columtitlesheight+injector_separator_width))
		self.listbox_list.append(self.payload_latest_version_listbox)

		self.listbox_separatorB = cw.separator(self.listbox_frame)
		self.listbox_separatorB.place(relx=.75,rely=0,relheight=1,width=injector_separator_width,)

		self.payload_version_listbox_frame = cw.titledlistboxframe(self.listbox_frame,"Current")
		self.payload_version_listbox_frame.place(relx=0.75,x=+injector_separator_width,rely=0,relheight=1,relwidth=0.25,width=-injector_separator_width)
		self.listbox_separatorB2 = cw.separator(self.payload_version_listbox_frame)
		self.listbox_separatorB2.place(relx=0,rely=0,y=columtitlesheight,height=injector_separator_width,relwidth=1,)
		self.payload_version_listbox = cw.customlistbox(self.payload_version_listbox_frame)
		self.payload_version_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset, y=columtitlesheight+injector_separator_width, height=-(columtitlesheight+injector_separator_width))
		self.listbox_list.append(self.payload_version_listbox)

		self.listbox_guide_separator = cw.themedlabel(self,"")
		self.listbox_guide_separator.place(relx=.40,rely=0,relheight=.7,width=4,)

		self.injectorguideframe = cw.themedframe(self,frame_borderwidth=0,frame_highlightthickness=0)
		self.injectorguideframe.place(relx=.40,x=+8,rely=0,relheight=.7,relwidth=.6,width=-(infoframewidth+8))
		self.injectorguide = tk.Text(self.injectorguideframe,foreground=guidetextcolor,background=dark_color,font=rcmguidefont,wrap="word",highlightthickness=0,borderwidth=0)
		self.injectorguide.place(relheight=1,relwidth=1,)
		self.injectorguide.configure(state=NORMAL)
		self.injectorguide.insert(END, RCMGUIDETEXT)
		self.injectorguide.configure(state=DISABLED)


		self.popsoftwarelistbox()
		self.updateinfo()

		#get current selection from list box
	def CurSelet(self, event):
		widget = event.widget
		selection=widget.curselection()
		picked = widget.get(selection[0])
		guicore.payloadchunknumber = widget.get(0, "end").index(picked)
		self.updateinfo()


		#fill the listboxes with data
	def popsoftwarelistbox(self,):
		for listbox in self.listbox_list:
			listbox.configure(state=NORMAL)
			listbox.delete(0,END)

		for softwarechunk in guicore.ijlist:
			softwarename = softwarechunk["software"]
			self.payload_listbox.insert(END, softwarename)

			with open(softwarechunk["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)
				version = jfile[0]["tag_name"]

			self.payload_latest_version_listbox.insert(END, version)

			status = guicore.checkguisetting(softwarename, "version")

			if status == version:
				self.payload_version_listbox.insert(END, checkmark)
			else:
				self.payload_version_listbox.insert(END, status)

		self.payload_version_listbox.configure(state=DISABLED)
		self.payload_latest_version_listbox.configure(state=DISABLED)


	def injectpayload(self,):
		if not checkifpyusbinstalled():
			resp =  tk.messagebox.askyesno("Install PyUSB?", "PyUSB is required for fusee-launcher to work, install?")
			if resp:
				try:
					installpyusb()
				except:
					self.printtoboth("Unknown error installing PyUSB")
					return
			else:
				self.printtoboth("Got answer: no, not installing")
				return

		with open(guicore.ijlist[guicore.payloadchunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
			softwarename = guicore.ijlist[guicore.payloadchunknumber]["software"]
			version = jfile[0]["tag_name"]
			if guicore.checkguisetting(softwarename,"version") == None or guicore.checkguisetting(softwarename,"version") =="not installed":
				self.printtoboth("payload not yet downloaded, downloading...")

				#default asset number
				assetnumber = 0

				if not guicore.ijlist[guicore.payloadchunknumber]["github_asset"] == None:
					#if the asset we are going for is not the default (eg it is set in locations.py under github_asset) update the assetnumber
					assetnumber = guicore.ijlist[guicore.payloadchunknumber]["github_asset"]

				#get the download url for the payload we are going for
				downloadurl = jfile[0]["assets"][assetnumber]["browser_download_url"]
				self.printtoboth("downloading payload from {}".format(downloadurl))

				#file yielded by the download
				file = webhandler.download(downloadurl)
				file = homebrewcore.joinpaths(homebrewcore.downloadsfolder, file) #get absolute path to it
					
				#if downloaded file is already .bin, set the payload path to it.
				if file.endswith(".bin"):
					payload = file
					
				elif file.endswith(".zip"):
					#if file is zip, unzip it and find the payload based on the pattern set in its entry in #locations
					with ZipFile(file, 'r') as zipObj:
						zipObj.extractall(homebrewcore.payloadsfolder)
						self.printtoboth("Sucessfully extracted {} to payloads folder\n".format(file))
						files = zipObj.namelist()
						payload = None
						for possiblepayloadfile in files:
							if possiblepayloadfile.startswith(guicore.ijlist[guicore.payloadchunknumber]["zip_items"]):
								payload = possiblepayloadfile
						if payload == None:
							self.printtoboth("Could not find payload in extracted files")
							return 

					payload = homebrewcore.joinpaths(homebrewcore.payloadsfolder,payload)

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
				self.popsoftwarelistbox()

			#If payload is already downloaded and up-to-date
			else:
				payload = guicore.checkguisetting(softwarename,"location")


		injectpayload(self,payload)





	#INFOBOX UPDATE
	#update title information
	def updatetitle(self,title):
		self.infobox.titlevar.set(title)

	#update author information
	def updateauthor(self,author):
		self.infobox.authorvar.set("by {}".format(author))

	#update project description
	def updatedescription(self, desc):
		self.project_description.configure(state=NORMAL)
		self.project_description.delete('1.0', END)
		self.project_description.insert(END, desc)
		self.project_description.configure(state=DISABLED)

	#update all info in the info box
	def updateinfo(self):
		self.payload_listbox.selection_clear(0,guicore.ijlistlen-1)
		self.payload_listbox.selection_set(guicore.payloadchunknumber)
		self.payload_listbox.see(guicore.payloadchunknumber)

		if not guicore.ijlist == {}:

			softwarename = guicore.ijlist[guicore.payloadchunknumber]["software"]
			self.infobox.updatetitle(softwarename)

			with open(guicore.ijlist[guicore.payloadchunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)

			#update author
			author = jfile[0]["author"]["login"]
			self.infobox.updateauthor(author)

			self.updateAuthorImage()

			self.infobox.updatedescription(guicore.ijlist[guicore.payloadchunknumber]["description"])


	def updateAuthorImageEvent(self,event):
		self.updateAuthorImage()


	def updateAuthorImage(self):
		softwarename = guicore.ijlist[guicore.payloadchunknumber]["software"]
		photopath = homebrewcore.checkphoto(homebrewcore.imagecachefolder, softwarename)

		if guicore.ijlist[guicore.payloadchunknumber]["photopath"] == None:
			guicore.ijlist[guicore.payloadchunknumber]["photopath"] = photopath

		if not photopath == None:
			photopath = homebrewcore.joinpaths(homebrewcore.imagecachefolder, photopath)
			photoexists = homebrewcore.exists(photopath)
		else:
			photoexists = False

		if not photoexists:
			with open(guicore.ijlist[guicore.payloadchunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)
				url = jfile[0]["author"]["avatar_url"]
				print(softwarename)
			photopath = webhandler.cacheimage(url,softwarename)
			guicore.ijlist[guicore.payloadchunknumber]["photopath"] = photopath
		try:
			project_image = tk.PhotoImage(file=photopath)

		except:
			# print(exc)
			photopath = homebrewcore.joinpaths(homebrewcore.assetfolder,notfoundimage)
			print("used not-found image due to error (you can safely ignore this error)")

		self.infobox.updateimage(image_path = photopath)


	#movement buttons, moves through homebrewlist or brew version
	def pageup(self):
		if guicore.payloadchunknumber < guicore.ijlistlen-1:
			guicore.payloadchunknumber += 1
			self.updateinfo()

	def pagedown(self):
		if guicore.payloadchunknumber > 0:
			guicore.payloadchunknumber -= 1
			self.updateinfo()



	def printtoboth(self,stringtoprint):
		self.console.print(stringtoprint)
		print(stringtoprint)

	def printtoconsolebox(self,stringtoprint):
		self.console.print(stringtoprint)



def checkifpyusbinstalled():
	reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
	installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
	if "pyusb" in installed_packages:
		return True
	return False

#installs PyUSB on-demand for use with py
def installPyUSB():
    try:
    	print(subprocess.call([sys.executable, "-m", "pip", "install", "pyusb"]))
    	return(True)
    except:
    	print("Error installing pyUSB, do you have pip installed?")
    	return(False)


def injectpayload(self,payload):
	fuseestatus = guicore.checkguisetting("fusee-launcher", "version")
	if fuseestatus == "not installed" or fuseestatus == "none" or fuseestatus == None:
		# self.printtoboth("fusee-launcher not installed, downloading")
		with open(guicore.payloadinjector[0]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
			downloadurl = jfile[0]["zipball_url"]
			file = webhandler.download(downloadurl)
			file = homebrewcore.joinpaths(homebrewcore.downloadsfolder, file)
			version = jfile[0]["tag_name"]
			with ZipFile(file, 'r') as zipObj:
				zipObj.extractall(homebrewcore.payloadsfolder)
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
	script_path = homebrewcore.joinpaths(homebrewcore.payloadsfolder, script_path)
	payload_file = payload
	p = subprocess.Popen([sys.executable, '-u', script_path, payload_file],
	          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
	with p.stdout:
	    for line in iter(p.stdout.readline, b''):
	    	self.printtoboth(line)
	p.wait()
