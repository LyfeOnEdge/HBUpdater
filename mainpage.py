import HBUpdater
from format import * 
import homebrewcore
import webhandler

import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog
import customwidgets as cw

import json




class mainPage(tk.Frame,):
	def __init__(self, parent, controller,back_command):
		tk.Frame.__init__(self,parent)

		self.controller = controller


		#Full window frame, holds everything
		self.outer_frame = cw.themedframe(self,frame_borderwidth=0)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

		#Frame for main list, contains listboxes and scroll bar, and list titles
		self.listbox_frame = cw.themedframe(self.outer_frame,frame_highlightthickness= 0)
		self.listbox_frame.place(relx=0.0, rely=0.0, relheight=1, relwidth=1, width=-infoframewidth,)
		self.listbox_frame.configure(background=dark_color)

		#The contents of this frame are built backwards due to needing to align the searchbox with the icons
		self.searchbox_frame = cw.themedframe(self.listbox_frame,frame_highlightthickness= 0,background_color=light_color, frame_borderwidth = 0)
		self.searchbox_frame.place(relx=0.0, rely=0.0,height=searchboxheight, relwidth=1,)

		#Variable to track place searchbox icons in correct location
		self.iconspacer = icon_and_search_bar_spacing
		
		# self.settingsimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"settings.png"))
		# self.settingsimage = self.settingsimage.subsample(2)
		# self.iconspacer = self.settingsimage.width()
		# self.settingsicon = cw.iconbutton(self.searchbox_frame,self.settingsimage,command_name=lambda: self.controller.show_frame("settingsPage"))
		# self.settingsicon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -self.settingsimage.height()/2,width = self.settingsimage.width(), height=self.settingsimage.height())

		# self.iconspacer += icon_and_search_bar_spacing


		self.sdimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"sd.png"))
		self.sdimage = self.sdimage.subsample(2)
		self.iconspacer += self.sdimage.width()
		self.sdicon = cw.iconbutton(self.searchbox_frame,self.sdimage,command_name=self.setSDpath)
		self.sdicon.place(relx= 1, x=-self.iconspacer, rely=.5, y = -self.sdimage.height()/2,width = self.sdimage.width(), height=self.sdimage.height())


		# self.iconspacer += icon_and_search_bar_spacing


		# self.addrepoimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"plus.png"))
		# self.addrepoimage = self.addrepoimage.subsample(2)
		# self.iconspacer += self.addrepoimage.width()
		# self.repoicon = cw.iconbutton(self.searchbox_frame, self.addrepoimage,command_name=None)
		# self.repoicon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -self.addrepoimage.height()/2,width = self.addrepoimage.width(), height=self.addrepoimage.height())

		# self.iconspacer += icon_and_search_bar_spacing

		# self.injectimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"injector.png"))
		# self.injectimage = self.injectimage.subsample(2)
		# self.iconspacer += self.injectimage.width()
		# self.injecticon = cw.iconbutton(self.searchbox_frame,self.injectimage,command_name=lambda: self.controller.show_frame("injectorScreen"))
		# self.injecticon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -self.injectimage.height()/2,width = self.injectimage.width(), height=self.injectimage.height())

		self.iconspacer += icon_and_search_bar_spacing*2

		#search box, custom class
		self.sb = cw.SearchBox(self.searchbox_frame, command=self.search, placeholder="Type and press enter to search")
		self.sb.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=searchboxheight-2*icon_and_search_bar_spacing, y=-((searchboxheight)/2) + icon_and_search_bar_spacing ) 

		#Frame to hold titles of colums
		self.column_title_frame=cw.themedframe(self.listbox_frame,frame_highlightthickness=0)
		self.column_title_frame.place(relx=0.0, rely=0, y=+searchboxheight, height=columtitlesheight, relwidth=1)

		self.big_software_name_label_frame = cw.themedframe(self.column_title_frame)
		self.big_software_name_label_frame.place(relx=0.0, rely=0.0, relheight=1, relwidth=0.44)
		self.big_software_name_label = cw.columnlabel(self.big_software_name_label_frame, "NAME")
		self.big_software_name_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)

		self.big_genre_name_label_frame = cw.themedframe(self.column_title_frame)
		self.big_genre_name_label_frame.place(relx=0.44, rely=0, relheight=1, relwidth=0.20)
		self.big_genre_name_label = cw.columnlabel(self.big_genre_name_label_frame, "GENRE")
		self.big_genre_name_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)

		self.big_software_version_label_frame = cw.themedframe(self.column_title_frame)
		self.big_software_version_label_frame.place(relx=0.64, rely=0, relheight=1, relwidth=0.18)
		self.big_software_version_label = cw.columnlabel(self.big_software_version_label_frame, "VERSION")
		self.big_software_version_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)

		self.big_install_status_label_frame = cw.themedframe(self.column_title_frame)
		self.big_install_status_label_frame.place(relx=0.82, rely=0, relheight=1, relwidth=0.18)
		self.big_install_status_label = cw.columnlabel(self.big_install_status_label_frame, "INSTALLED")
		self.big_install_status_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)


		#vertical scroll bar (Not placed, trying to make it only appear when needed)
		self.vsb = tk.Scrollbar(self.listbox_frame,orient="vertical", command=self.OnVsb)
		# self.vsb.place(relx=0.975, rely=0.15, relheight=0.94, relwidth=0.025)


		self.list_frame = cw.themedframe(self.listbox_frame,frame_highlightthickness=0)
		self.list_frame.place(relx=0,rely=0,y=searchboxheight+columtitlesheight, relheight=1, height=-(searchboxheight+columtitlesheight),relwidth=1)

		self.homebrew_listbox_frame = cw.themedframe(self.list_frame,)
		self.homebrew_listbox_frame.place(relx=0.0,rely=0,relheight=1,relwidth=0.44)
		self.homebrew_listbox = cw.customlistbox(self.homebrew_listbox_frame,)
		self.homebrew_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)

		self.genre_listbox_frame = cw.themedframe(self.list_frame,)
		self.genre_listbox_frame.place(relx=0.44,rely=0,relheight=1,relwidth=0.20)
		self.genre_listbox = cw.customlistbox(self.genre_listbox_frame,)
		self.genre_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)

		self.version_listbox_frame = cw.themedframe(self.list_frame,)
		self.version_listbox_frame.place(relx=0.64, rely=0, relheight=1, relwidth=0.18)
		self.version_listbox = cw.customlistbox(self.version_listbox_frame,)
		self.version_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)

		self.status_listbox_frame = cw.themedframe(self.list_frame,)
		self.status_listbox_frame.place(relx=0.82, rely=0, relheight=1, relwidth=0.18)
		self.status_listbox = cw.customlistbox(self.status_listbox_frame,)
		self.status_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)
		
		#bind listboxes to move with mouse
		self.homebrew_listbox.bind("<MouseWheel>", self.OnMouseWheel)
		self.genre_listbox.bind("<MouseWheel>", self.OnMouseWheel)
		self.version_listbox.bind("<MouseWheel>", self.OnMouseWheel)
		self.status_listbox.bind("<MouseWheel>", self.OnMouseWheel)

		#Bind double-click to open details:
		self.homebrew_listbox.bind('<Double-Button-1>', self.showdetailsevent)



		#Frame for details (raised when details button clicked)
		
		#past version tags listbox
		self.details_frame = cw.themedframe(self.outer_frame)
		self.details_frame.place(relx=0.0, rely=0.0, width=-infoframewidth, relheight=1, relwidth=1)
		
		self.tags_listbox = cw.customlistbox(self.details_frame)
		self.tags_listbox.place(relx=0.0, rely=0, relheight=1, relwidth=0.2)
		self.tags_listbox.configure(font=tags_listbox_font)
		self.tags_listbox.configure(font=version_number_font)
		self.tags_listbox.bind('<<ListboxSelect>>',self.CurTagSelet)
		

		#patch notes 
		self.scrolling_patch_notes = cw.ScrolledText(self.details_frame)
		self.scrolling_patch_notes.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)
		self.scrolling_patch_notes.configure(background="white")
		self.scrolling_patch_notes.configure(font=version_notes_font)
		self.scrolling_patch_notes.configure(foreground="black")
		self.scrolling_patch_notes.configure(highlightbackground="#d9d9d9")
		self.scrolling_patch_notes.configure(highlightcolor="black")
		self.scrolling_patch_notes.configure(selectbackground=version_notes_selection_background)
		self.scrolling_patch_notes.configure(selectforeground=version_notes_selection_foreground)
		self.scrolling_patch_notes.configure(wrap="none")
		self.scrolling_patch_notes.configure(background=version_notes_column_background)
		self.scrolling_patch_notes.configure(foreground=version_notes_color)


		self.infobox = cw.infobox(self.outer_frame)
		self.infobox.place(relx=1, x=-infoframewidth, rely=0.0, relheight=1, width=infoframewidth)


		#Shared images
		#self.installimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"installbutton.png")).zoom(3).subsample(5)
		self.infoimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"info.png")).zoom(3).subsample(5)
		#self.previousimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"prev.png")).zoom(3).subsample(5)
		#self.nextimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"next.png")).zoom(3).subsample(5)
		#self.backbutton = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"back.png")).zoom(3).subsample(5)
		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)


		#Back to list button frame, placed first so the details button covers it
		self.details_buttons_frame =cw.navbox(self.infobox,
			primary_button_command = self.specificinstall,
			etc_button_image = self.returnimage,
			etc_button_command = self.showlist,
			left_context_command = self.versioncusordown,
			right_context_command = self.versioncursorup,
			)
		self.details_buttons_frame.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)


		self.list_buttons_frame = cw.navbox(self.infobox,
			primary_button_command = self.install,
			etc_button_image = self.infoimage,
			etc_button_command = self.showdetails,
			left_context_command = self.pagedown,
			right_context_command = self.pageup,
			)
		self.list_buttons_frame.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)

		#initial update of the info frame
		self.showlist()
		self.updateinfo()
		self.refreshdetailwindow()
		self.popsoftwarelistbox()
		self.list_buttons_frame.tkraise()

	def setSDpath(self):
		chosensdpath = filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
		HBUpdater.setSDpath(chosensdpath)
		if HBUpdater.sdpathset:
			self.updatelistbox(None)

	def install(self):
		
		if HBUpdater.sdpathset:
			HBUpdater.installitem(HBUpdater.hbdict, HBUpdater.softwarechunknumber,0)
			self.updatelistbox(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(HBUpdater.hbdict, HBUpdater.softwarechunknumber,0)
				self.updatelistbox(None)
			else:
				print("SD Path Not set, not installing")

	def specificinstall(self):
		
		
		if HBUpdater.sdpathset:
			HBUpdater.installitem(HBUpdater.hbdict, HBUpdater.softwarechunknumber, HBUpdater.tagversionnumber)
			self.updatelistbox(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(HBUpdater.hbdict, HBUpdater.softwarechunknumber, HBUpdater.tagversionnumber)
				self.updatelistbox(None)
			else:
				print("SD Path Not set, not installing")

	#raises the details frame
	def showdetails(self):
		self.details_frame.tkraise()
		self.details_buttons_frame.tkraise()
	def showdetailsevent(self,event):
		self.showdetails()

    #raises the list frame
	def showlist(self):
		self.listbox_frame.tkraise()
		self.list_buttons_frame.tkraise()
	def showlistevent(self,event):
		self.showlist()

    #listbox scrollbar 
	def OnVsb(self, *args):
		self.homebrew_listbox.yview(*args)
		self.status_listbox.yview(*args)
		self.version_listbox.yview(*args)
		self.genre_listbox.yview(*args)

		#-event.delta makes the boxes scroll in the right direction
	def OnMouseWheel(self, event):
		self.homebrew_listbox.yview("scroll", -event.delta,"units")
		self.status_listbox.yview("scroll",-event.delta,"units")
		self.version_listbox.yview("scroll",-event.delta,"units")
		self.genre_listbox.yview("scroll",-event.delta,"units")
		# this prevents default bindings from firing, which
		# would end up scrolling the widget twice
		return "break"


	
	#fill the listboxes with data
	def popsoftwarelistbox(self,):
		self.homebrew_listbox.bind('<<ListboxSelect>>',self.CurSelet)

		for softwarechunk in HBUpdater.hbdict:
			softwarename = softwarechunk["software"]
			self.homebrew_listbox.insert(END, softwarename)

			# self.homebrew_listbox.itemconfig(END, foreground=font_color)
			with open(softwarechunk["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			  jfile = json.load(json_file)
			version = jfile[0]["tag_name"]
			self.version_listbox.insert(END, version)
			# self.version_listbox.itemconfig(END, foreground=font_color)

			self.status_listbox.insert(END, "not installed")

			group = softwarechunk["group"]
			self.genre_listbox.insert(END, group)

		self.genre_listbox.configure(state=DISABLED)
		self.version_listbox.configure(state=DISABLED)
		self.status_listbox.configure(state=DISABLED)

	def updatelistbox(self,searchterm):
		self.homebrew_listbox.configure(state=NORMAL)
		self.genre_listbox.configure(state=NORMAL)
		self.version_listbox.configure(state=NORMAL)
		self.status_listbox.configure(state=NORMAL)

		self.homebrew_listbox.delete(0,END)
		self.genre_listbox.delete(0,END)
		self.version_listbox.delete(0,END)
		self.status_listbox.delete(0,END)


		for softwarechunk in HBUpdater.hbdict:
			softwarename = softwarechunk["software"]
			self.homebrew_listbox.insert(END, softwarename)
			


			# self.homebrew_listbox.itemconfig(END, foreground=font_color)
			with open(softwarechunk["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			  jfile = json.load(json_file)
			version = jfile[0]["tag_name"]
			self.version_listbox.insert(END, version)
			# self.version_listbox.itemconfig(END, foreground=font_color)

			installedversion = HBUpdater.checkversion(softwarechunk["software"])

			if installedversion == version:
				self.status_listbox.insert(END, checkmark)
				self.status_listbox.itemconfig(END, foreground="white")
			else: 
				self.status_listbox.insert(END, installedversion)

			group = softwarechunk["group"]
			self.genre_listbox.insert(END, group)

			if searchterm == None:
				self.homebrew_listbox.itemconfig(END,foreground=listbox_font_color)
			else:
				if searchterm.lower() in softwarename.lower() or searchterm.lower() in group.lower() or version.lower().startswith(searchterm.lower()):
					self.homebrew_listbox.itemconfig(END,foreground=listbox_font_color)
				else:
					self.homebrew_listbox.itemconfig(END,foreground=dark_listbox_font_color)
				
		self.genre_listbox.configure(state=DISABLED)
		self.version_listbox.configure(state=DISABLED)
		self.status_listbox.configure(state=DISABLED)


	def search(self, searchstring):
		self.updatelistbox(searchstring)


	#get current selection from list box
	def CurSelet(self, event):
		
		widget = event.widget
		selection=widget.curselection()
		picked = widget.get(selection[0])
		HBUpdater.softwarechunknumber = widget.get(0, "end").index(picked)
		self.updateinfo()
		self.refreshdetailwindow()


	#INFOBOX UPDATE
	#update title information
	def updatetitle(self,title):
		self.titlevar.set(title)

	#update author information
	def updateauthor(self,author):
		self.authorvar.set("by {}".format(author))

	#update project description
	def updatedescription(self, desc):
		self.project_description.configure(state=NORMAL)
		self.project_description.delete('1.0', END)
		self.project_description.insert(END, desc)
		self.project_description.configure(state=DISABLED)

	#update all info in the info box
	def updateinfo(self):
		self.homebrew_listbox.selection_clear(0,HBUpdater.dictlen-1)
		self.homebrew_listbox.selection_set(HBUpdater.softwarechunknumber)
		self.homebrew_listbox.see(HBUpdater.softwarechunknumber)
		self.version_listbox.selection_clear(0,HBUpdater.dictlen-1)
		self.version_listbox.selection_set(HBUpdater.softwarechunknumber)
		self.version_listbox.see(HBUpdater.softwarechunknumber)
		self.status_listbox.selection_clear(0,HBUpdater.dictlen-1)
		self.status_listbox.selection_set(HBUpdater.softwarechunknumber)
		self.status_listbox.see(HBUpdater.softwarechunknumber)
		self.genre_listbox.selection_clear(0,HBUpdater.dictlen-1)
		self.genre_listbox.selection_set(HBUpdater.softwarechunknumber)
		self.genre_listbox.see(HBUpdater.softwarechunknumber)

		if not HBUpdater.hbdict == {}:

			softwarename = HBUpdater.hbdict[HBUpdater.softwarechunknumber]["software"]
			self.infobox.updatetitle(softwarename)

			with open(HBUpdater.hbdict[HBUpdater.softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)

			#update author
			author = jfile[0]["author"]["login"]
			self.infobox.updateauthor(author)

			self.updateAuthorImage()

			self.infobox.updatedescription(HBUpdater.hbdict[HBUpdater.softwarechunknumber]["description"])




	def updateAuthorImageEvent(self,event):
		self.updateAuthorImage()


	def updateAuthorImage(self):
		softwarename = HBUpdater.hbdict[HBUpdater.softwarechunknumber]["software"]
		photopath = homebrewcore.checkphoto(homebrewcore.imagecachefolder, softwarename)

		if HBUpdater.hbdict[HBUpdater.softwarechunknumber]["photopath"] == None:
			HBUpdater.hbdict[HBUpdater.softwarechunknumber]["photopath"] = photopath

		if not photopath == None:
			photopath = homebrewcore.joinpaths(homebrewcore.imagecachefolder, photopath)
			photoexists = homebrewcore.exists(photopath)
		else:
			photoexists = False

		if not photoexists:
			try:
				photopath = webhandler.cacheimage(authorimg,softwarename)
				HBUpdater.hbdict[HBUpdater.softwarechunknumber]["photopath"] = photopath
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
		if HBUpdater.softwarechunknumber < HBUpdater.dictlen-1:
			HBUpdater.softwarechunknumber += 1
			self.updateinfo()
			self.refreshdetailwindow()

	def pagedown(self):
		if HBUpdater.softwarechunknumber > 0:
			HBUpdater.softwarechunknumber -= 1
			self.updateinfo()
			self.refreshdetailwindow()


	#movement buttons, moves through homebrewlist or brew version
	def versioncursorup(self):
		if HBUpdater.tagversionnumber < HBUpdater.taglen-1:
			HBUpdater.tagversionnumber += 1
			self.updatetagsbox()
			self.updatetagnotes()

	def versioncusordown(self):
		if HBUpdater.tagversionnumber > 0:
			HBUpdater.tagversionnumber -= 1
			self.updatetagsbox()
			self.updatetagnotes()



	def updatetagsbox(self):
		self.tags_listbox.selection_clear(0,END)
		self.tags_listbox.selection_set(HBUpdater.tagversionnumber)
		self.tags_listbox.see(HBUpdater.tagversionnumber)

	def updatetagnotes(self):
		
	    
		with open(HBUpdater.hbdict[HBUpdater.softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
		tagnotes = jfile[HBUpdater.tagversionnumber]["body"]
		self.scrolling_patch_notes.configure(state=NORMAL)
		self.scrolling_patch_notes.delete('1.0', END)
		self.scrolling_patch_notes.insert(END, tagnotes)
		self.scrolling_patch_notes.configure(state=DISABLED)

	def gettagdescription(self,index_string):
		
		with open(HBUpdater.hbdict[HBUpdater.softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

		for version in jfile:
			if index_string == version["tag_name"]:
				tagnotes = version["body"]

		self.updatetagnotes()


	def refreshdetailwindow(self,):
		
		
		HBUpdater.taglen = 0
		HBUpdater.tagversionnumber = 0
		self.tags_listbox.delete(0,END)
		if not HBUpdater.hbdict == {}:
			with open(HBUpdater.hbdict[HBUpdater.softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)

			for version in jfile:
				HBUpdater.taglen+=1
				tag = version["tag_name"]
				self.tags_listbox.insert(END, tag)

			self.updatetagsbox()
			self.updatetagnotes()

	def CurTagSelet(self, event):
		
		
		try:
			widget = event.widget
			HBUpdater.tagversionnumber=widget.curselection()[0]
			self.updatetagsbox()
			self.updatetagnotes()
		except:
			pass