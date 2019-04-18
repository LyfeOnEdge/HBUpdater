import HBUpdater
from format import * 
import homebrewcore
import injector
import webhandler
from zipfile import ZipFile


import tkinter as tk
from tkinter.constants import *
import customwidgets as cw

import json

# #ijdict
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

		self.payload_listbox_frame = cw.themedframe(self)
		self.payload_listbox_frame.place(relx=0,rely=0,relheight=.7,relwidth=0.4)
		self.payload_listbox = cw.customlistbox(self.payload_listbox_frame,)
		self.payload_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)
		self.payload_listbox.bind('<<ListboxSelect>>',self.CurSelet)

		self.injectorguideframe = cw.themedframe(self,frame_borderwidth=2)
		self.injectorguideframe.place(relx=.4,rely=0,relheight=.7,relwidth=.6,width=-infoframewidth)
		self.injectorguide = tk.Text(self.injectorguideframe,foreground=guidetextcolor,background=dark_color,font=guidetext,wrap="word",highlightthickness=0,borderwidth=0)
		self.injectorguide.place(relheight=1,relwidth=1,x=+lbcolumnoffset, width=-lbcolumnoffset)
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
		HBUpdater.payloadchunknumber = widget.get(0, "end").index(picked)
		self.updateinfo()


		#fill the listboxes with data
	def popsoftwarelistbox(self,):
		for softwarechunk in HBUpdater.ijdict:
			softwarename = softwarechunk["software"]
			self.payload_listbox.insert(END, softwarename)

			# self.homebrew_listbox.itemconfig(END, foreground=font_color)
			# with open(softwarechunk["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			#   jfile = json.load(json_file)
			# version = jfile[0]["tag_name"]
			# self.version_listbox.insert(END, version)

			# self.status_listbox.insert(END, "not installed")

	def injectpayload(self):
		if not injector.checkifpyusbinstalled():
			resp =  tkinter.messagebox.askyesno("Install PyUSB?", "PyUSB is required for fusee-launcher to work, install?")
			if resp:
				try:
					injector.installpyusb()
				except:
					console.print("Unknown error installing PyUSB")
					return
			else:
				console.print("Got answer: no, not installing")
				return


		with open(HBUpdater.ijdict[HBUpdater.payloadchunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

			assetnumber = 0

			if not HBUpdater.ijdict[HBUpdater.payloadchunknumber]["github_asset"] == None:
				assetnumber = HBUpdater.ijdict[HBUpdater.payloadchunknumber]["github_asset"]

			downloadurl = jfile[0]["assets"][assetnumber]["browser_download_url"]
			file = webhandler.download(downloadurl)
			file = homebrewcore.joinpaths(homebrewcore.downloadsfolder, file)
			
		if file.endswith(".bin"):
			payload = file

		elif file.endswith(".zip"):

			with ZipFile(file, 'r') as zipObj:
				zipObj.extractall(homebrewcore.payloadsfolder)
				print("Sucessfully extracted {} to payloads folder".format(file))
				files = zipObj.namelist()
				payload = None
				for possiblepayloadfile in files:
					if possiblepayloadfile.startswith(HBUpdater.ijdict[HBUpdater.payloadchunknumber]["zip_items"]):
						payload = possiblepayloadfile
				if payload == None:
					console.print("Could not find payload in extracted files")
					return 

			payload = homebrewcore.joinpaths(homebrewcore.payloadsfolder,payload)

		else:
			console.print("file handling method not found")
			return

		injector.injectpayload(payload)






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
		self.payload_listbox.selection_clear(0,HBUpdater.ijdictlen-1)
		self.payload_listbox.selection_set(HBUpdater.payloadchunknumber)
		self.payload_listbox.see(HBUpdater.payloadchunknumber)


		if not HBUpdater.ijdict == {}:

			softwarename = HBUpdater.ijdict[HBUpdater.payloadchunknumber]["software"]
			self.infobox.updatetitle(softwarename)

			with open(HBUpdater.ijdict[HBUpdater.payloadchunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)

			#update author
			author = jfile[0]["author"]["login"]
			self.infobox.updateauthor(author)

			self.updateAuthorImage()

			self.infobox.updatedescription(HBUpdater.ijdict[HBUpdater.payloadchunknumber]["description"])


	def updateAuthorImageEvent(self,event):
		self.updateAuthorImage()


	def updateAuthorImage(self):
		softwarename = HBUpdater.hbdict[HBUpdater.payloadchunknumber]["software"]
		photopath = homebrewcore.checkphoto(homebrewcore.imagecachefolder, softwarename)

		if HBUpdater.hbdict[HBUpdater.payloadchunknumber]["photopath"] == None:
			HBUpdater.hbdict[HBUpdater.payloadchunknumber]["photopath"] = photopath

		if not photopath == None:
			photopath = homebrewcore.joinpaths(homebrewcore.imagecachefolder, photopath)
			photoexists = homebrewcore.exists(photopath)
		else:
			photoexists = False

		if not photoexists:
			try:
				photopath = webhandler.cacheimage(authorimg,softwarename)
				HBUpdater.hbdict[HBUpdater.payloadchunknumber]["photopath"] = photopath
			except: 
				print("could not download icon image (you can safely ignore this error)")
				photopath = homebrewcore.joinpaths(homebrewcore.assetfolder,notfoundimage)
		try:
			project_image = tk.PhotoImage(file=photopath)

		except:
			# print(exc)
			photopath = homebrewcore.joinpaths(homebrewcore.assetfolder,notfoundimage)
			project_image = tk.PhotoImage(file=photopath)
			print("used not-found image due to error (you can safely ignore this error)")

		self.infobox.updateimage(art_image = project_image)


	#movement buttons, moves through homebrewlist or brew version
	def pageup(self):
		if HBUpdater.payloadchunknumber < HBUpdater.ijdictlen-1:
			HBUpdater.payloadchunknumber += 1
			self.updateinfo()

	def pagedown(self):
		if HBUpdater.payloadchunknumber > 0:
			HBUpdater.payloadchunknumber -= 1
			self.updateinfo()


	# def downloadfusee(self):
		