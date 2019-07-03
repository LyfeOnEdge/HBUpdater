from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import modules.webhandler as webhandler

import os

import tkinter as tk
from tkinter.constants import *

developers = {
	"LyfeOnEdge" : {
		"project_page_url" : "https://discord.gg/cXtmY9M",
		"dev_flavor_text" : "In Soviet Russia, switch hack you.\nColorblind.\n←Join my discord for dragons"
	},

	"pprmint" : {
		"gravatar_url" : "http://de.gravatar.com/npprmint.json",
		"project_page_url" : "npprmint.github.io",
		"dev_flavor_text" : "UI concept and asset designer.\n\n←Click here to visit his website"
	}
}

thankyoutext = """vgmoose, crc32, pwsincd on the 4TU Discord server for cooperating with me so I could make my app compatible with the HB appstore.

Contributors / testers:
    pprmint - Original UI concept and asset designer, tester, Find out more about him at npprmint.github.io
    Kabiigon - MacOS testing, Gui tweaks, tried to make my app look like team-x wrote it. 
    IAMTHELAW - Testing, ideas
    Guts - Testing, ideas
    ELY_M - Testing, ideas
    Goffrier - Icon ideas

Jian Addelle - Comic Relief
loli hunter-san - uwu ~ owo 
Crusatyr - (ReiSwitched) Answered questions about ReiNX installs
Friedkeenan - Answered code questions about detecting the switch in rcm for auto-injection with fusee

Software credits:
fusee-launcher, Ktempkin and Qyraid GPL2 https://github.com/Qyriad/fusee-launcher
NUT, blawar GPL3 https://github.com/blawar/nut.
Fluffy, fourminute GPL3 https://github.com/fourminute/Fluffy
ssncpy, Anthony Da Mota GPL3 https://github.com/AkdM/ssncpy
"""

class aboutPage(tk.Frame):
	def __init__(self, parent, controller,page_name,back_command):
		self.back_command = back_command
		self.controller = controller

		width = guicore.checkguisetting("dimensions","guiwidth")
		height = guicore.checkguisetting("dimensions","guiheight")

		cw.ThemedFrame.__init__(self,parent,background_color= light_color)
		self.outer_frame = cw.ThemedFrame(self,background_color=light_color)
		self.outer_frame.place(relx=0.5,rely=0.5,x=-(width/2),y=-(height/2),width=width,height=height)
		

		#Credits and stuff 
		self.devlabel = cw.ThemedLabel(self.outer_frame, "DEVELOPERS", label_font = columnlabelfont, background = light_color, foreground = columnlabelcolor, anchor="center")
		self.devlabel.place(y=+separatorwidth,x=(2*separatorwidth+0.5*navbuttonheight),relwidth=1,width=-2*(2*separatorwidth+0.5*navbuttonheight))

		self.devframe = cw.ThemedFrame(self.outer_frame, background_color=light_color)
		self.devframe.place(y=+4*separatorwidth+0.5*navbuttonheight,x=separatorwidth,relwidth=1,width=-2*separatorwidth,height=3*navbuttonheight)

		self.lyfeframe = cw.ThemedFrame(self.devframe, background_color=light_color)
		self.lyfeframe.place(relx=0,rely=0,relwidth=0.5,relheight=1)

		self.mintframe = cw.ThemedFrame(self.devframe, background_color=light_color)
		self.mintframe.place(relx=0.5,rely=0,relwidth=0.5,relheight=1)


		lyfeimage = webhandler.getcachedimage("lyfeonedge")
		if not lyfeimage:
			lyfeimage = webhandler.grabgravatar("lyfeonedge")
			if not lyfeimage:
				lyfeimage = os.path.join(locations.assetfolder,notfoundimage)

		#I get an object named after me :D
		self.lyfeonedgeimage = tk.PhotoImage(file=lyfeimage)
		self.lyfeonedge = cw.devbox(self.lyfeframe,"LyfeOnEdge",developers["LyfeOnEdge"]["dev_flavor_text"],self.lyfeonedgeimage,command_name=lambda: webhandler.opentab(developers["LyfeOnEdge"]["project_page_url"]))
		self.lyfeonedge.place(relx=0.125, relheight=1,relwidth=0.875)


		pprmntimage = webhandler.getcachedimage("npprmint")
		if not pprmntimage:
			pprmntimage = webhandler.grabgravatar(locations.developers["pprmint"]["gravatar_url"])
			if pprmntimage == None:
				pprmntimage = os.path.join(locations.assetfolder,notfoundimage)

		self.pprmintimage = tk.PhotoImage(file=pprmntimage)
		self.pprmint = cw.devbox(self.mintframe,"pprmint",developers["pprmint"]["dev_flavor_text"],self.pprmintimage,command_name=lambda: webbrowser.open_new_tab(locations.developers["pprmint"]["project_page_url"]))
		self.pprmint.place(relx=0.125, relheight=1,relwidth=0.875)


		self.creditsseparator = cw.Separator(self.outer_frame,color=dark_color)
		self.creditsseparator.place(y=+1*separatorwidth+3*navbuttonheight,x=+separatorwidth,relwidth=1,width=-2*separatorwidth,height=separatorwidth)

		self.thankslabel = cw.ThemedLabel(self.outer_frame,"SPECIAL THANKS", label_font = columnlabelfont, background = light_color, foreground = columnlabelcolor,anchor="center")
		self.thankslabel.place(y=+2*separatorwidth+3*navbuttonheight,x=(2*separatorwidth+0.5*navbuttonheight),relwidth=1,width=-2*(2*separatorwidth+0.5*navbuttonheight),height=navbuttonheight)

		self.thankstext = cw.ScrolledText(self.outer_frame,background=light_color,borderwidth=0,highlightthickness=0,foreground=lgray,font=smallboldtext,wrap="word")
		self.thankstext.place(y=+0*separatorwidth+4*navbuttonheight,x=separatorwidth,relwidth=1,width=-(2*separatorwidth),relheight=1,height=-(+0*separatorwidth+4*navbuttonheight))
		self.thankstext.insert(END, thankyoutext)
		self.thankstext.config(state=DISABLED)

		#back to main page image and button
		self.returnimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)

		self.return_button = cw.navbutton(self.outer_frame, image_object=self.returnimage, command_name=back_command)
		self.return_button.place(relx=1, rely=1, x=-(separatorwidth+navbuttonheight), y=-(separatorwidth+navbuttonheight), height=navbuttonheight, width=navbuttonheight)

