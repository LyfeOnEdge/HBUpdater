from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.homebrewcore as homebrewcore
import modules.locations as locations
import modules.webhandler as webhandler


import tkinter as tk
from tkinter.constants import *


thankyoutext = """Ktempkin and Qyraid, for writing and maintaining fusee-launcher.py, and making it available via the github api upon my request.

Credits:
NUT, blawar GPL3 https://github.com/blawar/nut.
Fluffy, fourminute GPL3 https://github.com/fourminute/Fluffy

HBG Discord, /r/SwitchPirates, and the members of GBAtemp for their ideas, critiques, and testing.
"""

class settingsPage(tk.Frame):
	def __init__(self, parent, controller,back_command):
		tk.Frame.__init__(self,parent)

		#Full window frame, holds everything
		self.outer_frame = cw.themedframe(self,background_color = light_color)
		self.outer_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

		#back to main page button
		self.returnimage = tk.PhotoImage(file=homebrewcore.joinpaths(homebrewcore.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)
		
		self.settingsframe = cw.themedframe(self.outer_frame,background_color=light_color,frame_highlightthickness=0,frame_borderwidth=0)
		self.settingsframe.place(relwidth=1,relheight=1,width=-1.5*infoframewidth)

		self.settingboxlist = []

		spaceincrementer = 0.2
		self.settingslabel = cw.columnlabel(self.settingsframe,"SETTINGS",anchor="center",background=light_color)
		self.settingslabel.place(relx=0.5,width=5*navbuttonheight,x=-2.5*navbuttonheight,y=spaceincrementer*navbuttonheight)

		self.autoupdaterepossettingbox = cw.settingbox(self.settingsframe,"Automatically update repo information on launch")
		self.settingboxlist.append(self.autoupdaterepossettingbox)

		spaceincrementer+=1.2

		for settingbox in reversed(self.settingboxlist):
			settingbox.place(x=+0.5*navbuttonheight,y=spaceincrementer*navbuttonheight,relwidth=1,width=-navbuttonheight,height=navbuttonheight-separatorwidth)
			if not settingbox == self.settingboxlist[0]:
				spacer = cw.darkseparator(self.settingsframe)
				spacer.place(x=+0.5*navbuttonheight,y=spaceincrementer*navbuttonheight+navbuttonheight,relwidth=1,width=-navbuttonheight,height=0.5*separatorwidth)
			spaceincrementer+=1.2

		self.savebutton = cw.navbutton(self.settingsframe,text_string="SAVE",command_name=self.save)
		self.savebutton.place(relx=0.5,width=3*navbuttonheight,x=-1.5*navbuttonheight,y=spaceincrementer*navbuttonheight)

		spacer = cw.darkseparator(self.settingsframe)
		spacer.place(x=+0.5*navbuttonheight,y=spaceincrementer*navbuttonheight+navbuttonheight,relwidth=1,width=-navbuttonheight,height=separatorwidth)

		spaceincrementer+=1.2


		self.additionaltools = cw.columnlabel(self.settingsframe,"MORE TOOLS\n(mouse over for details)",anchor="center",background=light_color)
		self.additionaltools.place(relx=0.5,width=5*navbuttonheight,x=-2.5*navbuttonheight,y=spaceincrementer*navbuttonheight)

		spaceincrementer+=1.8

		self.additionalsettingboxlist = []

		self.installpil = cw.navbutton(self.settingsframe,command_name=self.installpilmodule,text_string="INSTALL PILLOW")
		self.pilttp = cw.tooltip(self.installpil,"""Install pillow module, this will use a different (better) 
image scaling method to display repo author images. 
You can also install pip manually and it will be 
automatically detected on launch.""")
		self.additionalsettingboxlist.append(self.installpil)

		for settingbox in reversed(self.additionalsettingboxlist):
			settingbox.place(x=+0.5*navbuttonheight,y=spaceincrementer*navbuttonheight,width=5*navbuttonheight,height=navbuttonheight-separatorwidth)
			spaceincrementer+=1.2



		self.creditsframe = cw.themedframe(self.outer_frame,frame_highlightthickness=0,frame_borderwidth=0)
		self.creditsframe.place(relx=1,y=0,relheight=1,x=-1.5*infoframewidth,width=1.5*infoframewidth)

		#Credits and stuff
		self.devlabel = cw.columnlabel(self.creditsframe,"DEVELOPERS",anchor="center")
		self.devlabel.place(y=+separatorwidth,x=(2*separatorwidth+0.5*navbuttonheight),relwidth=1,width=-2*(2*separatorwidth+0.5*navbuttonheight))

		lyfeimage = webhandler.getcachedimage("lyfeonedge")
		if not lyfeimage:
			lyfeimage = webhandler.grabgravatar(locations.developers["LyfeOnEdge"]["gravatar_url"])
			if lyfeimage == None:
				lyfeimage = homebrewcore.joinpaths(homebrewcore.assetfolder,notfoundimage)

		#I get an object named after me :D
		self.lyfeonedgeimage = tk.PhotoImage(file=lyfeimage)
		self.lyfeonedge = cw.devbox(self.creditsframe,"LyfeOnEdge",locations.developers["LyfeOnEdge"]["dev_flavor_text"],self.lyfeonedgeimage,command_name=lambda: webbrowser.open_new_tab(locations.developers["LyfeOnEdge"]["project_page_url"]))
		self.lyfeonedge.place(y=+2*separatorwidth+0.5*navbuttonheight,x=separatorwidth,relwidth=1,width=-2*separatorwidth,height=3*navbuttonheight)

		pprmntimage = webhandler.getcachedimage("npprmint")
		if not pprmntimage:
			pprmntimage = webhandler.grabgravatar(locations.developers["pprmint"]["gravatar_url"])
			if pprmntimage == None:
				pprmntimage = homebrewcore.joinpaths(homebrewcore.assetfolder,notfoundimage)

		self.pprmintimage = tk.PhotoImage(file=pprmntimage)
		self.pprmint = cw.devbox(self.creditsframe,"pprmint",locations.developers["pprmint"]["dev_flavor_text"],self.pprmintimage,command_name=lambda: webbrowser.open_new_tab(locations.developers["pprmint"]["project_page_url"]))
		self.pprmint.place(y=+3*navbuttonheight+separatorwidth,x=separatorwidth,relwidth=1,width=-2*separatorwidth,height=3*navbuttonheight)


		self.creditsseparator = cw.separator(self.creditsframe)
		self.creditsseparator.place(y=+(infoframewidth+3*separatorwidth),x=+separatorwidth,relwidth=1,width=-2*separatorwidth,height=separatorwidth)

		# self.prevbutton = cw.navbutton(self.creditsframe, command_name=self.prevcredit, text_string="<")
		# self.prevbutton.place(y=+(infoframewidth+separatorwidth),x=+separatorwidth,width=0.5*navbuttonheight,height=navbuttonheight)

		# self.nextbutton = cw.navbutton(self.creditsframe, command_name=self.nextcredit, text_string=">")
		# self.nextbutton.place(y=+(infoframewidth+separatorwidth),relx=1,x=-(separatorwidth+0.5*navbuttonheight),width=0.5*navbuttonheight,height=navbuttonheight)

		self.thankslabel = cw.columnlabel(self.creditsframe,"SPECIAL THANKS",anchor="center")
		self.thankslabel.place(y=+(infoframewidth+4*separatorwidth),x=(2*separatorwidth+0.5*navbuttonheight),relwidth=1,width=-2*(2*separatorwidth+0.5*navbuttonheight),height=navbuttonheight)

		self.thankstext = cw.ScrolledText(self.creditsframe,background=dark_color,borderwidth=0,highlightthickness=0,foreground=lgray,font=smallboldtext,wrap="word")
		self.thankstext.place(y=+(infoframewidth+5*separatorwidth+navbuttonheight),x=separatorwidth,relwidth=1,width=-(2*separatorwidth),relheight=1,height=-(infoframewidth+3*separatorwidth+navbuttonheight))
		self.thankstext.insert(END, thankyoutext)

		self.backtomain_button = cw.navbutton(self.settingsframe, image_object=self.returnimage, command_name=lambda: controller.show_frame("mainPage"))
		self.backtomain_button.place(relx=1, rely=1, x=-(separatorwidth+navbuttonheight), y=-(separatorwidth+navbuttonheight), height=navbuttonheight, width=navbuttonheight)

		self.updatesettingsstate()

	def updatesettingsstate(self):
		autoupdate = guicore.checkguisetting("guisettings","automatically_check_for_updates")
		self.autoupdaterepossettingbox.set(autoupdate)

	def save(self):
		newentry = {
					"guisettings" : {
						"automatically_check_for_updates" : self.autoupdaterepossettingbox.get(),
					}
				}
		guicore.setguisetting(newentry)

	def installpilmodule(self):
		webhandler.installpipmodule("pillow")