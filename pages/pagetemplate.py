from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.homebrewcore as homebrewcore
import modules.webhandler as webhandler

import tkinter as tk
from tkinter.constants import *

import json

class page(cw.themedframe,):
	#Call this with an appropriately formatted list to populate the table with
	def setlist(self,list):
		self.softwarelist = list

	#Call this with a list of image objects, tooltips, and associated callbacks to initialize the search box and add buttons
	#It will automatically generate a row of buttons depending on how the page was initialized 
	def setbuttons(self,buttonlist):
		if not self.pagetitle == None: #If a title has been specified make it and space it to fit with the buttons
			self.iconspacer = 5*searchboxheight - icon_and_search_bar_spacing
			self.titleframe = cw.themedframe(self.searchbox_frame,background_color=light_color)
			self.titleframe.place(relx= 1, rely=.5, x=-self.iconspacer + icon_and_search_bar_spacing, y = -((searchboxheight)/2) + icon_and_search_bar_spacing,width = self.iconspacer-2*icon_and_search_bar_spacing, height=searchboxheight-2*icon_and_search_bar_spacing)
			self.title = tk.Label(self.titleframe,foreground=w,background=light_color,text=self.pagetitle,font=giantboldtext)
			self.title.place(x=0,y=0,relwidth=1,relheight=1)
			self.iconspacer += searchboxheight - 2*icon_and_search_bar_spacing

		else:
			self.iconspacer = searchboxheight - icon_and_search_bar_spacing

		#Generate a button and link a tooltip for each button in the list
		for button in buttonlist:
			if not button == buttonlist[0]:
				self.iconspacer += searchboxheight-2*icon_and_search_bar_spacing
			self.buttonobj = cw.iconbutton(self.searchbox_frame,button["image"],command_name=button["callback"])
			self.buttonobj.place(relx= 1, rely=.5, x=-self.iconspacer, y = -((searchboxheight)/2) + icon_and_search_bar_spacing,width = searchboxheight-2*icon_and_search_bar_spacing, height=searchboxheight-2*icon_and_search_bar_spacing)
			button_ttp = cw.tooltip(self.buttonobj,button["tooltip"])
			self.iconspacer += icon_and_search_bar_spacing

		#add search box with remaining space
		self.iconspacer += icon_and_search_bar_spacing
		self.sb = cw.SearchBox(self.searchbox_frame, command=self.search, placeholder="Search")
		self.sb.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=searchboxheight-2*icon_and_search_bar_spacing, y=-((searchboxheight)/2) + icon_and_search_bar_spacing ) 

	#Call this to set the guide text for the details window
	def setguidetext(self,text):
		self.details_guide.insert(END,text)


	def __init__(self, parent, controller, back_command,
		primary_button_command=None,		#Set this to override the callback of the primary button
		secondary_button_command=None,		#Set this to override the callback of the secondary button (the big button in the details window)
		primary_button_text=None,			#Set this to override the default primary button text 
		secondary_button_text=None,			#Set this to override the default secondary button text 
		version_function=None,				#Set this to override the default callback used to populate the status columm (usually this checks to see if the software has been installed on the selected sd card)
		status_column="INSTALLED",			#Set this to override the status column title
		page_title=None,					#Set this to apply a page title by the buttons and search box, leave blank to exclude it
		softwaregroup=None 					#Set this to the keyword section of the tracking file to log installed software to
		):
		
		self.controller = controller		#Controller (most toplevel parent)
		self.softwaregroup = softwaregroup	#Make group available
		self.softwarelist = []				#list to hold software data to populate table and more
		self.currentselection = 0			#Variable to track currently selected software
		self.currenttagselection = 0		#Variable to track currently selected sub-version
		self.pagetitle = page_title

		if version_function == None:		#If version_function wasn't set use the defaut
			self.version_function = HBUpdater.getlogstatus #Checks to see what version of each app in installed
		else:
			self.version_function = version_function
			print("Set version function")



		cw.themedframe.__init__(self,parent)#Init frame
		self.bind("<<ShowFrame>>", self.on_show_frame) #Bind on_show_frame to showframe event
		


		#Shared images
		self.backimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)
		self.infoimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"info.png")).zoom(3).subsample(5)

		#Full window frame, holds everything
		self.outer_frame = cw.themedframe(self,frame_borderwidth=0,frame_highlightthickness= 0)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

		#Frame for main list, contains listboxes and scroll bar, and list titles
		self.content_frame = cw.themedframe(self.outer_frame,frame_borderwidth=0,frame_highlightthickness= 0)
		self.content_frame.place(relx=0.0, rely=0.0, relheight=1, relwidth=1, width=-infoframewidth,)
		self.content_frame.configure(background=dark_color)

		#The contents of this frame are built backwards in self.setbutton due to needing to align the searchbox with the icons
		self.searchbox_frame = cw.themedframe(self.content_frame,frame_highlightthickness= 0,background_color=light_color, frame_borderwidth = 0)
		self.searchbox_frame.place(relx=0.0, rely=0.0,height=searchboxheight, relwidth=1,)

		#vertical scroll bar (Not placed, trying to make it only appear when needed)
		self.vsb = tk.Scrollbar(self.content_frame,orient="vertical", command=self.OnVsb)
		# self.vsb.place(relx=0.975, rely=0.15, relheight=0.94, relwidth=0.025)


		self.list_frame = cw.themedframe(self.content_frame,frame_highlightthickness=0)
		self.list_frame.place(relx=0,rely=0,y=searchboxheight, relheight=1, height=-(searchboxheight),relwidth=1)


		#generate table with column labels from list, status column name can be set in declaration
		columns = ["NAME", "GENRE", "LATEST", status_column]
		self.listbox_list = []
		self.maintable = cw.themedtable(self.list_frame, columns, 100)
		self.maintable.place(relheight=1,relwidth=1)
		#bind listboxes to move with mouse scroll
		for column in columns:
			self.maintable.listboxes[column].bind("<MouseWheel>", self.OnMouseWheel)
			self.listbox_list.append(self.maintable.listboxes[column])

		#set listboxes to easy names
		self.software_listbox = self.maintable.listboxes["NAME"]
		self.software_listbox.bind('<<ListboxSelect>>',self.CurSelet)

		self.genre_listbox = self.maintable.listboxes["GENRE"]
		self.latest_listbox = self.maintable.listboxes["LATEST"]
		self.status_listbox = self.maintable.listboxes[status_column]

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

		#column to hold usage details, set using self.setlist()
		self.details_right_column = cw.themedframe(self.rightcolumn, frame_borderwidth=0,frame_highlightthickness=0,background_color=light_color)
		self.details_right_column.place(relwidth = 1, relheight=1)
		#Details guide for usage details and warnings
		self.details_guide = cw.ScrolledText(self.details_right_column,borderwidth=0,highlightthickness=0,background=light_color,foreground=guidetextcolor,wrap=WORD,font=details_guide_font)
		self.details_guide.place(relwidth=1,relheight=1,height=-(4*(navbuttonheight+separatorwidth)+separatorwidth))
		
		#Button to launch the project page for the selected software
		self.project_page_button = cw.navbutton(self.details_right_column,command_name=self.openprojectpage,image_object= None,text_string="PROJECT PAGE")
		self.project_page_button.place(relx=0, rely=1, y=-4*(navbuttonheight+separatorwidth), height=navbuttonheight, x=+separatorwidth,relwidth=1, width=-(2*separatorwidth))

		#Button to uninstall selected software
		self.uninstall_button = cw.navbutton(self.details_right_column,command_name=self.uninstall,image_object= None,text_string="UNINSTALL")
		self.uninstall_button.place(relx=0, rely=1, y=-3*(navbuttonheight+separatorwidth), height=navbuttonheight, x=+separatorwidth,relwidth=1, width=-(2*separatorwidth))

		#Back to list button frame, placed first so the details button covers it\
		#Set commands based on if they were overridden
		if secondary_button_command == None:
			sbc = self.specificinstall
		else:
			sbc = secondary_button_command

		if secondary_button_text == None:
			sbt = "INSTALL"
		else:
			sbt = secondary_button_text
		self.details_buttons =cw.navbox(self.details_right_column,
			primary_button_command = sbc,
			primary_button_text = sbt,
			etc_button_image = self.backimage,
			etc_button_command = self.showlist,
			left_context_command = self.versioncusordown,
			right_context_command = self.versioncursorup,
			)
		self.details_buttons.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)


		#Main column with software details and more
		self.main_right_column = cw.themedframe(self.rightcolumn, frame_borderwidth=0,frame_highlightthickness=0,background_color=light_color)
		self.main_right_column.place(relwidth = 1, relheight=1)

		self.infobox = cw.infobox(self.main_right_column)
		self.infobox.place(relwidth=1,relheight=1,)


		if primary_button_command == None:
			pbc = self.install
		else:
			pbc = primary_button_command

		if primary_button_text == None:
			pbt = "INSTALL"
		else:
			pbt = primary_button_text
		self.list_buttons_frame = cw.navbox(self.main_right_column,
			primary_button_command = pbc,
			primary_button_text = pbt,
			etc_button_image = self.infoimage,
			etc_button_command = self.showdetails,
			left_context_command = self.pagedown,
			right_context_command = self.pageup,
			)
		self.list_buttons_frame.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)

		#Make sure list is made visible
		self.showlist()
		self.updateinfobox()
		self.refreshdetailwindow()
		self.updatetable(None)
		self.list_frame.tkraise()


	#Raises window to select sd card
	def setSDpath(self):
		chosensdpath = tk.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
		HBUpdater.setSDpath(chosensdpath)
		if HBUpdater.sdpathset:
			self.updatetable(None)

	#Installs selected software, brings up sd card selection if it hasn't been selected yet
	def install(self):
		if HBUpdater.sdpathset:
			HBUpdater.installitem(self.softwarelist, self.currentselection, 0, self.softwaregroup)
			self.updatetable(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(self.softwarelist, self.currentselection,0, self.softwaregroup)
				self.updatetable(None)
			else:
				print("SD Path Not set, not installing")

	#Installs specific version of selected software, brings up sd card selection if it hasn't been selected yet
	def specificinstall(self):
		if HBUpdater.sdpathset:
			HBUpdater.installitem(self.softwarelist, self.currentselection, self.currenttagselection, self.softwaregroup)
			self.updatetable(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(self.softwarelist, self.currentselection, self.currenttagselection, self.softwaregroup)
				self.updatetable(None)
			else:
				print("SD Path Not set, not installing")

	#Uninstalls selected software, brings up sd card selection if it hasn't been selected yet
	def uninstall(self):
		if HBUpdater.sdpathset:
			HBUpdater.uninstallsoftware(self.softwaregroup, self.softwarelist[self.currentselection]["software"])
			self.updatetable(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.uninstallsoftware(self.softwaregroup, self.softwarelist[self.currentselection]["software"])
				self.updatetable(None)
			else:
				print("SD Path Not set, not installing")

	#called when enter is pressed in searchbox
	def search(self, searchstring):
		self.updatetable(searchstring)

	#raises the details frame
	def showdetails(self):
		self.details_frame.tkraise()
		self.details_right_column.tkraise()
	def showdetailsevent(self,event):
		self.showdetails()

	#raises the list frame
	def showlist(self):
		self.content_frame.tkraise()
		self.main_right_column.tkraise()
	def showlistevent(self,event):
		self.showlist()

	#listbox scrollbar 
	def OnVsb(self, *args):
		for listbox in self.listbox_list:
			listbox.yview(*args)

	def OnMouseWheel(self, event):
		for listbox in self.listbox_list:
			listbox.yview("scroll", -event.delta,"units")
		# this prevents default bindings from firing, which
		# would end up scrolling the widget twice
		return "break"

	#Empties table
	def cleartable(self):
		for listbox in self.listbox_list:
			listbox.delete(0,END)

	#Fills table with data
	def updatetable(self,searchterm):
		#Set all listboxes to be enabled
		for listbox in self.listbox_list:
			listbox.configure(state=NORMAL)
		#Empty table to populate it again
		self.cleartable()
		for softwarechunk in self.softwarelist:
			softwarename = softwarechunk["software"]
			#insert name of software in software column
			self.software_listbox.insert(END, softwarename)
			
			with open(softwarechunk["githubjson"], encoding="utf-8") as json_file: 
				jfile = json.load(json_file) 
			version = jfile[0]["tag_name"]
			#Insert latest available software version in latest column
			self.latest_listbox.insert(END, version)

			#Check to see if and which version is installed 
			installedversion = self.version_function(self.softwaregroup,softwarechunk["software"])
			#If the installed version is up-to-date print a check mark, else insert not installed or the installed version
			if installedversion == version:
				self.status_listbox.insert(END, checkmark)
				self.status_listbox.itemconfig(END, foreground="white")
			elif installedversion == None:
				installedversion = "not installed"
				self.status_listbox.insert(END, installedversion)

			else: 
				self.status_listbox.insert(END, installedversion)

			#Get the genre of the software item and insert it
			group = softwarechunk["group"]
			self.genre_listbox.insert(END, group)

			#If a search term has been specified with the table update, hilight items that match the search term
			if searchterm == None:
				self.software_listbox.itemconfig(END,foreground=listbox_font_color)
			else:
				if searchterm.lower() in softwarename.lower() or searchterm.lower() in group.lower() or version.lower().startswith(searchterm.lower()):
					self.software_listbox.itemconfig(END,foreground=listbox_font_color)
				else:
					self.software_listbox.itemconfig(END,foreground=dark_listbox_font_color)
		for listbox in self.listbox_list:
			listbox.configure(state=DISABLED)      
		self.software_listbox.configure(state=NORMAL)


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
	def updateinfobox(self):
		for listbox in self.listbox_list:
			listbox.selection_clear(0,len(self.softwarelist)-1)
			listbox.selection_set(self.currentselection)
			listbox.see(self.currentselection)

		if not self.softwarelist == {} and not self.softwarelist == []:

			softwarename = self.softwarelist[self.currentselection]["software"]
			self.infobox.updatetitle(softwarename)

			with open(self.softwarelist[self.currentselection]["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)

			#update author
			author = jfile[0]["author"]["login"]
			self.infobox.updateauthor(author)

			self.updateAuthorImage()

			self.infobox.updatedescription(self.softwarelist[self.currentselection]["description"])
		else:
			pass

	def updateAuthorImageEvent(self,event):
		self.updateAuthorImage()

	def updateAuthorImage(self):
		softwarename = self.softwarelist[self.currentselection]["software"]
		photopath = homebrewcore.checkphoto(homebrewcore.imagecachefolder, softwarename)
		if self.softwarelist[self.currentselection]["photopath"] == None:
			self.softwarelist[self.currentselection]["photopath"] = photopath

		if not photopath == None:
			photopath = homebrewcore.joinpaths(homebrewcore.imagecachefolder, photopath)
			photoexists = homebrewcore.exists(photopath)
		else:
			photoexists = False

		if not photoexists:
			try:
				with open(self.softwarelist[self.currentselection]["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
					jfile = json.load(json_file)
					url = jfile[0]["author"]["avatar_url"]
				photopath = webhandler.cacheimage(url,softwarename)
				self.softwarelist[self.currentselection]["photopath"] = photopath
			except: 
				print("could not download icon image (you can safely ignore this error)")
				photopath = homebrewcore.joinpaths(homebrewcore.assetfolder,notfoundimage)
		try:
			project_image = tk.PhotoImage(file=photopath)

		except:
			photopath = homebrewcore.joinpaths(homebrewcore.assetfolder,notfoundimage)
			print("used not-found image due to error (you can safely ignore this error)")

		self.infobox.updateimage(image_path = photopath)


#movement button callbacks, moves up or down main list
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
		except:
			pass
	def pageup(self):
		if self.currentselection < len(self.softwarelist)-1:
			self.currentselection += 1
			self.currenttagselection = 0
			self.updateinfobox()
			self.refreshdetailwindow()
	def pagedown(self):
		if self.currentselection > 0:
			self.currentselection -= 1
			self.currenttagselection = 0
			self.updateinfobox()
			self.refreshdetailwindow()


#movement button callbacks, moves up or down details list
	#get current selection subversion from list box
	def CurTagSelet(self, event):
		try:
			widget = event.widget
			self.currenttagselection=widget.curselection()[0]
			self.updatetagsbox()
			self.updatetagnotes()
		except:
			pass
	def versioncursorup(self):
		if self.currenttagselection < guicore.taglen-1:
			self.currenttagselection += 1
			self.updatetagsbox()
			self.updatetagnotes()
	def versioncusordown(self):
		if self.currenttagselection > 0:
			self.currenttagselection -= 1
			self.updatetagsbox()
			self.updatetagnotes()








	def updatetagsbox(self):
		self.tags_listbox.selection_clear(0,END)
		self.tags_listbox.selection_set(self.currenttagselection)
		self.tags_listbox.see(self.currenttagselection)

	def updatetagnotes(self):
		with open(self.softwarelist[self.currentselection]["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
		tagnotes = jfile[self.currenttagselection]["body"]
		self.scrolling_patch_notes.configure(state=NORMAL)
		self.scrolling_patch_notes.delete('1.0', END)
		self.scrolling_patch_notes.insert(END, tagnotes)
		self.scrolling_patch_notes.configure(state=DISABLED)

	def gettagdescription(self,index_string):
		with open(self.softwarelist[self.currentselection]["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

		for version in jfile:
			if index_string == version["tag_name"]:
				tagnotes = version["body"]

		self.updatetagnotes()

	def refreshdetailwindow(self,):
		guicore.taglen = 0
		self.currenttagselection = 0
		self.tags_listbox.delete(0,END)
		if not self.softwarelist == []:
			with open(self.softwarelist[self.currentselection]["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)

			for version in jfile:
				guicore.taglen+=1
				tag = version["tag_name"]
				self.tags_listbox.insert(END, tag)

			self.updatetagsbox()
			self.updatetagnotes()

		else:
			pass

	#Update page whenever it is raised
	def on_show_frame(self,event):
		self.updatewindow()
		self.updateinfobox()

	def updatewindow(self):
		self.updatetable(None)
		self.refreshdetailwindow()

	#Opens the project page for currently selected homebrew
	def openprojectpage(self):
		url = self.softwarelist[self.currentselection]["projectpage"]
		if url == None:
			print("No project page found, generating from github api link")
			url = webhandler.parse_api_to_standard_github(self.softwarelist[self.currentselection]["githubapi"])
		print("Opening {}".format(url))
		webhandler.opentab(url)

