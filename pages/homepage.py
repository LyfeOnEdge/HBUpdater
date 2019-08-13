from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
# import modules.HBUpdater as HBUpdater
import modules.webhandler as webhandler
import modules.locations as locations
import modules.style as style
import os

import tkinter as tk
from tkinter.constants import *

import modules.toolhelper as toolhelper
import pages.serialpage as serialpage
# import pages.errorpage as errorpage
homebuttonwidth = 144
homebuttonspacing = 5


home_page_button_text_highlight_color = "black"

class homePage(cw.ThemedFrame):
	def buildbuttonrow(self,title,buttonlist,frame):
		global home_page_button_text_highlight_color

		iconspacer = homebuttonspacing
		for button in buttonlist:
			if not button == buttonlist[0]:
				iconspacer += homebuttonwidth-2*homebuttonspacing

			buttonframe = cw.ThemedFrame(frame,background_color=style.homepage_button_background_color)
			buttonframe.place(rely=.5, x=iconspacer, y = -((homebuttonwidth)/2) + 4*homebuttonspacing,width = homebuttonwidth-2*homebuttonspacing, height=homebuttonwidth-2*homebuttonspacing)
			buttonobj = cw.navbutton(buttonframe,image_object=button["image"],command_name=button["callback"],background = style.homepage_button_background_color)
			buttonobj.place(relwidth=1,relheight=1)
			button_ttp = cw.tooltip(buttonobj,button["tooltip"])
			buttonlabel = cw.ThemedLabel(buttonframe,button["shorttip"],anchor="center",label_font=smallboldtext,foreground=style.homepage_button_text_color,background=home_page_button_text_highlight_color)
			buttonlabel.place(rely=1, relx=0.5, x=-0.5*homebuttonwidth, width=homebuttonwidth, y = -20,height=20) #width = homebuttonwidth-2*homebuttonspacing
			iconspacer += 2*homebuttonspacing

		rowlabel = cw.ThemedLabel(frame,title,anchor="w",label_font=largeboldtext,foreground=style.homepage_category_separator_title_color,background=style.homepage_category_separator_color)
		rowlabel.place(x=0, y = 0,relwidth=1)
		#Generate a button and link a tooltip for each button in the list

	def __init__(self, parent, controller,page_name,back_command):

		global home_page_separator_color

		self.back_command = back_command
		self.controller = controller

		width = guicore.checkguisetting("dimensions","guiwidth")
		height = guicore.checkguisetting("dimensions","guiheight")

		cw.ThemedFrame.__init__(self,parent,background_color= style.homepage_background_color)
		self.outerframe = cw.ThemedFrame(self, background_color = style.homepage_background_color)
		self.outerframe.place(relx=0.5,rely=0.5,x=-(width/2),y=-(height/2),width=width,height=height)

		self.settingsimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder,"settings.png"))
		self.injectimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder,"injector.png"))
		self.nutimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder,"nut.png"))
		self.fluffyimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "fluffy.png"))
		self.pythonimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "python.png"))
		self.cfwimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "cfw.png"))
		self.betaimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "beta.png"))
		self.homebrewimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "homebrew.png"))
		self.gameimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "games.png"))
		self.githubimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "github.png"))
		# self.appstoreimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "hbappstore.png"))
		self.serialimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "serialchecker.png"))
		self.emuimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "emu.png"))
		# self.experimentalimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "experimental.png"))
		self.profileimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "profile.png"))
		self.backupsimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "backups.png"))

		homebrewbuttonlist = [
			{
			"image" : self.homebrewimage,
			"callback" : lambda: self.controller.show_frame("homebrewPage"),
			"tooltip" : "Install homebrew apps",
			"shorttip" : "Homebrew"
			},
			{
			"image" : self.gameimage,
			"callback" : lambda: self.controller.show_frame("gamesPage"),
			"tooltip" : "Install homebrew games",
			"shorttip" : "Games"
			},
			{
			"image" : self.emuimage,
			"callback" : lambda: self.controller.show_frame("emuPage"),
			"tooltip" : "Emulators",
			"shorttip" : "Emulators"
			},
			{
			"image" : self.cfwimage,
			"callback" : lambda: self.controller.show_frame("cfwPage"),
			"tooltip" : "Custom Firmware Manager",
			"shorttip" : "CFW Manager"
			},
			{
			"image" : self.pythonimage,
			"callback" : lambda: self.controller.show_frame("pynxPage"),
			"tooltip" : "Homebrew python script for use with NX Python",
			"shorttip" : "Python Scripts"
			},
		]


		toolbuttonlist = [
			{
			"image" : self.injectimage,
			"callback" : lambda: self.controller.show_frame("injectorScreen"),
			"tooltip" : "Built-in RCM injector GUI",
			"shorttip" : "RCM Injector"
			},
			{
			"image" : self.nutimage,
			"callback" : self.checknutandstart,
			"tooltip" : "Open NUT server",
			"shorttip" : "NUT Client"
			},
			{
			"image" : self.fluffyimage,
			"callback" : self.checkfluffyandstart,
			"tooltip" : "Open fluffy",
			"shorttip" : "Fluffy"
			},
			{
			"image" : self.backupsimage,
			"callback" : lambda: self.controller.show_frame("backupPage"),
			"tooltip" : "Beta SD card backup manager",
			"shorttip" : "SD Backup"
			},		
			{
			"image" : self.serialimage,
			"callback" : lambda: self.controller.show_frame("serialPage"),
			"tooltip" : "Built-in Switch serial number checker GUI",
			"shorttip" : "Serial Checker"
			},
		]


		otherbuttonlist = [
			{
			"image" : self.settingsimage,
			"callback" : lambda: self.controller.show_frame("settingsPage"),
			"tooltip" : "Open settings page",
			"shorttip" : "Settings"
			},
			{
			"image" : self.profileimage,
			"callback" : lambda: self.controller.show_frame("aboutPage"),
			"tooltip" : "Open about page",
			"shorttip" : "About"
			},
			{
			"image" : self.githubimage,
			"callback" : lambda: webhandler.opentab("https://www.github.com/LyfeOnEdge/HBUpdater"),
			"tooltip" : "Open HBUpdater Github",
			"shorttip" : "HBU Github"
			},
			# {
			# "image" : self.betaimage,
			# "callback" : lambda: self.controller.show_frame("addrepoPage"),
			# "tooltip" : "delete me",
			# "shorttip" : "repo pages"
			# },
			# {
			# "image" : self.betaimage,
			# "callback" : lambda: self.controller.show_frame("dbPage"),
			# "tooltip" : "delete me",
			# "shorttip" : "titledb"
			# },
			# {
			# "image" : self.betaimage,
			# "callback" : lambda: self.controller.show_frame("usbPage"),
			# "tooltip" : "delete me",
			# "shorttip" : "nutpage"
			# },
		]


		self.homebrewbox = cw.ThemedFrame(self.outerframe,background_color=style.homepage_background_color)
		self.homebrewbox.place(relx=0,rely=0,relwidth=1,relheight=0.33)
		self.buildbuttonrow("HOMEBREW",homebrewbuttonlist,self.homebrewbox)

		self.toolsbox = cw.ThemedFrame(self.outerframe,background_color=style.homepage_background_color)
		self.toolsbox.place(relx=0,rely=0.33,relwidth=1,relheight=0.33)
		self.buildbuttonrow("SWITCH TOOLS",toolbuttonlist,self.toolsbox)

		self.otherbox = cw.ThemedFrame(self.outerframe,background_color=style.homepage_background_color)
		self.otherbox.place(relx=0,rely=0.66,relwidth=1,relheight=0.33)
		self.buildbuttonrow("MORE",otherbuttonlist,self.otherbox)

	def checknutandstart(self):
		if not toolhelper.checkifhelperdownloaded("nut"):
			self.controller.frames["errorPage"].getanswer("homePage","It looks like you don't have nut installed yet,\nwould you like to install it and its dependencies?\nThis can take up to a minute",toolhelper.getnut)
			return
		else:
			toolhelper.starthelper("nut")


	def checkfluffyandstart(self):
		if not toolhelper.checkifhelperdownloaded("fluffy"):
			self.controller.frames["errorPage"].getanswer("homePage","It looks like you don't have fluffy installed yet,\nwould you like to install it and its dependencies?\nThis can take up to a minute",toolhelper.getfluffy)
			return
		else:
			toolhelper.starthelper("fluffy")