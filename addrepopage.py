import HBUpdater
from format import * 
import homebrewcore
import webhandler

import tkinter as tk
from tkinter.constants import *
import customwidgets as cw

import json
import sys,subprocess


# #ijdict
# fuseefolder = homebrewcore.getpath("fusee-launcher")

class addRepoScreen(cw.themedframe):
	def __init__(self, parent, controller,back_command):
		cw.themedframe.__init__(self,parent,frame_borderwidth=0,frame_highlightthickness= 0,background_color= light_color)
		self.repoframe = cw.themedframe(self,frame_borderwidth=0,frame_highlightthickness= 0,background_color= light_color)
		self.repoframe.place(x=0,y=0,relwidth=1, width=-infoframewidth, relheight=1,)

		self.searchbox_frame = cw.themedframe(self.repoframe,frame_borderwidth=0,frame_highlightthickness= 0,background_color=light_color,)
		self.searchbox_frame.place(relx=0.0, rely=1,height=searchboxheight, relwidth=1,y=-2*searchboxheight)

		self.iconspacer = 0

		self.addrepoimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"plus.png"))
		self.addrepoimage = self.addrepoimage.zoom((3)).subsample(5)
		self.iconspacer += searchboxheight-2*icon_and_search_bar_spacing
		self.addbutton = cw.navbutton(self.searchbox_frame,image_object=self.addrepoimage,command_name=lambda: addrepo(self))
		self.addbutton.place(relx= 1, x=-self.iconspacer, rely=.5, y = -((searchboxheight)/2) + icon_and_search_bar_spacing,width =searchboxheight-2*icon_and_search_bar_spacing, height=searchboxheight-icon_and_search_bar_spacing)

		self.iconspacer += icon_and_search_bar_spacing*2

		self.searchbox = cw.SearchBox(self.searchbox_frame, 
			command=lambda: addrepo(self), 
			placeholder="Add repo in format 'https://github.com/author/repo'",
			)

		self.searchbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=searchboxheight-icon_and_search_bar_spacing, y=-((searchboxheight)/2) + icon_and_search_bar_spacing )



		self.descriptionbox_frame = cw.themedframe(self.repoframe,frame_borderwidth=0,frame_highlightthickness= 0,background_color=light_color,)
		self.descriptionbox_frame.place(relx=0.0, rely=1,height=searchboxheight, relwidth=1,y=-searchboxheight)

		self.iconspacer = 0

		self.descriptionbox = cw.SearchBox(self.descriptionbox_frame, 
			command=lambda: addrepo(self), 
			placeholder="(Optional) Repo Description",
			)

		self.descriptionbox.place(relx=0,rely=.5, x=+icon_and_search_bar_spacing, relwidth=1, width=-(self.iconspacer), height=searchboxheight-2*icon_and_search_bar_spacing, y=-((searchboxheight)/2) + icon_and_search_bar_spacing )








		self.repolistboxframe = cw.titledlistboxframe(self.repoframe,"Repo")
		self.repolistboxframe.place(relx=0,rely=0,relwidth=1,relheight=1,height=-2*searchboxheight, width=-validcolumnwidth)
		self.repolistboxseparator = cw.separator(self.repolistboxframe)
		self.repolistboxseparator.place(relx=0,rely=0,y=columtitlesheight,height=reposeparatorwidth,relwidth=1,)
		self.repolistbox = cw.customlistbox(self.repolistboxframe)
		self.repolistbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset, y=columtitlesheight+reposeparatorwidth,height=-(columtitlesheight+injector_separator_width))

		self.separatorA = cw.separator(self.repolistboxframe)
		self.separatorA.place(relx=0,rely=0,width=reposeparatorwidth,relheight=1,)

		self.validlistboxframe = cw.titledlistboxframe(self.repoframe,"Valid")
		self.validlistboxframe.place(relx=1,x=-validcolumnwidth+reposeparatorwidth,rely=0,relheight=1,height=-2*searchboxheight, width=validcolumnwidth)
		self.validlistboxseparator = cw.separator(self.validlistboxframe)
		self.validlistboxseparator.place(relx=0,rely=0,y=columtitlesheight,height=reposeparatorwidth,relwidth=1,)
		self.validlistbox = cw.customlistbox(self.repolistboxframe)
		self.validlistbox.place(relheight=1,relwidth=1, x=+lbcolumnoffset, width=-lbcolumnoffset, y=columtitlesheight+reposeparatorwidth,height=-(columtitlesheight+injector_separator_width))


		self.infobox = cw.infobox(self)
		self.infobox.place(relx=1, x=-infoframewidth, rely=1, y=-87.5, height=87.5, width=infoframewidth)

		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)

		#Back to list button frame, placed first so the details button covers it
		self.repobuttons =cw.navbox(self.infobox,
			primary_button_command = None, 
			etc_button_image = self.returnimage,
			etc_button_command = lambda: controller.show_frame("mainPage"),
			left_context_command = None,
			right_context_command = None,
			)
		self.repobuttons.place(relx=.5, rely=1, x=-100, y=-87.5, height= 87.5, width=200)


		def addrepo(self):
			HBUpdater.addrepo(self.sb.get_text())
		
