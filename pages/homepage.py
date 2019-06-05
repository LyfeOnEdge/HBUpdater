from modules.format import * 
import modules.customwidgets as cw
# import modules.guicore as guicore
# import modules.HBUpdater as HBUpdater
# import modules.webhandler as webhandler
import modules.locations as locations
import os

import tkinter as tk
from tkinter.constants import *

import pages.installerhelperpage as installerhelperpage
import pages.serialpage as serialpage
import pages.errorpage as errorpage
homebuttonwidth = 120
homebuttonspacing = 5

class homePage(cw.themedframe):
	def buildbuttonrow(self,title,buttonlist,frame):
		iconspacer = homebuttonspacing
		for button in buttonlist:
			if not button == buttonlist[0]:
				iconspacer += homebuttonwidth-2*homebuttonspacing
			buttonobj = cw.iconbutton(frame,button["image"],command_name=button["callback"])
			buttonobj.place(rely=.5, x=iconspacer, y = -((homebuttonwidth)/2) + homebuttonspacing,width = homebuttonwidth-2*homebuttonspacing, height=homebuttonwidth-2*homebuttonspacing)
			button_ttp = cw.tooltip(buttonobj,button["tooltip"])
			buttonlabel = cw.themedguidelabel(frame,button["shorttip"],anchor="center",label_font=smallboldtext)
			buttonlabel.place(rely=0.5, x=iconspacer, y = +(homebuttonwidth-2*homebuttonspacing)/2,width = homebuttonwidth-2*homebuttonspacing)
			iconspacer += 2*homebuttonspacing

		rowlabel = cw.themedguidelabel(frame,title,anchor="w",label_font=largeboldtext)
		rowlabel.place(x=0, y = 0,relwidth=1)
		#Generate a button and link a tooltip for each button in the list

	def __init__(self, parent, controller,back_command):
		self.back_command = back_command
		self.controller = controller

		cw.themedframe.__init__(self,parent,background_color= light_color)
		self.outerframe = cw.themedframe(self)
		self.outerframe.place(relx=0.5,rely=0.5,x=-(790/2),y=-(510/2),width=790,height=510)

		self.settingsimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"settings.png"))
		self.injectimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"injector.png"))
		self.nutimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"nut.png")).zoom(2)
		self.fluffyimage = tk.PhotoImage(file=os.path.join(locations.assetfolder, "fluffy.png"))
		self.pythonimage = tk.PhotoImage(file=os.path.join(locations.assetfolder, "python.png"))
		self.cfwimage = tk.PhotoImage(file=os.path.join(locations.assetfolder, "cfw.png"))
		self.betaimage = tk.PhotoImage(file=os.path.join(locations.assetfolder, "beta.png"))
		self.homebrewimage = tk.PhotoImage(file=os.path.join(locations.assetfolder, "homebrew.png"))
		self.gameimage = tk.PhotoImage(file=os.path.join(locations.assetfolder, "games.png"))

		homebrewbuttonlist = [
			{
			"image" : self.homebrewimage,
			"callback" : lambda: self.controller.show_frame("mainPage"),
			"tooltip" : "Install homebrew apps",
			"shorttip" : "Homebrew Apps"
			},

			{
			"image" : self.gameimage,
			"callback" : lambda: self.controller.show_frame("gamesPage"),
			"tooltip" : "Install homebrew games",
			"shorttip" : "Homebrew Games"
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
			"shorttip" : "Nut Server"
			},

			{
			"image" : self.fluffyimage,
			"callback" : self.checkfluffyandstart,
			"tooltip" : "Open fluffy server",
			"shorttip" : "Fluffy Server"
			},

			{
			"image" : self.betaimage,
			"callback" : self.checkserialandstart,
			"tooltip" : "Built-in Switch serial number checker GUI",
			"shorttip" : "Serial Checker"
			},
		]


		otherbuttonlist = [
			{
			"image" : self.betaimage,
			"callback" : lambda: self.controller.show_frame("errorPage"),
			"tooltip" : "Whatever is in beta",
			"shorttip" : "In beta"
			},


			{
			"image" : self.settingsimage,
			"callback" : lambda: self.controller.show_frame("settingsPage"),
			"tooltip" : "Open settings page",
			"shorttip" : "Settings"
			},
		]


		self.homebrewbox = cw.themedframe(self.outerframe,background_color=light_color)
		self.homebrewbox.place(relx=0,rely=0,relwidth=1,relheight=0.33)
		self.buildbuttonrow("HOMEBREW",homebrewbuttonlist,self.homebrewbox)

		self.toolsbox = cw.themedframe(self.outerframe,background_color=light_color)
		self.toolsbox.place(relx=0,rely=0.33,relwidth=1,relheight=0.33)
		self.buildbuttonrow("SWITCH TOOLS",toolbuttonlist,self.toolsbox)

		separator = cw.darkseparator(self.outerframe)
		separator.place(relx=0,rely=0.32,relwidth=1,height=separatorwidth)

		self.otherbox = cw.themedframe(self.outerframe,background_color=light_color)
		self.otherbox.place(relx=0,rely=0.66,relwidth=1,relheight=0.34)
		self.buildbuttonrow("MORE",otherbuttonlist,self.otherbox)

		separator = cw.darkseparator(self.outerframe)
		separator.place(relx=0,rely=0.65,relwidth=1,height=separatorwidth)

	def checknutandstart(self):
		if not installerhelperpage.checkifhelperdownloaded("nut"):
			installerhelperpage.seterrorstate("nut")
			self.controller.show_frame("installerHelperPage")
			return
		installerhelperpage.starthelper("nut")

	def checkfluffyandstart(self):
		if not installerhelperpage.checkifhelperdownloaded("fluffy"):
			installerhelperpage.seterrorstate("fluffy")
			self.controller.show_frame("installerHelperPage")
			return
		installerhelperpage.starthelper("fluffy")

	def checkserialandstart(self):
		status = serialpage.checkifSSNCinstalled()
		if status == "not installed" or status == None:
			self.controller.show_frame("errorPage")
			self.controller.frames["errorPage"].getanswer("serialPage","Would you like to install Switch Serial Number Checker and its dependencies?",lambda: serialpage.downloadSSNCandinstalldependencies())
		else:
			self.controller.show_frame("serialPage")

