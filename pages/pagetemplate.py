from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.webhandler as webhandler
import modules.locations as locations
import modules.appstore as appstore

import tkinter as tk
from tkinter.constants import *

#If PIL is installed import the libraries needed for image scaling
if guicore.getpilstatus():
	from PIL import Image, ImageTk

import os, json

class page(cw.ThemedFrame,):
	#Call this with an appropriately formatted list to populate the table with
	def setlist(self,listy):
		self.basesoftwarelist = listy
		self.softwarelist = self.basesoftwarelist[:]

	def populatesoftwarelist(self,list):
		if guicore.checkguisetting("guisettings","automatically_check_for_repo_updates"):
			populatedlist = webhandler.getUpdatedSoftwareLinks(list) #use this to download new json (required to get updates)
		else:
			populatedlist = webhandler.getJsonSoftwareLinks(list) #use this to use only pre-downloaded json files
		for softwarechunk in populatedlist:
			softwarechunk["photopath"] = None
			try:
				se = softwarechunk["store_equivalent"]
				if not se:
					softwarechunk["store_equivalent"] = softwarechunk["software"]
			except:
				softwarechunk["store_equivalent"] = softwarechunk["software"]

		return(populatedlist)

	#Call this with a list of image objects, tooltips, and associated callbacks to initialize the search box and add buttons
	#It will automatically generate a row of buttons depending on how the page was initialized 
	def setbuttons(self,buttonlist):
		if not self.pagetitle == None: #If a title has been specified make it and space it to fit with the buttons
			self.iconspacer = 5*searchboxheight - icon_and_search_bar_spacing
			self.titleframe = cw.ThemedFrame(self.searchbox_frame,background_color=light_color)
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
			self.buttonobj = cw.navbutton(self.searchbox_frame,image_object=button["image"],command_name=button["callback"])
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
		latest_function=None,				#Set this to override the default callback used to populate the latest column using the software's name
		genre_function=None,				#Set this to override the default callback used to populate the genre column
		status_column="INSTALLED",			#Set this to override the status column title
		page_title=None,					#Set this to apply a page title by the buttons and search box, leave blank to exclude it
		page_name=None,
		softwaregroup=None, 				#Set this to the keyword section of the tracking file to log installed software to
		noimage = None,						#Set this to true to disable the info box
		nodetail = None,
		):

		self.page_name = page_name
		self.controller = controller		#Controller (most toplevel parent)
		self.softwaregroup = softwaregroup	#Make group available
		self.softwarelist = []				#list to hold software data to populate table and more
		self.currentselection = 0			#Variable to track currently selected software
		self.currenttagselection = 0		#Variable to track currently selected sub-version
		self.pagetitle = page_title
		self.noimage = noimage
		self.nodetail = nodetail

		if latest_function:
			self.latest_function = latest_function
		else:
			self.latest_function = self.get_latest_store_version

		if version_function:		
			self.version_function = version_function
		else:
			self.version_function = self.get_installed_version

		if genre_function:
			self.genre_function = genre_function
		else:
			self.genre_function = self.get_genre

		cw.ThemedFrame.__init__(self,parent)#Init frame
		self.bind("<<ShowFrame>>", self.on_show_frame) #Bind on_show_frame to showframe event
		


		base_x = 40

		#Default image handling, when pillow isn't installed
		if not guicore.getpilstatus():
			#Shared images
			self.infoimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"info.png")).zoom(3).subsample(5)
			self.returnimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"returnbutton.png")).zoom(3).subsample(5)
			self.addrepoimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"plus.png")).subsample(2)
			self.sdimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"sd.png")).zoom(2).subsample(4)
		else:
			#open, resize, and convert images to tk format using pillow
			self.infoimage = ImageTk.PhotoImage(Image.open(os.path.join(locations.assetfolder,"info.png")).resize((base_x, base_x), Image.ANTIALIAS))
			self.returnimage = ImageTk.PhotoImage(Image.open(os.path.join(locations.assetfolder,"returnbutton.png")).resize((base_x, base_x), Image.ANTIALIAS))
			self.addrepoimage = ImageTk.PhotoImage(Image.open(os.path.join(locations.assetfolder,"plus.png")).resize((int(base_x*.9), int(base_x*.9)), Image.ANTIALIAS))
			self.sdimage = ImageTk.PhotoImage(Image.open(os.path.join(locations.assetfolder,"sd.png")).resize((int(base_x*.8), int(base_x*.8)), Image.ANTIALIAS))
		
		



		

		#Full window frame, holds everything
		self.outer_frame = cw.ThemedFrame(self,frame_borderwidth=0,frame_highlightthickness= 0)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

		#Frame for main list, contains listboxes and scroll bar, and list titles
		self.content_frame = cw.ThemedFrame(self.outer_frame,frame_borderwidth=0,frame_highlightthickness= 0)
		self.content_frame.place(relx=0.0, rely=0.0, relheight=1, relwidth=1, width=-infoframewidth,)
		self.content_frame.configure(background=dark_color)

		#The contents of this frame are built backwards in self.setbutton due to needing to align the searchbox with the icons
		self.searchbox_frame = cw.ThemedFrame(self.content_frame,frame_highlightthickness= 0,background_color=light_color, frame_borderwidth = 0)
		self.searchbox_frame.place(relx=0.0, rely=0.0,height=searchboxheight, relwidth=1,)

		#vertical scroll bar (Not placed, trying to make it only appear when needed)
		self.vsb = tk.Scrollbar(self.content_frame,orient="vertical", command=self.OnVsb)
		# self.vsb.place(relx=0.975, rely=0.15, relheight=0.94, relwidth=0.025)


		self.list_frame = cw.ThemedFrame(self.content_frame,frame_highlightthickness=0)
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
		self.details_frame = cw.ThemedFrame(self.outer_frame)
		self.details_frame.place(relx=0.0, rely=0.0, width=-infoframewidth, relheight=1, relwidth=1)
		

		self.tags_listbox = cw.ThemedListbox(self.details_frame)
		self.tags_listbox.place(relx=0.0, rely=0, relheight=1, relwidth=0.2)
		self.tags_listbox.configure(font=tags_listbox_font)
		self.tags_listbox.configure(font=version_number_font)
		self.tags_listbox.bind('<<ListboxSelect>>',self.CurTagSelet)

		self.patch_notes_separator = cw.Separator(self.details_frame)
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
		self.rightcolumn = cw.ThemedFrame(self, frame_borderwidth=0,frame_highlightthickness=0)
		self.rightcolumn.place(relx=1, x=-infoframewidth, rely=0.0, relheight=1, width=infoframewidth)

		#column to hold usage details, set using self.setlist()
		self.details_right_column = cw.ThemedFrame(self.rightcolumn, frame_borderwidth=0,frame_highlightthickness=0,background_color=light_color)
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
			etc_button_image = self.returnimage,
			etc_button_command = self.showlist,
			left_context_command = self.versioncusordown,
			right_context_command = self.versioncursorup,
			)
		self.details_buttons.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)


		#Main column with software details and more
		self.main_right_column = cw.ThemedFrame(self.rightcolumn, frame_borderwidth=0,frame_highlightthickness=0,background_color=light_color)
		self.main_right_column.place(relwidth = 1, relheight=1)

		self.infobox = infobox(self.main_right_column)
		#only place infobox if we need it
		if not self.noimage:
			self.infobox.place(relwidth=1,relheight=1,)


		if primary_button_command == None:
			pbc = self.install
			self.software_listbox.bind('<Double-Button-1>', self.install)
		else:
			pbc = primary_button_command
			self.software_listbox.bind('<Double-Button-1>', primary_button_command)



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
	def setSDpath(self, evnt=None):
		chosensdpath = tk.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
		HBUpdater.setSDpath(chosensdpath)
		self.on_show_frame(None)

	#Installs selected software, brings up sd card selection if it hasn't been selected yet
	def install(self, evnt=None):
		sc = self.softwarelist[self.currentselection]

		if HBUpdater.sdpathset:
			HBUpdater.installitem(sc,  0)
			self.updatetable(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(sc, 0)
				self.updatetable(None)
			else:
				print("SD Path Not set, not installing")

	#Installs specific version of selected software, brings up sd card selection if it hasn't been selected yet
	def specificinstall(self, evnt=None):
		sc = self.softwarelist[self.currentselection]

		if HBUpdater.sdpathset:
			HBUpdater.installitem(sc, self.currenttagselection)
			self.updatetable(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.installitem(sc, self.currenttagselection)
				self.updatetable(None)
			else:
				print("SD Path Not set, not installing")

	#Uninstalls selected software, brings up sd card selection if it hasn't been selected yet
	def uninstall(self):
		sc = self.softwarelist[self.currentselection]

		try:
			se = sc["store_equivalent"]
		except:
			se = None

		if HBUpdater.sdpathset:
			HBUpdater.uninstallsoftware(se)
			self.updatetable(None)
		else:
			self.setSDpath()

			if HBUpdater.sdpathset:
				HBUpdater.uninstallsoftware(se)
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
			
			#Insert newest available software version in latest column
			version = self.latest_function(softwarechunk)
			self.latest_listbox.insert(END, version)

			#Check to see if and which version is installed 
			installedversion = self.version_function(softwarechunk["store_equivalent"])
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

			group = self.genre_function(softwarechunk)
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

	#Takes a list chunk, returns newest version. Default latest version check
	def get_latest_version(self, chunk):
		try:
			jsn = chunk["githubjson"]
			if os.path.isfile(jsn):
				with open(jsn, encoding="utf-8") as json_file: 
					jfile = json.load(json_file) 
				version = jfile[0]["tag_name"]
			else:
				version = "unknown"
		except Exception as e:
				print("get_latest_version error {}".format(e))

				version = "unknown"
		return version

	#Takes a list chunk, returns newest version. Default latest version check
	def get_latest_store_version(self, chunk):
		try:
			jsn = chunk["githubjson"]
			if os.path.isfile(jsn):
				with open(jsn, encoding="utf-8") as json_file: 
					jfile = json.load(json_file) 
				version = jfile[0]["tag_name"]
				try:
					se = chunk["store_equivalent"]
					if se:
						version = appstore.parse_version_to_store_equivalent(version, se)
				except:
					pass
			else:
				version = "unknown"
		except Exception as e:
				print("get_latest_version error {}".format(e))

				version = "unknown"
		return version

	def get_installed_version(self, package):
		return HBUpdater.get_app_status(package)

	#Not default but can be called with version_function
	#to populate table with data based on the store installed version
	def get_store_installed_version(self, software):
		try:
			store_package_name = HBUpdater.get_updater_equivalent(software)
			if store_package_name:
				version = HBUpdater.get_store_package_version(store_package_name)
			else:
				version = "not installed"
		except Exception as e:
			print(e)
			version = "not installed"

		return version

	def get_genre(self,chunk):
		return chunk["group"]

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

	def updatelistboxcursor(self):
		for listbox in self.listbox_list:
			listbox.selection_clear(0,len(self.softwarelist)-1)
			listbox.selection_set(self.currentselection)
			listbox.activate(self.currentselection)
			listbox.see(self.currentselection)

	#update all info in the info box
	def updateinfobox(self):
		self.updatelistboxcursor()

		if not self.noimage:

			if not self.softwarelist == {} and not self.softwarelist == []:

				sel = self.softwarelist[self.currentselection]

				softwarename = sel["software"]
				self.infobox.updatetitle(softwarename)

				try:
					with open(sel["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
						jfile = json.load(json_file)

					#update author
					author = jfile[0]["author"]["login"]
					

					self.updateAuthorImage()

				except Exception as e:
					print("updateinfobox error - {}".format(e))

					# try:
					self.updateAuthorImage()
					# except Exception as e2:
					# 	print("updateAuthorImage error - {}".format(e2))
					author = sel["author"]

				self.infobox.updateauthor(author)

				self.infobox.updatedescription(sel["description"])

			else:
				pass

	def updateAuthorImageEvent(self,event):
		self.updateAuthorImage()

	def updateAuthorImage(self):
		sel = self.softwarelist[self.currentselection]
		#Variable to track if we have found the author image yet
		photopath = None
		notfound = os.path.join(locations.assetfolder,notfoundimage)
		

		#Check if we have already set the photopath, if so return the file
		if not sel["photopath"] == None:
			photopath = sel["photopath"]
			try:
				self.infobox.updateimage(image_path = photopath)
			except Exception as e:
				#if encountered an error with given photo path (wrong type, corrupt etc)
				if type(e) == 'TclError':
					self.infobox.updateimage(image_path = notfound)
					sel["photopath"] = notfound
					return

		#If gotten this far, check and see if we have already downloaded an image for this author
		authorname = sel["author"]
		#If authorname isn't none 
		if authorname:
			photopath = self.checkphoto(locations.imagecachefolder, authorname)
			if photopath:
				if sel["photopath"] == None:
					sel["photopath"] = photopath

				self.infobox.updateimage(image_path = photopath)
				return

		#If it wasn't already set, AND it hasn't been downloaded yet
		#Try getting it from the associated json
		try:
			with open(sel["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)
				url = jfile[0]["author"]["avatar_url"]

			if url:
				photopath = webhandler.cacheimage(url,authorname)
				sel["photopath"] = photopath
		except:
		#If that failed, take a stab in the dark with their github avatar image, this is useful for data sets without github jsons
			photopath = webhandler.guessgithubavatar(authorname)

			if photopath:
				sel["photopath"] = photopath

		#If the photopath is still none, use the not-found image
		if not photopath:
			photopath = notfound

		if sel["photopath"] == None:
			sel["photopath"] = photopath

		self.infobox.updateimage(image_path = photopath)

	def checkphoto(self,dir, photo):
		for s in os.listdir(dir):
			if os.path.splitext(s)[0] == photo and os.path.isfile(os.path.join(dir, s)):
				return os.path.join(dir, s)

		return None


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
		if self.currenttagselection < len(self.softwarelist)-1:
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
		try:
			with open(self.softwarelist[self.currentselection]["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
				jfile = json.load(json_file)
			tagnotes = jfile[self.currenttagselection]["body"]
			self.scrolling_patch_notes.configure(state=NORMAL)
			self.scrolling_patch_notes.delete('1.0', END)
			self.scrolling_patch_notes.insert(END, tagnotes)
			self.scrolling_patch_notes.configure(state=DISABLED)
		except:
			self.scrolling_patch_notes.configure(state=NORMAL)
			self.scrolling_patch_notes.delete('1.0', END)
			self.scrolling_patch_notes.insert(END, "Error, no content to display")
			self.scrolling_patch_notes.configure(state=DISABLED)

	def gettagdescription(self,index_string):
		with open(self.softwarelist[self.currentselection]["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

		for version in jfile:
			if index_string == version["tag_name"]:
				tagnotes = version["body"]

		self.updatetagnotes()

	def refreshdetailwindow(self,):
		self.currenttagselection = 0
		self.tags_listbox.delete(0,END)

		if not self.nodetail:

			if not self.softwarelist == []:
				try:
					with open(self.softwarelist[self.currentselection]["githubjson"],encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
						jfile = json.load(json_file)

					for version in jfile:
						tag = version["tag_name"]
						self.tags_listbox.insert(END, tag)
				except:
					print("detailwindow refresh error - failed to load repo json - {}".format(self.softwarelist[self.currentselection]["software"]))

				self.updatetagsbox()
				self.updatetagnotes()

			else:
				pass

	#Update page whenever it is raised
	def on_show_frame(self,event):
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

	def refreshwindow(self):
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



#Displays author photo, name, project name, and project description on list (template) pages
class infobox(cw.ThemedFrame):
	def __init__(self,frame):
		cw.ThemedFrame.__init__(self,frame,background_color=light_color,frame_borderwidth=0)

		#holds author picture
		self.project_art_label = cw.ThemedLabel(self,label_text = "project_art",anchor="n")
		self.project_art_label.place(relx=0.0, rely=0.0, height=infoframewidth, relwidth=1)

		#Homebrew Title
		self.titlevar = tk.StringVar()
		self.titlevar.set("title_var")
		self.project_title_label = cw.ThemedLabel(self, 
			label_text = "project_title", 
			text_variable = self.titlevar, 
			foreground=info_softwarename_color, 
			label_font=info_softwarename_font,
			anchor="n"
			)
		self.project_title_label.place(relx=0.0, rely=0.0, y=infoframewidth, relwidth=1.0)


		#author name
		self.authorvar = tk.StringVar()
		self.authorvar.set("author_var")
		self.author_name_label = cw.ThemedLabel(self,
			label_text = "author_name", 
			text_variable = self.authorvar, 
			foreground=info_author_color, 
			label_font=info_author_font,
			anchor="n"
			)
		self.author_name_label.place(relx=0.0, rely=0, y=infoframewidth + 25,  relwidth=1.0)

		self.topsep = cw.ThemedFrame(self,
			background_color = lgray,
			frame_borderwidth = 2,
		)
		self.topsep.place(x = (infoframewidth / 2), y = infoframewidth+52, height = 4, relwidth = 0.9, anchor="center")

		#Description
		self.project_description = cw.ScrolledText(self,
			background=light_color,
			foreground=info_description_color,
			font=info_description_font,
			borderwidth=0,
			state=NORMAL,
			wrap="word",
			)
		self.project_description.place(relx=0.5, rely=0.0, y=+infoframewidth+55, relheight = 1, height=-(infoframewidth + 55 + 100), relwidth=0.85, anchor = "n")
		self.project_description.delete('1.0', END)
		self.project_description.insert(END, "Project description")
		self.project_description.configure(state=DISABLED)


		self.topsep = cw.ThemedFrame(self,
			background_color = lgray,
			frame_borderwidth = 2,
		)
		self.topsep.place(x = (infoframewidth / 2), rely = 1, y = -95, height = 4, relwidth = 0.9, anchor="center")


	def updatetitle(self,title):
		self.titlevar.set(title)

	#update author information
	def updateauthor(self,author):
		self.authorvar.set("by {}".format(author))

	def updateimage(self,image_path):
		#Default image handling method
		if not guicore.getpilstatus():
			imagemax = infoframewidth
			try:
				art_image = tk.PhotoImage(file=image_path)
			except:
				art_image = tk.PhotoImage(file=os.path.join(locations.assetfolder, "notfound.png"))
			while not (art_image.width() > (imagemax - 80) and not (art_image.width() > imagemax)):
				if art_image.width() > imagemax:
					art_image = art_image.subsample(2)
				if art_image.width() < (imagemax - 80):
					art_image = art_image.zoom(3)
		else:
		#Pillow handling
			art_image = Image.open(image_path)
			art_image = art_image.resize((infoframewidth, infoframewidth), Image.ANTIALIAS)
			art_image = ImageTk.PhotoImage(art_image)
		

		self.project_art_label.configure(image=art_image)
		self.project_art_label.image = art_image

	#update project description
	def updatedescription(self, desc):
		self.project_description.configure(state=NORMAL)
		self.project_description.delete('1.0', END)
		self.project_description.insert(END, desc)
		self.project_description.configure(state=DISABLED)

