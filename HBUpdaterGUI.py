import os, sys

print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    sys.exit("Python 3.6 or greater is required to run this program.")

version = "0.2 (BETA)"
print("HBUpdaterGUI version {}".format(version))

import platform

#My modules
import webhandler 
import homebrewcore
import locations
from format import *

#Backend will not rin standalone
import HBUpdater
#GUI imports (weird import format)
import tkinter as tk
print("using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))

from tkinter import messagebox
from tkinter import filedialog
from tkinter.constants import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
py3 = True

import json

hbdict = {}

#Image for when there is an author image incompatible with tkinter
notfoundimage = "notfound.png"
softwarechunknumber = 0 #variable to track where we are in the list of homebrew
tagversionnumber = 0 #variable to track currently selected tag number
taglen=0 #variable to track number of items in version listbox 
infoframewidth = 225 #width infoframe takes up
searchboxheight=35 #Height of searhbox
columtitlesheight= 25 #Height of the frames holding the column titles

#Main frame handler, raises and lowers pages in z layer
class appManagerGui(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		if platform.system() == 'Windows':
			print("Windows detected, setting icon")
			self.iconbitmap(homebrewcore.joinpaths(homebrewcore.assetfolder, 'HBUpdater.ico'))

		# self.resizable(False,False)
		self.geometry("790x510")   #startup size 720p
		self.minsize(width=790, height=510) #minimum size currently supported
		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		container.configure(borderwidth = 0)
		container.configure(highlightthickness = 0)


		self.frames = {}
		for F in (mainPage,injectorPage,settingsPage):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("mainPage") #Show the main page frame

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()



class mainPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)

		self.controller = controller

		self.style = ttk.Style()
		if sys.platform == "win32":
			self.style.theme_use('winnative')

		#Full window frame, holds everything
		self.outer_frame = themedframe(self)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

		#Frame for main list, contains listboxes and scroll bar, and list titles
		self.listbox_frame = themedframe(self.outer_frame,frame_highlightthickness= 0)
		self.listbox_frame.place(relx=0.0, rely=0.0, relheight=1, relwidth=1, width=-infoframewidth,)
		self.listbox_frame.configure(background=dark_color)

		#The contents of this frame are built backwards due to needing to align the searchbox with the icons
		self.searchbox_frame = themedframe(self.listbox_frame,frame_highlightthickness= 1,background_color=light_color)
		self.searchbox_frame.place(relx=0.0, rely=0.0,height=searchboxheight, relwidth=1,)

		#Variable to track place searchbox icons in correct location
		self.iconspacer = 0
		
		# self.settingsimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"settings.png"))
		# self.settingsimage = self.settingsimage.subsample(2)
		# self.iconspacer = self.settingsimage.width()
		# self.settingsicon = iconbutton(self.searchbox_frame,self.settingsimage,command_name=lambda: self.controller.show_frame("settingsPage"))
		# self.settingsicon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -self.settingsimage.height()/2,width = self.settingsimage.width(), height=self.settingsimage.height())

		# self.iconspacer += icon_and_search_bar_spacing


		self.sdimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"sd.png"))
		self.sdimage = self.sdimage.subsample(2)
		self.iconspacer += self.sdimage.width()
		self.sdicon = iconbutton(self.searchbox_frame,self.sdimage,command_name=self.setSDpath)
		self.sdicon.place(relx= 1, x=-self.iconspacer, rely=.5, y = -self.sdimage.height()/2,width = self.sdimage.width(), height=self.sdimage.height())


		# self.iconspacer += icon_and_search_bar_spacing


		# self.addrepoimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"plus.png"))
		# self.addrepoimage = self.addrepoimage.subsample(2)
		# self.iconspacer += self.addrepoimage.width()
		# self.repoicon = iconbutton(self.searchbox_frame, self.addrepoimage,command_name=None)
		# self.repoicon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -self.addrepoimage.height()/2,width = self.addrepoimage.width(), height=self.addrepoimage.height())

		# # self.iconspacer += icon_and_search_bar_spacing

		# self.injectimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"injector.png"))
		# self.injectimage = self.injectimage.subsample(2)
		# self.iconspacer += self.injectimage.width()
		# self.injecticon = iconbutton(self.searchbox_frame,self.injectimage,command_name=lambda: self.controller.show_frame("injectorPage"))
		# self.injecticon.place(relx= 1, rely=.5, x=-self.iconspacer, y = -self.injectimage.height()/2,width = self.injectimage.width(), height=self.injectimage.height())

		self.iconspacer += icon_and_search_bar_spacing*2

		#search box, custom class
		self.sb = SearchBox(self.searchbox_frame, command=self.search, placeholder="Type and press enter to search")
		self.sb.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing*2, relwidth=1, width=-(self.iconspacer+5), height=searchboxheight-10, y=-(searchboxheight-10)/2)

		#Frame to hold titles of colums
		self.column_title_frame=themedframe(self.listbox_frame,frame_highlightthickness=0)
		self.column_title_frame.place(relx=0.0, rely=0, y=+searchboxheight, height=columtitlesheight, relwidth=1)

		self.big_software_name_label_frame = themedframe(self.column_title_frame)
		self.big_software_name_label_frame.place(relx=0.0, rely=0.0, relheight=1, relwidth=0.44)
		self.big_software_name_label = columnlabel(self.big_software_name_label_frame, "NAME")
		self.big_software_name_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)

		self.big_genre_name_label_frame = themedframe(self.column_title_frame)
		self.big_genre_name_label_frame.place(relx=0.44, rely=0, relheight=1, relwidth=0.20)
		self.big_genre_name_label = columnlabel(self.big_genre_name_label_frame, "GENRE")
		self.big_genre_name_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)

		self.big_software_version_label_frame = themedframe(self.column_title_frame)
		self.big_software_version_label_frame.place(relx=0.64, rely=0, relheight=1, relwidth=0.18)
		self.big_software_version_label = columnlabel(self.big_software_version_label_frame, "VERSION")
		self.big_software_version_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)

		self.big_install_status_label_frame = themedframe(self.column_title_frame)
		self.big_install_status_label_frame.place(relx=0.82, rely=0, relheight=1, relwidth=0.18)
		self.big_install_status_label = columnlabel(self.big_install_status_label_frame, "INSTALLED")
		self.big_install_status_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)


		#vertical scroll bar (Not placed, trying to make it only appear when needed)
		self.vsb = tk.Scrollbar(self.listbox_frame,orient="vertical", command=self.OnVsb)
		# self.vsb.place(relx=0.975, rely=0.15, relheight=0.94, relwidth=0.025)


		self.list_frame = themedframe(self.listbox_frame,frame_highlightthickness=0)
		self.list_frame.place(relx=0,rely=0,y=searchboxheight+columtitlesheight, relheight=1, height=-(searchboxheight+columtitlesheight),relwidth=1)

		self.homebrew_listbox_frame = themedframe(self.list_frame,)
		self.homebrew_listbox_frame.place(relx=0.0,rely=0,relheight=1,relwidth=0.44)
		self.homebrew_listbox = customlistbox(self.homebrew_listbox_frame,)
		self.homebrew_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)

		self.genre_listbox_frame = themedframe(self.list_frame,)
		self.genre_listbox_frame.place(relx=0.44,rely=0,relheight=1,relwidth=0.20)
		self.genre_listbox = customlistbox(self.genre_listbox_frame,)
		self.genre_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)

		self.version_listbox_frame = themedframe(self.list_frame,)
		self.version_listbox_frame.place(relx=0.64, rely=0, relheight=1, relwidth=0.18)
		self.version_listbox = customlistbox(self.version_listbox_frame,)
		self.version_listbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset)

		self.status_listbox_frame = themedframe(self.list_frame,)
		self.status_listbox_frame.place(relx=0.82, rely=0, relheight=1, relwidth=0.18)
		self.status_listbox = customlistbox(self.status_listbox_frame,)
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
		self.details_frame = themedframe(self.outer_frame)
		self.details_frame.place(relx=0.0, rely=0.0, width=-infoframewidth, relheight=1, relwidth=1)
		
		self.tags_listbox = customlistbox(self.details_frame)
		self.tags_listbox.place(relx=0.0, rely=0, relheight=1, relwidth=0.2)
		self.tags_listbox.configure(font=tags_listbox_font)
		self.tags_listbox.configure(font=version_number_font)
		self.tags_listbox.bind('<<ListboxSelect>>',self.CurTagSelet)
		

		#patch notes 
		self.scrolling_patch_notes = ScrolledText(self.details_frame)
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

		self.info_frame = themedframe(self.outer_frame)
		self.info_frame.place(relx=1, x=-infoframewidth, rely=0.0, relheight=.999, width=infoframewidth)
		self.info_frame.configure(background=light_color)
		self.info_frame.bind("<Configure>", self.configure)

		#holds author picture
		self.project_art_label =themedlabel(self.info_frame,label_text = "project_art",)
		self.project_art_label.place(relx=0.0, rely=0.0, height=infoframewidth, relwidth=1)
		# self.project_art_label.configure(background=light_color)
		# self.project_art_label.configure(highlightbackground="#d9d9d9")
		# self.project_art_label.configure(highlightcolor="black")
		# self.project_art_label.configure(text='''project_art''')
		# self.project_art_label.configure(anchor="n")

		#Homebrew Title
		self.titlevar = tk.StringVar()
		self.titlevar.set("title_var")
		self.project_title_label = themedlabel(self.info_frame, 
			label_text = "project_title", 
			text_variable = self.titlevar, 
			label_color=info_softwarename_color, 
			label_font=info_softwarename_font
			)
		self.project_title_label.place(relx=0.0, rely=0.0, y=infoframewidth-30, relwidth=1.0)


		#author name
		self.authorvar = tk.StringVar()
		self.authorvar.set("author_var")
		self.author_name_label = themedlabel(self.info_frame,
			label_text = "author_name", 
			text_variable = self.authorvar, 
			label_color=info_author_color, 
			label_font=info_author_font
			)
		self.author_name_label.place(relx=0.0, rely=0, y=+infoframewidth, relwidth=1.0)


		#Description
		self.project_description = ScrolledText(self.info_frame)
		self.project_description.place(relx=0.0, rely=0.0, y=+infoframewidth+30, relheight=1, height=-(infoframewidth+30+100), relwidth=.98)
		self.project_description.configure(background=light_color)
		self.project_description.configure(foreground=info_description_color)
		self.project_description.configure(font=info_description_font)
		self.project_description.configure(wrap="word")
		self.project_description.configure(state=NORMAL)
		self.project_description.delete('1.0', END)
		self.project_description.insert(END, "Project description")
		self.project_description.configure(state=DISABLED)
		self.project_description.configure(borderwidth=0)


		#Shared images
		self.installimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"installbutton.png"))
		self.installimage = self.installimage.zoom(3).subsample(5)
		self.infoimage = tk.PhotoImage(file=os.path.join(homebrewcore.assetfolder,"info.png"))
		self.infoimage = self.infoimage.zoom(3).subsample(5)
		self.previousimage = tk.PhotoImage(file=os.path.join(homebrewcore.assetfolder,"prev.png"))
		self.previousimage = self.previousimage.zoom((3)).subsample(5)
		self.nextimage = tk.PhotoImage(file=os.path.join(homebrewcore.assetfolder,"next.png"))
		self.nextimage = self.nextimage.zoom((3)).subsample(5)
		self.backbutton = tk.PhotoImage(file=os.path.join(homebrewcore.assetfolder,"back.png"))
		self.backbutton = self.backbutton.zoom((3)).subsample(5)
		self.returnimage = tk.PhotoImage(file=os.path.join(homebrewcore.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)


		#Back to list button frame, placed first so the details button covers it
		self.details_buttons_frame =themedframe(self.info_frame,background_color=light_color,frame_borderwidth=0)
		self.details_buttons_frame.place(relx=.5, rely=1, x=-100, y=-87.5, height= 75, width=200)


		#back to list button
		self.backtolist_button = navbutton(self.details_buttons_frame, image_object=self.returnimage, command_name=self.showlist)
		self.backtolist_button.place(relx=1, rely=0, x=-self.infoimage.width(), height=self.infoimage.height(), width=self.infoimage.width())


		#install_button
		self.details_install_button = navbutton(self.details_buttons_frame, image_object = self.installimage, command_name = self.specificinstall)
		self.details_install_button.place(relx=0.00, rely=0, height=self.installimage.height(), width=self.installimage.width())

		#previous button in details menu
		self.details_previous_button = navbutton(self.details_buttons_frame, image_object = self.previousimage, command_name = self.versioncusordown)
		self.details_previous_button.place(relx=0.00, rely=1,y=-self.previousimage.height(),  height=self.previousimage.height(), width=self.previousimage.width())

		#next button in details menu
		self.details_next_button = navbutton(self.details_buttons_frame, image_object=self.nextimage, command_name=self.versioncursorup)
		self.details_next_button.place(relx=1, rely=1, y=-self.nextimage.height(), height=self.nextimage.height(), x=-self.nextimage.width(), width =self.nextimage.width())


		#frame to hold details button
		self.list_buttons_frame = themedframe(self.info_frame,background_color=light_color,frame_borderwidth=0)
		self.list_buttons_frame.place(relx=.5, rely=1, x=-100, y=-87.5, height= 75, width=200)

		#install button
		self.install_button = navbutton(self.list_buttons_frame, image_object = self.installimage, command_name=self.install)
		self.install_button.place(relx=0.00, rely=0, height=self.installimage.height(), width=self.installimage.width())

		#go-to-details button
		self.details_button = navbutton(self.list_buttons_frame, image_object=self.infoimage, command_name=self.showdetails)
		self.details_button.place(relx=1, rely=0, x=-self.infoimage.width(), height=self.infoimage.height(), width=self.infoimage.width())

		#previous button, goes up one section on the list
		self.previous_button = navbutton(self.list_buttons_frame, image_object=self.previousimage, command_name=self.pagedown)
		self.previous_button.place(relx=0.00, rely=1,y=-self.previousimage.height(),  height=self.previousimage.height(), width=self.previousimage.width())

		#next button, goes down one section on the list
		self.next_button = navbutton(self.list_buttons_frame, image_object=self.nextimage, command_name=self.pageup)
		self.next_button.place(relx=1, rely=1, y=-self.nextimage.height(), height=self.nextimage.height(), x=-self.nextimage.width(), width =self.nextimage.width())


		#initial update of the info frame
		self.showlist()
		self.updateinfo(0)
		self.refreshdetailwindow(0)
		self.popsoftwarelistbox()
		self.list_buttons_frame.tkraise()

	def setSDpath(self):
		chosensdpath = filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
		HBUpdater.setSDpath(chosensdpath)
		if HBUpdater.sdpathset:
			self.updatelistbox(None)

	def install(self):
		global softwarechunknumber
		if HBUpdater.sdpathset:
			HBUpdater.installitem(hbdict, softwarechunknumber,0)
			self.updatelistbox(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(hbdict, softwarechunknumber,0)
				self.updatelistbox(None)
			else:
				print("SD Path Not set, not installing")

	def specificinstall(self):
		global softwarechunknumber
		global tagversionnumber
		if HBUpdater.sdpathset:
			HBUpdater.installitem(hbdict, softwarechunknumber, tagversionnumber)
			self.updatelistbox(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(hbdict, softwarechunknumber, tagversionnumber)
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

	def configure(self,event):
		self.updateAuthorImageEvent(event)

	
	#fill the listboxes with data
	def popsoftwarelistbox(self,):
		self.homebrew_listbox.bind('<<ListboxSelect>>',self.CurSelet)

		for softwarechunk in hbdict:
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


		for softwarechunk in hbdict:
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
		global softwarechunknumber
		widget = event.widget
		selection=widget.curselection()
		picked = widget.get(selection[0])
		# softwarenumber = 0
		# for softwarechunk in hbdict:
		#     if softwarechunk["software"] == picked:
		#         softwarechunknumber = softwarenumber
		#     softwarenumber+= 1
		#index is superior method
		softwarechunknumber = widget.get(0, "end").index(picked)
		self.updateinfo(softwarechunknumber)
		self.refreshdetailwindow(softwarechunknumber)


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
	def updateinfo(self, softwarechunknumber):
		global dictlen
		global hbdict
		self.homebrew_listbox.selection_clear(0,dictlen-1)
		self.homebrew_listbox.selection_set(softwarechunknumber)
		self.homebrew_listbox.see(softwarechunknumber)
		self.version_listbox.selection_clear(0,dictlen-1)
		self.version_listbox.selection_set(softwarechunknumber)
		self.version_listbox.see(softwarechunknumber)
		self.status_listbox.selection_clear(0,dictlen-1)
		self.status_listbox.selection_set(softwarechunknumber)
		self.status_listbox.see(softwarechunknumber)


		softwarename = hbdict[softwarechunknumber]["software"]
		self.updatetitle(softwarename)

		with open(hbdict[softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

		#update author
		author = jfile[0]["author"]["login"]
		self.updateauthor(author)

		#update author url
		authorurl = jfile[0]["author"]["html_url"]
		authorimg = jfile[0]["author"]["avatar_url"]
		# authorimgfile = homebrewcore.joinpaths(homebrewcore.cachefolder, webhandler.getfilenamefromurl(authorimg))

		self.updateAuthorImage()

		self.updatedescription(hbdict[softwarechunknumber]["description"])

	def updateAuthorImageEvent(self,event):
		self.updateAuthorImage()


	def updateAuthorImage(self):
		global softwarechunknumber
		global hbdict
		softwarename = hbdict[softwarechunknumber]["software"]
		photopath = homebrewcore.checkphoto(homebrewcore.imagecachefolder, softwarename)

		if hbdict[softwarechunknumber]["photopath"] == None:
			hbdict[softwarechunknumber]["photopath"] = photopath

		if not photopath == None:
			photopath = homebrewcore.joinpaths(homebrewcore.imagecachefolder, photopath)
			photoexists = homebrewcore.exists(photopath)
		else:
			photoexists = False

		if not photoexists:
			try:
				photopath = webhandler.cacheimage(authorimg,softwarename)
				hbdict[softwarechunknumber]["photopath"] = photopath
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

		imagemax = self.info_frame.winfo_width()
		while not (project_image.width() > (imagemax - 80) and not (project_image.width() > imagemax)):
			if project_image.width() > imagemax:
				project_image = project_image.subsample(3)
			if project_image.width() < (imagemax - 80):
				project_image = project_image.zoom(4)

		self.project_art_label.configure(image=project_image)
		self.project_art_label.image = project_image

	#movement buttons, moves through homebrewlist or brew version
	def pageup(self):
		global softwarechunknumber
		if softwarechunknumber < dictlen-1:
			softwarechunknumber += 1
			self.updateinfo(softwarechunknumber)
			self.refreshdetailwindow(softwarechunknumber)

	def pagedown(self):
		global softwarechunknumber
		if softwarechunknumber > 0:
			softwarechunknumber -= 1
			self.updateinfo(softwarechunknumber)
			self.refreshdetailwindow(softwarechunknumber)


	#movement buttons, moves through homebrewlist or brew version
	def versioncursorup(self):
		global tagversionnumber
		if tagversionnumber < taglen-1:
			tagversionnumber += 1
			self.updatetagsbox()
			self.updatetagnotes()
			# self.updateinfo(softwarechunknumber)
			# self.updatedetailwindow(softwarechunknumber)

	def versioncusordown(self):
		global tagversionnumber
		if tagversionnumber > 0:
			tagversionnumber -= 1
			self.updatetagsbox()
			self.updatetagnotes()
			# self.updateinfo(softwarechunknumber)
			# self.updatedetailwindow(softwarechunknumber)

	def updatetagsbox(self):
		global tagversionnumber
		self.tags_listbox.selection_clear(0,END)
		self.tags_listbox.selection_set(tagversionnumber)
		self.tags_listbox.see(tagversionnumber)

	def updatetagnotes(self):
		global softwarechunknumber
		global tagversionnumber
		global taglen
	    
		with open(hbdict[softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
		# print("taglen = {}".format(taglen))
		# print("tagver = {}".format(tagversionnumber))
		tagnotes = jfile[tagversionnumber]["body"]
		self.scrolling_patch_notes.configure(state=NORMAL)
		self.scrolling_patch_notes.delete('1.0', END)
		self.scrolling_patch_notes.insert(END, tagnotes)
		self.scrolling_patch_notes.configure(state=DISABLED)

	def gettagdescription(self,index_string):
		global softwarechunknumber
		with open(hbdict[softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

		for version in jfile:
			if index_string == version["tag_name"]:
				tagnotes = version["body"]

		self.updatetagnotes()

	def refreshdetailwindow(self,softwarechunknumber):
		global taglen
		global tagversionnumber
		taglen = 0
		tagversionnumber = 0
		self.tags_listbox.delete(0,END)
		with open(hbdict[softwarechunknumber]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

		for version in jfile:
			taglen+=1
			tag = version["tag_name"]
			self.tags_listbox.insert(END, tag)

		self.updatetagsbox()
		self.updatetagnotes()

	def CurTagSelet(self, event):
		global softwarechunknumber
		global tagversionnumber
		try:
			widget = event.widget
			tagversionnumber=widget.curselection()[0]
			# self.gettagdescription(picked)
			self.updatetagsbox()
			self.updatetagnotes()
		except:
			pass


class settingsPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)

		self.style = ttk.Style()
		if sys.platform == "win32":
			self.style.theme_use('winnative')

		#Full window frame, holds everything
		self.outer_frame = themedframe(self)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)


		#back to main page button
		self.returnimage = tk.PhotoImage(file=os.path.join(homebrewcore.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)
		self.backtomain_button = navbutton(self.outer_frame, image_object=self.returnimage, command_name=lambda: controller.show_frame("mainPage"))
		self.backtomain_button.place(relx=1, rely=1, x=-(self.returnimage.width() + 20), y=-(self.returnimage.height()+20), height=self.returnimage.height(), width=self.returnimage.width())


class injectorPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)

		self.style = ttk.Style()
		if sys.platform == "win32":
			self.style.theme_use('winnative')

		#Full window frame, holds everything
		self.outer_frame = themedframe(self)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)


		#back to main page button
		self.returnimage = tk.PhotoImage(file=os.path.join(homebrewcore.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)
		self.backtomain_button = tk.Button(self.outer_frame, image=self.returnimage, command=lambda: controller.show_frame("mainPage"))
		self.backtomain_button.place(relx=1, rely=1, x=-(self.returnimage.width() + 20), y=-(self.returnimage.height()+20), height=self.returnimage.height(), width=self.returnimage.width())
		self.backtomain_button.configure(background=light_color)
		self.backtomain_button.configure(borderwidth=0)
		self.backtomain_button.configure(pady="0")
		self.backtomain_button.configure(activebackground=light_color)

		self.textoutheight = 10
		self.textoutputwidth = 50
		self.textoutput = tk.Text(self.outer_frame, height=self.textoutheight, width = 50, font=smalltext)
		self.textoutput.place(relx=0,rely=.7,relwidth=.6,relheight=.3)
		self.textoutput.configure(background = b)
		self.textoutput.configure(foreground = w)
		self.textoutput.configure(state=DISABLED)
		self.textoutput.configure(borderwidth = 0)

		def spewToTextOutput(self,textToSpew):
			self.textoutput.config(state=NORMAL)
			self.textoutput.insert(END, textToSpew + "\n\n")
			self.textoutput.config(state=DISABLED)
			self.textoutput.see(END)
			print(textToSpew)

		def spewBytesToTextOutput(self,textToSpew):
			self.textoutput.config(state=NORMAL)
			self.textoutput.insert(END, (textToSpew.decode("utf-8") + "\n\n"))
			self.textoutput.config(state=DISABLED)
			self.textoutput.see(END)
			print(textToSpew)



#Mit License
def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))

class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'contains_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.contains_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.contains_placeholder:
            entry.delete(0, "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
        
            state.contains_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            
            state.contains_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")
    
    entry.placeholder_state = state

    return state

#Searchbox, mit license.
class SearchBox(tk.Frame):
    def __init__(self, master, entry_width=30, entry_font=search_font, entry_background=dark_color, entry_foreground=search_font_color, button_text="Search", button_ipadx=10, button_background=dark_color, button_foreground="white", button_font=None, opacity=0.8, placeholder=place_holder_text, placeholder_font=place_holder_font, placeholder_color=place_holder_color, spacing=3, command=None):
        tk.Frame.__init__(self, master, borderwidth=0, highlightthickness=0,background=entry_background)
        
        self._command = command

        self.entry = tk.Entry(self, width=entry_width, background=entry_background, highlightcolor=button_background, highlightthickness=0, foreground = entry_foreground,borderwidth=0)
        self.entry.place(x=0,y=0,relwidth=1,relheight=1)
        
        if entry_font:
            self.entry.configure(font=entry_font)

        if placeholder:
            add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=placeholder_font)

        self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())
        self.entry.bind("<Return>", self._on_execute_command)

        opacity = float(opacity)

        if button_background.startswith("#"):
            r,g,b = hex2rgb(button_background)
        else:
            # Color name
            r,g,b = master.winfo_rgb(button_background)

        r = int(opacity*r)
        g = int(opacity*g)
        b = int(opacity*b)

        if r <= 255 and g <= 255 and b <=255:
            self._button_activebackground = '#%02x%02x%02x' % (r,g,b)
        else:
            self._button_activebackground = '#%04x%04x%04x' % (r,g,b)

        self._button_background = button_background

    def get_text(self):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            if entry.placeholder_state.contains_placeholder:
                return ""
            else:
                return entry.get()
        else:
            return entry.get()
        
    def set_text(self, text):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            entry.placeholder_state.contains_placeholder = False

        entry.delete(0, END)
        entry.insert(0, text)
        
    def clear(self):
        self.entry_var.set("")
        
    def focus(self):
        self.entry.focus()

    def _on_execute_command(self, event):
        text = self.get_text()
        self._command(text)

    def _state_normal(self, event):
        self.button_label.configure(background=self._button_background)

    def _state_active(self, event):
        self.button_label.configure(background=self._button_activebackground)



#Automatic scrollbar on labels
class AutoScroll(object):
	def __init__(self, master):
		try:
			vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
		except:
			pass
		hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

		try:
			self.configure(yscrollcommand=self._autoscroll(vsb))
		except:
			pass
		self.configure(xscrollcommand=self._autoscroll(hsb))

		self.grid(column=0, row=0, sticky='nsew')
		try:
			vsb.grid(column=1, row=0, sticky='ns')
		except:
			pass
		hsb.grid(column=0, row=1, sticky='ew')

		master.grid_columnconfigure(0, weight=1)
		master.grid_rowconfigure(0, weight=1)

		if py3:
			methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
				| tk.Place.__dict__.keys()
		else:
			methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
				+ tk.Place.__dict__.keys()

		for meth in methods:
			if meth[0] != '_' and meth not in ('config', 'configure'):
				setattr(self, meth, getattr(master, meth))

	@staticmethod
	def _autoscroll(sbar):
		'''Hide and show scrollbar as needed.'''
		def wrapped(first, last):
			first, last = float(first), float(last)
			if first <= 0 and last >= 1:
				sbar.grid_remove()
			else:
				sbar.grid()
			sbar.set(first, last)
		return wrapped

	def __str__(self):
		return str(self.master)

def _create_container(func):
	'''Creates a ttk Frame with a given master, and use this new frame to
	place the scrollbars and the widget.'''
	def wrapped(cls, master, **kw):
		container = ttk.Frame(master)
		container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
		container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
		return func(cls, container, **kw)
	return wrapped

class ScrolledText(AutoScroll, tk.Text):
	'''A standard Tkinter Text widget with scrollbars that will
	automatically show/hide as needed.'''
	@_create_container
	def __init__(self, master, **kw):
		tk.Text.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

class ScrolledListBox(AutoScroll, tk.Listbox):
	@_create_container
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

def _bound_to_mousewheel(event, widget):
	child = widget.winfo_children()[0]
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
	else:
		child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
		child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		widget.unbind_all('<MouseWheel>')
		widget.unbind_all('<Shift-MouseWheel>')
	else:
		widget.unbind_all('<Button-4>')
		widget.unbind_all('<Button-5>')
		widget.unbind_all('<Shift-Button-4>')
		widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
	if platform.system() == 'Windows':
		widget.yview_scroll(-1*int(event.delta/120),'units')
	elif platform.system() == 'Darwin':
		widget.yview_scroll(-1*int(event.delta),'units')
	else:
		if event.num == 4:
			widget.yview_scroll(-1, 'units')
		elif event.num == 5:
			widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
	if platform.system() == 'Windows':
		widget.xview_scroll(-1*int(event.delta/120), 'units')
	elif platform.system() == 'Darwin':
		widget.xview_scroll(-1*int(event.delta), 'units')
	else:
		if event.num == 4:
			widget.xview_scroll(-1, 'units')
		elif event.num == 5:
			widget.xview_scroll(1, 'units')


class themedframe(tk.Frame):
	def __init__(self,parent,frame_borderwidth = 0,frame_highlightthickness = 1,background_color = dark_color):
		tk.Frame.__init__(self,parent, 
			background = background_color,
			highlightthickness=frame_highlightthickness,
			highlightbackground=light_color,
			borderwidth = frame_borderwidth,
			)

class customlistbox(tk.Listbox):
	def __init__(self,frame, **kw, ):
		tk.Listbox.__init__(self,frame,**kw,
			highlightthickness=0,
			highlightbackground=light_color,
			borderwidth=0,
			exportselection = False, 
			background=dark_color,
			foreground=listbox_font_color,
			font=listbox_font,
			disabledforeground=dark_listbox_font_color,
			selectbackground=listboxselectionbackground,
			selectforeground=listboxselectionforeground,
			)

class iconbutton(tk.Listbox):
	def __init__(self,frame, image_object,command_name,):
		tk.Button.__init__(self,frame,
			background = light_color, 
			activebackground = light_color,
			borderwidth = 0,
			highlightthickness = 0,
			image = image_object,
			command = command_name,
			)

class columnlabel(tk.Label):
	def __init__(self,frame,label_text):
		tk.Label.__init__(self,frame,
			background = dark_color, 
			foreground = columnlabelcolor,
			borderwidth = 0,
			highlightthickness = 0,
			font = columnlabelfont,
			anchor = "w",
			text = label_text,
			)

class navbutton(tk.Button):
	def __init__(self,frame,image_object,command_name):
		tk.Button.__init__(self,frame,
			background=light_color,
			borderwidth=0,
			activebackground=light_color,
			#pady="0",
			image=image_object,
			command=command_name,
			)


class themedlabel(tk.Label):
	def __init__(self,frame,label_text,label_font=smalltext,label_color=w,text_variable=None):
		tk.Label.__init__(self,frame,
			background = light_color,
			highlightthickness=0,
			anchor="n",
			text = label_text,
			font=label_font,
			foreground= label_color,
			textvariable = text_variable,
			)








def setDict(dicty):
    global hbdict
    hbdict = dicty

    global dictlen
    dictlen = len(hbdict)

if __name__ == '__main__':  
	setDict(webhandler.getJsonSoftwareLinks(locations.softwarelist))
	#setDict(webhandler.getUpdatedSoftwareLinks(locations.softwarelist))
	#setDict(webhandler.getMissingJson(locations.softwarelist))
	for softwarechunk in hbdict:
		softwarechunk["photopath"] = None
	gui = appManagerGui()
	gui.title("HBUpdater")
	gui.mainloop()



# #launch with a passed software list
# def startGui(dicty):
#     setDict(HBUpdater.software)
#     gui = appManagerGui()
#     gui.mainloop()
