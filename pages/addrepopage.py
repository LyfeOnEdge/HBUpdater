from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.homebrewcore as homebrewcore
import modules.webhandler as webhandler

import tkinter as tk
from tkinter.constants import *

import json
import sys,subprocess


sd_subfolder_placeholder = "SD subfolder (blank for root)"
genre_placeholder = "Genre"
repo_description_placeholder = "(Optional) Repo Description"


new_url_placeholder = "Repo URL in format: https://www.github.com/author/repo"
new_subfolder_placeholder = "SD subfolder (blank for root)"
new_genre_placeholder = "Genre"
new_description_placeholder = "(Optional) Repo Description"

REPOGUIDETEXT = """Usage Guide:

Click new, fill out the various fields, and hit save to add a new repo. 

To edit a repo: select the repo you wish to edit, change desired values, and click save.

#REPO URL: Add your github repo link in format https://github.com/Author/Repo.

#SD SUBFOLDER: The subfolder to install to on the SD card. Usually "/" or "/switch" (lower case). Check out the readme for the github repo you are adding if you don't know as it will likely tell you. Sometimes .zips contain the subfolders with in them and can be extracted to the root. In this case leave the SD subfolder field blank. 

#GENRE: Makes no difference in functionality, you can set this to whatever you want.

#DESCRIPTION: Not required, but nice."""

#Main screen for adding repositories to the gui
class addRepoScreen(cw.themedframe):
	def __init__(self, parent, controller,back_command):
		cw.themedframe.__init__(self,parent,background_color= light_color)

		#Screen for viewing current repos
		self.mainreposcreen = cw.themedframe(self,background_color=light_color)
		self.mainreposcreen.place(x=0,y=0,relwidth=1,relheight=1)

		self.listboxframe = cw.themedframe(self.mainreposcreen)
		self.listboxframe.place(x=+repolistboxseparatorwidth,y=+repolistboxseparatorwidth,relwidth=1, width=-(infoframewidth+repolistboxseparatorwidth), relheight=1,height=-(4*entryheight+repolistboxseparatorwidth))

		self.listboxlist = []
		self.repolistboxframe = cw.titledlistboxframe(self.listboxframe,"Repo")
		self.repolistboxframe.place(relx=0,rely=0,relwidth=1,relheight=1,)
		self.repolistbox = cw.customlistbox(self.listboxframe)
		self.repolistbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-(lbcolumnoffset+2*repocolumnwidth), y=columtitlesheight+repolistboxseparatorwidth,height=-(columtitlesheight+injector_separator_width))
		self.repolistbox.bind('<<ListboxSelect>>',self.CurSelet)

		self.listboxlist.append(self.repolistbox)

		self.authorseparator = cw.separator(self.listboxframe)
		self.authorseparator.place(relx=1,x=-3*repocolumnwidth,rely=0,width=repolistboxseparatorwidth,relheight=1,)
		self.authorlistboxframe = cw.titledlistboxframe(self.listboxframe,"Author")
		self.authorlistboxframe.place(relx=1,x=-3*repocolumnwidth+repolistboxseparatorwidth,rely=0,relheight=1, width=repocolumnwidth,)
		self.authorlistbox = cw.customlistbox(self.listboxframe)
		self.authorlistbox.place(relx=1,x=-3*repocolumnwidth+repolistboxseparatorwidth+lbcolumnoffset,rely=0,relheight=1, width=repocolumnwidth, y=columtitlesheight+repolistboxseparatorwidth, height=-(columtitlesheight+injector_separator_width))
		self.listboxlist.append(self.authorlistbox)

		self.groupseparator = cw.separator(self.listboxframe)
		self.groupseparator.place(relx=1,x=-2*repocolumnwidth,rely=0,width=repolistboxseparatorwidth,relheight=1,)
		self.grouplistboxframe = cw.titledlistboxframe(self.listboxframe,"Genre")
		self.grouplistboxframe.place(relx=1,x=-2*repocolumnwidth+repolistboxseparatorwidth,rely=0,relheight=1, width=repocolumnwidth,)
		self.grouplistbox = cw.customlistbox(self.listboxframe)
		self.grouplistbox.place(relx=1,x=-2*repocolumnwidth+repolistboxseparatorwidth+lbcolumnoffset,rely=0,relheight=1, width=repocolumnwidth, y=columtitlesheight+repolistboxseparatorwidth, height=-(columtitlesheight+injector_separator_width))
		self.listboxlist.append(self.grouplistbox)

		self.sdseparator = cw.separator(self.listboxframe)
		self.sdseparator.place(relx=1,x=-repocolumnwidth,rely=0,width=repolistboxseparatorwidth,relheight=1,)
		self.sdlistboxframe = cw.titledlistboxframe(self.listboxframe,"Subfolder")
		self.sdlistboxframe.place(relx=1,x=-repocolumnwidth+repolistboxseparatorwidth,rely=0,relheight=1, width=repocolumnwidth,)
		self.sdlistbox = cw.customlistbox(self.listboxframe)
		self.sdlistbox.place(relx=1,x=-repocolumnwidth+repolistboxseparatorwidth+lbcolumnoffset,rely=0,relheight=1, width=repocolumnwidth, y=columtitlesheight+repolistboxseparatorwidth, height=-(columtitlesheight+injector_separator_width))
		self.listboxlist.append(self.sdlistbox)

		for listbox in self.listboxlist:
			listbox.bind("<MouseWheel>", self.OnMouseWheel)

		self.iconspacer = 0

		self.bottomseparator = cw.separator(self.listboxframe)
		self.bottomseparator.place(relx=0,rely=1,y=-repolistboxseparatorwidth,relwidth=1, height=repolistboxseparatorwidth)

		self.horizontalseparator = cw.separator(self.listboxframe)
		self.horizontalseparator.place(relx=0,rely=0,y=columtitlesheight,height=repolistboxseparatorwidth,relwidth=1,)

		self.repoframe = cw.themedframe(self.mainreposcreen,background_color= light_color)
		self.repoframe.place(relx=0, rely=1, y=-((4*entryheight)+separatorwidth),relwidth=1, width=-(infoframewidth), height=((4*entryheight)+separatorwidth))
		
		self.entryboxlist=[]
		self.iconspacer = 0
		self.urlbox_frame = cw.themedframe(self.repoframe,background_color=light_color,)
		self.urlbox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-(4*entryheight)-separatorwidth)
		self.urlbox = cw.entrybox(self.urlbox_frame, 
			command=lambda: self.saveedits(), 
			placeholder="Gituhub Repo URL",
			)
		self.urlbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-self.iconspacer, height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )

		self.entryboxlist.append(self.urlbox)

		self.iconspacer = 0
		self.subfolderbox_frame = cw.themedframe(self.repoframe,background_color=light_color,)
		self.subfolderbox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-(3*entryheight)-separatorwidth)
		self.subfolderbox = cw.entrybox(self.subfolderbox_frame, 
			command=lambda: self.saveedits(), 
			placeholder=sd_subfolder_placeholder,
			)
		self.subfolderbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )

		self.entryboxlist.append(self.subfolderbox)

		self.genrebox_frame = cw.themedframe(self.repoframe,background_color=light_color,)
		self.genrebox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-(2*entryheight)-separatorwidth)
		self.genrebox = cw.entrybox(self.genrebox_frame, 
			command=lambda: self.saveedits(), 
			placeholder=genre_placeholder,
			)
		self.genrebox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )

		self.entryboxlist.append(self.genrebox)

		self.iconspacer = 0
		self.descriptionbox_frame = cw.themedframe(self.repoframe,background_color=light_color,)
		self.descriptionbox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-entryheight-separatorwidth, )
		self.descriptionbox = cw.entrybox(self.descriptionbox_frame, 
			command=lambda: self.saveedits(), 
			placeholder=repo_description_placeholder,
			)
		self.descriptionbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )

		self.entryboxlist.append(self.descriptionbox)


		

		self.repoguide = cw.ScrolledText(self.mainreposcreen,
			background=light_color,
			foreground=guidetextcolor,
			wrap="word",
			highlightthickness=0,
			borderwidth=0,
			font=repoguidefont
			)
		self.repoguide.place(relx=1,x=-infoframewidth+2,rely=0,y=+separatorwidth,width=infoframewidth-2,relheight=1,height=-((87.5+45.75)+separatorwidth))
		self.repoguide.configure(state=NORMAL)
		self.repoguide.insert(END, REPOGUIDETEXT)
		self.repoguide.configure(state=DISABLED)

		self.infobox = cw.infobox(self.mainreposcreen)
		self.infobox.place(relx=1, x=-infoframewidth, rely=1, y=-87.5, height=87.5, width=infoframewidth)
		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)
		#Back to list button frame, placed first so the details button covers it
		self.repobuttons =cw.navbox(self.infobox,
			primary_button_command = lambda: self.saveedits(), 
			primary_button_text="SAVE",
			etc_button_image = self.returnimage,
			etc_button_command = lambda: controller.show_frame("mainPage"),
			left_context_command = lambda: self.prevbuttonpress(),
			right_context_command = lambda: self.nextbuttonpress(),
			)
		self.repobuttons.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)

		self.trashimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder, "trash.png"))
		self.trashimage= self.trashimage.subsample(2)

		self.hackynewanddeletebuttons = cw.navbox(self.mainreposcreen,
			primary_button_command = lambda: self.shownewreposcreen(), 
			primary_button_text="NEW",
			etc_button_image = self.trashimage,
			etc_button_command = lambda: self.removerepo(),
			left_context_command = None,
			right_context_command = None,
			)
		self.hackynewanddeletebuttons.place(relx=1, rely=1, x=-200, y=-(87.5+45.75), height= 43.75, width=200)

		self.reloadreopscreen()

		#frame for adding new repo
		self.addreposcreen = cw.themedframe(self,background_color=light_color)
		self.addreposcreen.place(x=0,y=0,relwidth=1,relheight=1)

		self.addrepoframe = cw.themedframe(self.addreposcreen,background_color= light_color)
		self.addrepoframe.place(relx=0, rely=0,relwidth=1, height=4*entryheight+separatorwidth)
		
		self.newentryboxlist=[]
		self.iconspacer = separatorwidth
		self.new_urlbox_frame = cw.themedframe(self.addrepoframe,background_color=light_color,)
		self.new_urlbox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-(4*entryheight)-separatorwidth)
		self.new_urlbox = cw.entrybox(self.new_urlbox_frame,  
			placeholder=new_url_placeholder,
			)
		self.new_urlbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-self.iconspacer, height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )
		self.newentryboxlist.append(self.new_urlbox)

		self.new_subfolderbox_frame = cw.themedframe(self.addrepoframe,background_color=light_color,)
		self.new_subfolderbox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-(3*entryheight)-separatorwidth)
		self.new_subfolderbox = cw.entrybox(self.new_subfolderbox_frame, 
			placeholder=new_subfolder_placeholder,
			)
		self.new_subfolderbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )
		self.newentryboxlist.append(self.new_subfolderbox)

		self.new_genrebox_frame = cw.themedframe(self.addrepoframe,background_color=light_color,)
		self.new_genrebox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-(2*entryheight)-separatorwidth)
		self.new_genrebox = cw.entrybox(self.new_genrebox_frame, 
			placeholder=new_genre_placeholder,
			)
		self.new_genrebox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )
		self.newentryboxlist.append(self.new_genrebox)

		self.new_descriptionbox_frame = cw.themedframe(self.addrepoframe,background_color=light_color,)
		self.new_descriptionbox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-entryheight-separatorwidth, )
		self.new_descriptionbox = cw.entrybox(self.new_descriptionbox_frame, 
			placeholder=new_description_placeholder,
			)
		self.new_descriptionbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )
		self.newentryboxlist.append(self.new_descriptionbox)

		self.download_github_button = cw.navbutton(self.addreposcreen,command_name = lambda: self.download_json_then_list_assets(), text_string="Get Repo Data")
		self.download_github_button.place(relx=0,rely=0,y=+((4*entryheight)+separatorwidth),x=0,height=navbuttonheight,width=3*navbuttonheight)

		self.get_repo_data_button_guide = cw.themedguidelabel(self.addreposcreen,"""^Fill out the fields above\n<-Then click this button to download the repo information from github""")
		self.get_repo_data_button_guide.place(relx=0,rely=0,y=+((4*entryheight)+separatorwidth),relwidth=1, width=-3*navbuttonheight, x=+3*navbuttonheight,height=navbuttonheight)


		self.assetsframe = cw.themedframe(self.addreposcreen,background_color=light_color)
		self.assetsframe.place(relx=0,rely=0,y=((4*entryheight)+2*separatorwidth+navbuttonheight),relwidth=1,  relheight=1,height=-((4*entryheight)+2*separatorwidth+navbuttonheight))
		self.assetslistbox = cw.ScrolledListBox(self.assetsframe,borderwidth=0,highlightthickness=0,background=dark_color,foreground=w)
		self.assetslistbox.place(x=+separatorwidth,y=0,relwidth=1,relheight=1, width=-2*separatorwidth, height=-(2*separatorwidth+2*navbuttonheight))
		self.assetsguide = cw.themedguidelabel(self.assetsframe, "^Select github asset you wish to manage with this repo. \n This relies on the repo's developer releasing the app with a consistent format.",)
		self.assetsguide.place(x=0,rely=1,y=-(2*navbuttonheight+separatorwidth), relwidth=1,height=navbuttonheight)
		self.finaladdrepobutton = cw.navbutton(self.assetsframe, text_string="ADD REPO", command_name=lambda: self.addrepo())
		self.finaladdrepobutton.place(rely=1,relx=0,x=+separatorwidth,y=-(navbuttonheight+separatorwidth),height=navbuttonheight,width=3*navbuttonheight)

		self.dummyframe = cw.themedframe(self.addreposcreen,background_color=light_color)
		self.dummyframe.place(relx=0,rely=0,y=((4*entryheight)+2*separatorwidth+navbuttonheight),relwidth=1,  relheight=1,height=-((4*entryheight)+2*separatorwidth+navbuttonheight))

		self.returnbuttonframe = cw.themedframe(self.addreposcreen)
		self.returnbuttonframe.place(relx=1,rely=1,x=-(navbuttonspacing+navbuttonheight), y=-(navbuttonspacing+navbuttonheight),height=navbuttonheight, width=navbuttonheight)
		self.returntoreposcreenbutton = cw.navbutton(self.returnbuttonframe,image_object=self.returnimage,command_name=lambda: self.showmainreposcreen())
		self.returntoreposcreenbutton.place(relwidth=1,relheight=1)

		self.raiseframe(self.mainreposcreen)
		
		#fill out info
		#Get json
		#fill lisbox
		#raise listbox and submit button
		#user selects item from listbox
		#submitbutton becomes undisabled
		#user submits new repo
	def download_json_then_list_assets(self):
		url = self.new_urlbox.get_text().strip("/")
		if url == "" or url == None:
			print("No url to parse")
			return
		desc = self.new_descriptionbox.get_text()
		subfolder = self.new_subfolderbox.get_text()
		genre = self.new_genrebox.get_text()

		if desc == None or desc == "":
			desc = "Added by user, you can edit this description in the repos menu."
		if genre == None or genre == "":
			genre = "user repo"


		repochunk = guicore.getrepochunkfromurl(url,desc,subfolder,genre)
		# print(json.dumps(repochunk,indent=4))

		guicore.newrepotempvariable = repochunk

		with open(guicore.newrepotempvariable["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

			if jfile == [] or jfile == None:
				print("""No api data, it looks like the repository you are trying to add 
	has no official releases, talk to the repo author and ask them to 
	release it in order to use it with HBUpdater.""")
				return

			if len(jfile[0]["assets"]) == 0:
				print("No assets")
				return

			self.assetslistbox.delete(0,END)
			for asset in jfile[0]["assets"]:
				self.assetslistbox.insert(END,asset["name"])

			self.raiseframe(self.assetsframe)

	def addrepo(self):
		print("adding repo")
		
		try:
			assetnum = self.assetslistbox.curselection()[0]
		except:
			print("no asset selected")
			return

		print("asset chosen: {}".format(assetnum))

		guicore.newrepotempvariable["github_asset"] = assetnum
		print(json.dumps(guicore.newrepotempvariable,indent=4))

		newentry = {
						guicore.newrepotempvariable["software"] : guicore.newrepotempvariable
					}

		guicore.hbdict.append(guicore.newrepotempvariable)
		guicore.setDict(guicore.hbdict)
		guicore.updateguirepos(newentry)
		guicore.newrepotempvariable = {}
		print("repo successfully added")
		self.reloadreopscreen()

	def saveedits(self):
		url = self.urlbox.get_text()

		desc = self.descriptionbox.get_text()
		if desc == repo_description_placeholder:
			desc = None

		subfolder = self.subfolderbox.get_text()
		if sd_subfolder_placeholder == subfolder:
			subfolder = None

		genre = self.genrebox.get_text()
		if genre == genre_placeholder:
			genre = None

		repochunk = guicore.getrepochunkfromurl(url,desc,subfolder,genre)
		print(json.dumps(repochunk,indent=4))

		with open(repochunk["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)

		if jfile == [] or jfile == None:
			print("""No api data, it looks like the repository you are trying to add 
has no official releases, talk to the repo author and ask them to 
release it in order to use it with HBUpdater.""")
			return

		if len(jfile[0]["assets"]) == 0:
			print("No assets")
			return

		newentry = {
						repochunk["software"] : repochunk
					}

		guicore.updateguirepos(newentry)

		chunk = 0
		for softwarechunk in guicore.hbdict:
			if softwarechunk["software"] == repochunk["software"]:
				guicore.hbdict[chunk] = repochunk
				guicore.setDict(guicore.hbdict)
				self.reloadreopscreen()
				return
			else:
				chunk +=1
		print("If you are seeing this message, there is a bug in the 'add repo' screen, and your repo was not added")
		return

	def removerepo(self):
		selectiontoremove = guicore.repolist[guicore.currepo]["software"]
		print("removing repo {}".format(selectiontoremove))
		guicore.removeitemfromrepo(selectiontoremove)

		for softwarechunk in guicore.hbdict:
			if softwarechunk["software"] == selectiontoremove:
				guicore.hbdict.remove(softwarechunk)

		guicore.setDict(guicore.hbdict)
		guicore.currepo = 0
		self.setrepostrings()
		self.reloadreopscreen()

	def OnMouseWheel(self, event):
		for listbox in self.listboxlist:
			listbox.yview("scroll", -event.delta,"units")
		# this prevents default bindings from firing, which
		# would end up scrolling the widget twice
		return "break"

	#get current selection from list box
	def CurSelet(self, event):
		widget = event.widget
		selection=widget.curselection()
		picked = widget.get(selection[0])
		guicore.currepo = widget.get(0, END).index(picked)
		self.reloadreopscreen()
		
	def reloadreopscreen(self):
		guicore.makerepodict()
		self.populaterepobox()
		self.setrepostrings()

	def clearboxes(self):
		for entry in self.entryboxlist:
			entry.clear()
	
	def populaterepobox(self):
		self.authorlistbox.config(state=NORMAL)
		self.grouplistbox.config(state=NORMAL)
		self.sdlistbox.config(state=NORMAL)
		for listbox in self.listboxlist:
			listbox.delete(0,END)
		if not guicore.repolist == None:
			for repo in guicore.repolist:
					softwarename = repo["software"]
					author = repo["author"]
					group = repo["group"]
					subfolder = repo["install_subfolder"]
					if subfolder == None or subfolder == "":
						subfolder = "root"
					self.repolistbox.insert(END, softwarename)
					self.authorlistbox.insert(END,author)
					self.grouplistbox.insert(END,group)
					self.sdlistbox.insert(END,subfolder)
			self.authorlistbox.config(state=DISABLED)
			self.grouplistbox.config(state=DISABLED)
			self.sdlistbox.config(state=DISABLED)

	def setrepostrings(self):
		self.repolistbox.selection_clear(0,len(guicore.repolist)-1)
		self.repolistbox.selection_set(guicore.currepo)
		if not guicore.repolist == []:
			url = guicore.repolist[guicore.currepo]["githuburl"]
			desc = guicore.repolist[guicore.currepo]["description"]
			subfolder = guicore.repolist[guicore.currepo]["install_subfolder"]
			genre = guicore.repolist[guicore.currepo]["group"]

			self.urlbox.enable()
			self.urlbox.set_text(url)
			self.urlbox.disable()
			self.descriptionbox.set_text(desc)
			self.subfolderbox.set_text(subfolder)
			self.genrebox.set_text(genre)

	def nextbuttonpress(self):
		if guicore.currepo < len(guicore.repolist)-1:
			guicore.currepo += 1
			self.setrepostrings()

	def prevbuttonpress(self):
		if guicore.currepo > 0:
			guicore.currepo -= 1
			self.setrepostrings()

	#raises specified frame, keeps return button on top
	def raiseframe(self,frame):
		frame.tkraise()
		self.returnbuttonframe.tkraise()

	def shownewreposcreen(self):
		self.addreposcreen.tkraise()

	def showmainreposcreen(self):
		self.mainreposcreen.tkraise()
