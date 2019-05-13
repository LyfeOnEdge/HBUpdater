import HBUpdater
from format import * 
import homebrewcore
import guicore
import webhandler
import nuthandler

import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog
import customwidgets as cw

import json

import webbrowser

details_guide_text = """This menu will allow you to install older versions of apps, uninstall software, and go to the software's project page. Project pages are not currently supported for user-added content. 
""" 

class mainPage(tk.Frame,):
	def __init__(self, parent, controller,back_command):
		tk.Frame.__init__(self,parent)
		self.bind("<<ShowFrame>>", self.on_show_frame)
		self.controller = controller


		#Shared images
		self.infoimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"info.png")).zoom(3).subsample(5)
		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)
		self.settingsimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"settings.png"))
		self.nutimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"nut.png"))

		#Full window frame, holds everything
		self.outer_frame = cw.themedframe(self,frame_borderwidth=0,frame_highlightthickness= 0)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)


		#page for warning users that nut isn't installed and asking if they want to install it
		self.nutinstallframe = cw.themedframe(self.outer_frame,frame_borderwidth=0,frame_highlightthickness=0)
		self.nutinstallframe.place(relwidth=1,relheight=1)
		self.nutreturnbutton = cw.navbutton(self.nutinstallframe, image_object=self.returnimage, command_name=self.showlist)
		self.nutreturnbutton.place(relx=1, rely=1, x=-(separatorwidth+navbuttonheight), y=-(separatorwidth+navbuttonheight), height=navbuttonheight, width=navbuttonheight)

		self.nuttimewarningframe= cw.themedframe(self.nutinstallframe,frame_highlightthickness=0,frame_borderwidth=0)
		self.nuttimewarningframe.place(relheight=1,relwidth=1)
		self.nuttimewarning = cw.themedguidelabel(self.nuttimewarningframe,"DOWNLOADING NUT SERVER AND INSTALLING DEPENDENCIES.\nTHIS CAN TAKE A WHILE, ESPECIALLY WITH SLOWER SYSTEMS.\nPLEASE BE PATIENT")
		self.nuttimewarning.place(relx=0.5,rely=0.5,x=-200, width=400,height=3*navbuttonheight)

		self.nutnotdownloadedwarningframe= cw.themedframe(self.nutinstallframe,frame_highlightthickness=0,frame_borderwidth=0)
		self.nutnotdownloadedwarningframe.place(relheight=1,relwidth=1)
		self.nutnotdownloadedwarning = cw.themedguidelabel(self.nutnotdownloadedwarningframe,"IT LOOKS LIKE YOU DON'T HAVE NUT DOWNLOADED YET,\n WOULD YOU LIKE TO DOWNLOAD IT AND INSTALL ITS DEPENDENCIES?")
		self.nutnotdownloadedwarning.place(relx=0.5,rely=0.5,x=-200, width=400,height=3*navbuttonheight)
		self.installnutbutton = cw.navbutton(self.nutnotdownloadedwarningframe, command_name=self.getnut,text_string="YES")
		self.installnutbutton.place(relx=0.5,rely=0.5,y=+(3*navbuttonheight + separatorwidth),width=100,x=-50)



		#Frame for main list, contains listboxes and scroll bar, and list titles
		self.listbox_frame = cw.themedframe(self.outer_frame,frame_borderwidth=0,frame_highlightthickness= 0)
		self.listbox_frame.place(relx=0.0, rely=0.0, relheight=1, relwidth=1, width=-infoframewidth,)
		self.listbox_frame.configure(background=dark_color)

		#The contents of this frame are built backwards due to needing to align the searchbox with the icons
		self.searchbox_frame = cw.themedframe(self.listbox_frame,frame_highlightthickness= 0,background_color=light_color, frame_borderwidth = 0)
		self.searchbox_frame.place(relx=0.0, rely=0.0,height=searchboxheight, relwidth=1,)

		#Variable to track place searchbox icons in correct location
		self.iconspacer = icon_and_search_bar_spacing
		
		self.iconspacer += searchboxheight-2*icon_and_search_bar_spacing
		self.nuticon = cw.iconbutton(self.searchbox_frame,self.nutimage,command_name=self.checknutandstart)
		self.nuticon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -((searchboxheight)/2) + icon_and_search_bar_spacing,width = searchboxheight-2*icon_and_search_bar_spacing, height=searchboxheight-2*icon_and_search_bar_spacing)
		self.iconspacer += icon_and_search_bar_spacing
		
		# self.iconspacer += searchboxheight-2*icon_and_search_bar_spacing
		# self.settingsicon = cw.iconbutton(self.searchbox_frame,self.settingsimage,command_name=lambda: self.controller.show_frame("settingsPage"))
		# self.settingsicon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -((searchboxheight)/2) + icon_and_search_bar_spacing,width = searchboxheight-2*icon_and_search_bar_spacing, height=searchboxheight-2*icon_and_search_bar_spacing)
		# self.iconspacer += icon_and_search_bar_spacing
		
		self.injectimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"injector.png"))
		self.injectimage = self.injectimage.subsample(2)
		self.iconspacer += searchboxheight-2*icon_and_search_bar_spacing
		self.injecticon = cw.iconbutton(self.searchbox_frame,self.injectimage,command_name=lambda: self.controller.show_frame("injectorScreen"))
		self.injecticon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -((searchboxheight)/2) + icon_and_search_bar_spacing,width = searchboxheight-2*icon_and_search_bar_spacing, height=searchboxheight-2*icon_and_search_bar_spacing)
		
		self.iconspacer += icon_and_search_bar_spacing
		self.sdimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"sd.png"))
		self.sdimage = self.sdimage.subsample(2)
		self.iconspacer += searchboxheight-2*icon_and_search_bar_spacing
		self.sdicon = cw.iconbutton(self.searchbox_frame,self.sdimage,command_name=self.setSDpath)
		self.sdicon.place(relx= 1, x=-self.iconspacer, rely=.5, y = -((searchboxheight)/2) + icon_and_search_bar_spacing,width =searchboxheight-2*icon_and_search_bar_spacing, height=searchboxheight-2*icon_and_search_bar_spacing)

		self.iconspacer += icon_and_search_bar_spacing
		self.addrepoimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"plus.png"))
		self.addrepoimage = self.addrepoimage.subsample(2)
		self.iconspacer += searchboxheight-2*icon_and_search_bar_spacing
		self.repoicon = cw.iconbutton(self.searchbox_frame, self.addrepoimage,command_name=lambda: self.controller.show_frame("addRepoScreen"))
		self.repoicon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -((searchboxheight)/2) + icon_and_search_bar_spacing,width = searchboxheight-2*icon_and_search_bar_spacing, height=searchboxheight-2*icon_and_search_bar_spacing)

		#search box, custom class
		self.iconspacer += icon_and_search_bar_spacing*2
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
		self.big_software_version_label = cw.columnlabel(self.big_software_version_label_frame, "LATEST")
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


		self.listbox_list = []

		self.homebrew_listbox_frame = cw.themedframe(self.list_frame,)
		self.homebrew_listbox_frame.place(relx=0.0,rely=0,relheight=1,relwidth=0.44)
		self.homebrew_listbox = cw.customlistbox(self.homebrew_listbox_frame,)
		self.homebrew_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)
		self.homebrew_listbox.bind('<Double-Button-1>', self.showdetailsevent) #Bind double-click to open details
		self.homebrew_listbox.bind('<<ListboxSelect>>',self.CurSelet)
		self.listbox_list.append(self.homebrew_listbox)

		self.genre_listbox_frame = cw.themedframe(self.list_frame,)
		self.genre_listbox_frame.place(relx=0.44,rely=0,relheight=1,relwidth=0.20)
		self.genre_listbox = cw.customlistbox(self.genre_listbox_frame,)
		self.genre_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)
		self.listbox_list.append(self.genre_listbox)

		self.version_listbox_frame = cw.themedframe(self.list_frame,)
		self.version_listbox_frame.place(relx=0.64, rely=0, relheight=1, relwidth=0.18)
		self.version_listbox = cw.customlistbox(self.version_listbox_frame,)
		self.version_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)
		self.listbox_list.append(self.version_listbox)

		self.status_listbox_frame = cw.themedframe(self.list_frame,)
		self.status_listbox_frame.place(relx=0.82, rely=0, relheight=1, relwidth=0.18)
		self.status_listbox = cw.customlistbox(self.status_listbox_frame,)
		self.status_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)
		self.listbox_list.append(self.status_listbox)
		
		#bind listboxes to move with mouse scroll
		for listbox in self.listbox_list:
			listbox.bind("<MouseWheel>", self.OnMouseWheel)

		# self.homebrew_listbox.bind("<MouseWheel>", self.OnMouseWheel)
		# self.genre_listbox.bind("<MouseWheel>", self.OnMouseWheel)
		# self.version_listbox.bind("<MouseWheel>", self.OnMouseWheel)
		# self.status_listbox.bind("<MouseWheel>", self.OnMouseWheel)

		


		#Frame for details (raised when details button clicked)
		#past version tags listbox
		self.details_frame = cw.themedframe(self.outer_frame)
		self.details_frame.place(relx=0.0, rely=0.0, width=-infoframewidth, relheight=1, relwidth=1)
		
		self.tags_listbox = cw.customlistbox(self.details_frame)
		self.tags_listbox.place(relx=0.0, rely=0, relheight=1, relwidth=0.2)
		self.tags_listbox.configure(font=tags_listbox_font)
		self.tags_listbox.configure(font=version_number_font)
		self.tags_listbox.bind('<<ListboxSelect>>',self.CurTagSelet)

		self.patch_notes_separator = cw.separator(self.details_frame)
		self.patch_notes_separator.place(relx=0.2,width=separatorwidth, rely=0, relheight=1,)
		
		#patch notes 
		self.scrolling_patch_notes = cw.ScrolledText(self.details_frame,
			highlightcolor="black",
			highlightbackground="#d9d9d9",
			font=version_notes_font,
			selectbackground=version_notes_selection_background,
			selectforeground=version_notes_selection_foreground,
			background=version_notes_column_background,
			foreground=version_notes_color,
			wrap="none",
			borderwidth=0,
			highlightthickness=0,
			)
		self.scrolling_patch_notes.place(relx=0.2,x=+separatorwidth, rely=0, relheight=1, relwidth=0.8,width=-separatorwidth)


		#frame to hold subframes in far right column
		self.rightcolumn = cw.themedframe(self, frame_borderwidth=0,frame_highlightthickness=0)
		self.rightcolumn.place(relx=1, x=-infoframewidth, rely=0.0, relheight=1, width=infoframewidth)



		self.details_right_column = cw.themedframe(self.rightcolumn, frame_borderwidth=0,frame_highlightthickness=0,background_color=light_color)
		self.details_right_column.place(relwidth = 1, relheight=1)

		self.details_guide = cw.ScrolledText(self.details_right_column,borderwidth=0,highlightthickness=0,background=light_color,foreground=guidetextcolor,wrap=WORD,font=details_guide_font)
		self.details_guide.place(relwidth=1,relheight=1,height=-(4*(navbuttonheight+separatorwidth)+separatorwidth))
		self.details_guide.insert(END,details_guide_text)

		self.project_page_button = cw.navbutton(self.details_right_column,command_name=self.openprojectpage,image_object= None,text_string="PROJECT PAGE")
		self.project_page_button.place(relx=0, rely=1, y=-4*(navbuttonheight+separatorwidth), height=navbuttonheight, x=+separatorwidth,relwidth=1, width=-(2*separatorwidth))

		self.uninstall_button = cw.navbutton(self.details_right_column,command_name=self.uninstall,image_object= None,text_string="UNINSTALL")
		self.uninstall_button.place(relx=0, rely=1, y=-3*(navbuttonheight+separatorwidth), height=navbuttonheight, x=+separatorwidth,relwidth=1, width=-(2*separatorwidth))

		#Back to list button frame, placed first so the details button covers it
		self.details_buttons =cw.navbox(self.details_right_column,
			primary_button_command = self.specificinstall,
			etc_button_image = self.returnimage,
			etc_button_command = self.showlist,
			left_context_command = self.versioncusordown,
			right_context_command = self.versioncursorup,
			)
		self.details_buttons.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)


		self.main_right_column = cw.themedframe(self.rightcolumn, frame_borderwidth=0,frame_highlightthickness=0,background_color=light_color)
		self.main_right_column.place(relwidth = 1, relheight=1)

		self.infobox = cw.infobox(self.main_right_column)
		self.infobox.place(relwidth=1,relheight=1,)

		self.list_buttons_frame = cw.navbox(self.main_right_column,
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
		self.main_right_column.tkraise()

	def setSDpath(self):
		chosensdpath = filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
		HBUpdater.setSDpath(chosensdpath)
		if HBUpdater.sdpathset:
			self.updatelistbox(None)

	def install(self):
		
		if HBUpdater.sdpathset:
			HBUpdater.installitem(guicore.hbdict, guicore.softwarechunknumber,0)
			self.updatelistbox(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(guicore.hbdict, guicore.softwarechunknumber,0)
				self.updatelistbox(None)
			else:
				print("SD Path Not set, not installing")

	def specificinstall(self):
		if HBUpdater.sdpathset:
			HBUpdater.installitem(guicore.hbdict, guicore.softwarechunknumber, guicore.tagversionnumber)
			self.updatelistbox(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(guicore.hbdict, guicore.softwarechunknumber, guicore.tagversionnumber)
				self.updatelistbox(None)
			else:
				print("SD Path Not set, not installing")

	def uninstall(self):
		if HBUpdater.sdpathset:
			HBUpdater.uninstallsoftware(guicore.hbdict[guicore.softwarechunknumber]["software"])
			self.updatelistbox(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.uninstallsoftware(guicore.hbdict[guicore.softwarechunknumber]["software"])
				self.updatelistbox(None)
			else:
				print("SD Path Not set, not installing")

	def checknutandstart(self):
		if not nuthandler.checkifnutdownloaded():
			self.nutnotdownloadedwarningframe.tkraise()
			self.nutinstallframe.tkraise()
			return
		self.startnut()

	def startnut(self):
		nuthandler.startnut()

	def getnut(self):
		self.nuttimewarningframe.tkraise()
		nuthandler.downloadnutandinstalldependencies()
		self.nutnotdownloadedwarningframe.tkraise()
		self.showlist()



	#raises the details frame
	def showdetails(self):
		self.details_frame.tkraise()
		self.details_right_column.tkraise()
	def showdetailsevent(self,event):
		self.showdetails()

    #raises the list frame
	def showlist(self):
		self.listbox_frame.tkraise()
		self.main_right_column.tkraise()
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
		for listbox in self.listbox_list:
			listbox.yview("scroll", -event.delta,"units")
		# this prevents default bindings from firing, which
		# would end up scrolling the widget twice
		return "break"

	#fill the listboxes with data
	def popsoftwarelistbox(self,):
		for softwarechunk in guicore.hbdict:
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
		for listbox in self.listbox_list:
			listbox.configure(state=NORMAL)
			listbox.delete(0,END)


		for softwarechunk in guicore.hbdict:
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
		guicore.softwarechunknumber = widget.get(0, "end").index(picked)
		self.updateinfo()
		self.refreshdetailwindow()


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
		self.homebrew_listbox.selection_clear(0,guicore.dictlen-1)
		self.homebrew_listbox.selection_set(guicore.softwarechunknumber)
		self.homebrew_listbox.see(guicore.softwarechunknumber)
		self.version_listbox.selection_clear(0,guicore.dictlen-1)
		self.version_listbox.selection_set(guicore.softwarechunknumber)
		self.version_listbox.see(guicore.softwarechunknumber)
		self.status_listbox.selection_clear(0,guicore.dictlen-1)
		self.status_listbox.selection_set(guicore.softwarechunknumber)
		self.status_listbox.see(guicore.softwarechunknumber)
		self.genre_listbox.selection_clear(0,guicore.dictlen-1)
		self.genre_listbox.selection_set(guicore.softwarechunknumber)
		self.genre_listbox.see(guicore.softwarechunknumber)

		if not guicore.hbdict == {}:

			softwarename = guicore.hbdict[guicore.softwarechunknumber]["software"]
			self.infobox.updatetitle(softwarename)

			with open(guicore.hbdict[guicore.softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)

			#update author
			author = jfile[0]["author"]["login"]
			self.infobox.updateauthor(author)

			self.updateAuthorImage()

			self.infobox.updatedescription(guicore.hbdict[guicore.softwarechunknumber]["description"])




	def updateAuthorImageEvent(self,event):
		self.updateAuthorImage()


	def updateAuthorImage(self):
		softwarename = guicore.hbdict[guicore.softwarechunknumber]["software"]
		photopath = homebrewcore.checkphoto(homebrewcore.imagecachefolder, softwarename)

		if guicore.hbdict[guicore.softwarechunknumber]["photopath"] == None:
			guicore.hbdict[guicore.softwarechunknumber]["photopath"] = photopath

		if not photopath == None:
			photopath = homebrewcore.joinpaths(homebrewcore.imagecachefolder, photopath)
			photoexists = homebrewcore.exists(photopath)
		else:
			photoexists = False

		if not photoexists:
			try:
				with open(guicore.hbdict[guicore.softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
					jfile = json.load(json_file)
					url = jfile[0]["author"]["avatar_url"]
				photopath = webhandler.cacheimage(url,softwarename)
				guicore.hbdict[guicore.softwarechunknumber]["photopath"] = photopath
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
		if guicore.softwarechunknumber < guicore.dictlen-1:
			guicore.softwarechunknumber += 1
			self.updateinfo()
			self.refreshdetailwindow()

	def pagedown(self):
		if guicore.softwarechunknumber > 0:
			guicore.softwarechunknumber -= 1
			self.updateinfo()
			self.refreshdetailwindow()


	#movement buttons, moves through homebrewlist or brew version
	def versioncursorup(self):
		if guicore.tagversionnumber < guicore.taglen-1:
			guicore.tagversionnumber += 1
			self.updatetagsbox()
			self.updatetagnotes()

	def versioncusordown(self):
		if guicore.tagversionnumber > 0:
			guicore.tagversionnumber -= 1
			self.updatetagsbox()
			self.updatetagnotes()

	def updatetagsbox(self):
		self.tags_listbox.selection_clear(0,END)
		self.tags_listbox.selection_set(guicore.tagversionnumber)
		self.tags_listbox.see(guicore.tagversionnumber)

	def updatetagnotes(self):
		with open(guicore.hbdict[guicore.softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
		tagnotes = jfile[guicore.tagversionnumber]["body"]
		self.scrolling_patch_notes.configure(state=NORMAL)
		self.scrolling_patch_notes.delete('1.0', END)
		self.scrolling_patch_notes.insert(END, tagnotes)
		self.scrolling_patch_notes.configure(state=DISABLED)

	def gettagdescription(self,index_string):
		with open(guicore.hbdict[guicore.softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

		for version in jfile:
			if index_string == version["tag_name"]:
				tagnotes = version["body"]

		self.updatetagnotes()


	def refreshdetailwindow(self,):
		guicore.taglen = 0
		guicore.tagversionnumber = 0
		self.tags_listbox.delete(0,END)
		if not guicore.hbdict == {}:
			with open(guicore.hbdict[guicore.softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)

			for version in jfile:
				guicore.taglen+=1
				tag = version["tag_name"]
				self.tags_listbox.insert(END, tag)

			self.updatetagsbox()
			self.updatetagnotes()

	def CurTagSelet(self, event):
		try:
			widget = event.widget
			guicore.tagversionnumber=widget.curselection()[0]
			self.updatetagsbox()
			self.updatetagnotes()
		except:
			pass

	def openprojectpage(self):
		try:
			url = guicore.hbdict[guicore.softwarechunknumber]["projectpage"]
			webbrowser.open_new_tab(url)
		except:
			print("invalid or non-existant project page url")

	#whenever we return to the main page reload it
	def on_show_frame(self,event):
		self.updatelistbox(None)