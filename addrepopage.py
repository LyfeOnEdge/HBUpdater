import HBUpdater
from format import * 
import homebrewcore
import webhandler
import guicore

import tkinter as tk
from tkinter.constants import *
import customwidgets as cw

import json
import sys,subprocess


# #ijdict
# fuseefolder = homebrewcore.getpath("fusee-launcher")
#"Add repo in format 'https://github.com/author/repo'"



class addRepoScreen(cw.themedframe):
	def __init__(self, parent, controller,back_command):
		cw.themedframe.__init__(self,parent,frame_borderwidth=0,frame_highlightthickness= 0,background_color= light_color)

		self.listboxframe = cw.themedframe(self,frame_borderwidth=0,frame_highlightthickness= 0)
		self.listboxframe.place(x=+reposeparatorwidth,y=+reposeparatorwidth,relwidth=1, width=-(infoframewidth+reposeparatorwidth), relheight=1,height=-reposeparatorwidth)

		self.repolistboxframe = cw.titledlistboxframe(self.listboxframe,"Repo")
		self.repolistboxframe.place(relx=0,rely=0,relwidth=1,relheight=1,)
		self.repolistboxseparator = cw.separator(self.repolistboxframe)
		self.repolistboxseparator.place(relx=0,rely=0,y=columtitlesheight,height=reposeparatorwidth,relwidth=1,)
		self.repolistbox = cw.customlistbox(self.listboxframe)
		self.repolistbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset, y=columtitlesheight+reposeparatorwidth,height=-(columtitlesheight+injector_separator_width))

		self.separatorA = cw.separator(self.listboxframe)
		self.separatorA.place(relx=1,x=-validcolumnwidth,rely=0,width=reposeparatorwidth,relheight=1,)

		self.validlistboxframe = cw.titledlistboxframe(self.listboxframe,"Valid")
		self.validlistboxframe.place(relx=1,x=-validcolumnwidth+reposeparatorwidth,rely=0,relheight=1, width=validcolumnwidth,)
		self.validlistboxseparator = cw.separator(self.validlistboxframe)
		self.validlistboxseparator.place(relx=0,rely=0,y=columtitlesheight,height=reposeparatorwidth,relwidth=1,)
		self.validlistbox = cw.customlistbox(self.listboxframe)
		self.validlistbox.place(relx=1,x=-validcolumnwidth+reposeparatorwidth,rely=0,relheight=1, width=validcolumnwidth, y=columtitlesheight+reposeparatorwidth, height=-(columtitlesheight+injector_separator_width))

		self.iconspacer = 0

		self.bottomseparator = cw.separator(self.listboxframe)
		self.bottomseparator.place(relx=0,rely=1,y=-reposeparatorwidth,relwidth=1, height=reposeparatorwidth)

		self.repoframe = cw.themedframe(self,frame_borderwidth=0,frame_highlightthickness= 0,background_color= light_color)
		self.repoframe.place(relx=1,x=-infoframewidth, y=0, width=infoframewidth-icon_and_search_bar_spacing, relheight=1, height=-87.5,)

		self.iconspacer = 0
		self.urlbox_frame = cw.themedframe(self.repoframe,frame_borderwidth=0,frame_highlightthickness= 0,background_color=light_color,)
		self.urlbox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-(4*entryheight)-reposeparatorwidth)
		
		self.urlbox = cw.entrybox(self.urlbox_frame, 
			command=lambda: self.addrepo(), 
			placeholder="Gituhub Repo URL",
			)
		self.urlbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-self.iconspacer, height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )

		self.iconspacer = 0
		self.subfolderbox_frame = cw.themedframe(self.repoframe,frame_borderwidth=0,frame_highlightthickness= 0,background_color=light_color,)
		self.subfolderbox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-(3*entryheight)-reposeparatorwidth)
		self.subfolderbox = cw.entrybox(self.subfolderbox_frame, 
			command=lambda: self.addrepo(), 
			placeholder="SD subfolder (blank for root)",
			)
		self.subfolderbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )

		self.genrebox_frame = cw.themedframe(self.repoframe,frame_borderwidth=0,frame_highlightthickness= 0,background_color=light_color,)
		self.genrebox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-(2*entryheight)-reposeparatorwidth)
		self.genrebox = cw.entrybox(self.genrebox_frame, 
			command=lambda: self.addrepo(), 
			placeholder="Genre",
			)
		self.genrebox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )


		


		self.iconspacer = 0
		self.descriptionbox_frame = cw.themedframe(self.repoframe,frame_borderwidth=0,frame_highlightthickness= 0,background_color=light_color,)
		self.descriptionbox_frame.place(relx=0.0, rely=1, height=entryheight, relwidth=1,y=-entryheight-reposeparatorwidth, )
		self.descriptionbox = cw.entrybox(self.descriptionbox_frame, 
			command=lambda: self.addrepo(), 
			placeholder="(Optional) Repo Description",
			)
		self.descriptionbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=entryheight-icon_and_search_bar_spacing, y=-((entryheight)/2) + icon_and_search_bar_spacing )

		self.infobox = cw.infobox(self)
		self.infobox.place(relx=1, x=-infoframewidth, rely=1, y=-87.5, height=87.5, width=infoframewidth)
		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)
		#Back to list button frame, placed first so the details button covers it
		self.repobuttons =cw.navbox(self.infobox,
			primary_button_command = lambda: self.addrepo(), 
			primary_button_text="ADD REPO",
			etc_button_image = self.returnimage,
			etc_button_command = lambda: controller.show_frame("mainPage"),
			left_context_command = None,
			right_context_command = None,
			)
		self.repobuttons.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)

		self.populaterepobox()
		






	def addrepo(self):
		guicore.addrepo(self.urlbox.get_text(),self.descriptionbox.get_text(),self.subfolderbox.get_text(),self.genrebox.get_text())
	

	def populaterepobox(self):
		repolist =  guicore.getrepolist()
		if not repolist == None:
			print("repo data {}".format(repolist))
			for repo in repolist:
				if not repo == "created_with":
					print(repo)
					softwarename = repolist[repo]["software"]
					self.repolistbox.insert(END, softwarename)
