from modules.format import * 
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import modules.webhandler as webhandler

import os

import tkinter as tk
from tkinter.constants import *


class settingsPage(tk.Frame):
	def __init__(self, parent, controller,page_name,back_command):
		self.back_command = back_command
		self.controller = controller

		width = guicore.checkguisetting("dimensions","guiwidth")
		height = guicore.checkguisetting("dimensions","guiheight")

		cw.ThemedFrame.__init__(self,parent,background_color= light_color)
		self.outer_frame = cw.ThemedFrame(self, background_color = light_color)
		self.outer_frame.place(relx=0.5,rely=0.5,x=-(width/2),y=-(height/2),width=width,height=height)

		#back to main page button image
		self.returnimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"returnbutton.png"))
		self.returnimage = self.returnimage.zoom((3)).subsample(5)
		
		self.settingframe = cw.ThemedFrame(self.outer_frame,background_color=light_color,frame_highlightthickness=0,frame_borderwidth=0)
		self.settingframe.place(relwidth=1,relheight=1,width=-1.5*infoframewidth)


		self.modulesframe = cw.ThemedFrame(self.outer_frame,background_color=dark_color,frame_highlightthickness=0,frame_borderwidth=0)
		self.modulesframe.place(relheight=1,relx=1, width=1.5*infoframewidth, x=-1.5*infoframewidth)
# 		self.settingboxlist = []

# 		spaceincrementer = 0.2
# 		self.settingslabel = cw.columnlabel(self.settingsframe,"SETTINGS",anchor="center",background=light_color)
# 		self.settingslabel.place(relx=0.5,width=5*navbuttonheight,x=-2.5*navbuttonheight,y=spaceincrementer*navbuttonheight)

# 		self.autoupdaterepossettingbox = cw.settingbox(self.settingsframe,"Automatically update repo information on launch\n(disable leads to faster launch time and less bandwidth)")
# 		self.settingboxlist.append(self.autoupdaterepossettingbox)

# 		self.alerttoupdatebox = cw.settingbox(self.settingsframe,"Check for updates to HBUpdater")
# 		self.settingboxlist.append(self.alerttoupdatebox)

# 		spaceincrementer+=1.2

# 		for settingbox in reversed(self.settingboxlist):
# 			settingbox.place(x=+0.5*navbuttonheight,y=spaceincrementer*navbuttonheight,relwidth=1,width=-navbuttonheight,height=navbuttonheight-separatorwidth)
# 			if not settingbox == self.settingboxlist[0]:
# 				spacer = cw.Separator(self.settingsframe,color=dark_color)
# 				spacer.place(x=+0.5*navbuttonheight,y=spaceincrementer*navbuttonheight+navbuttonheight,relwidth=1,width=-navbuttonheight,height=0.5*separatorwidth)
# 			spaceincrementer+=1.2

# 		self.savebutton = cw.navbutton(self.settingsframe,text_string="SAVE",command_name=self.save)
# 		self.savebutton.place(relx=0.5,width=3*navbuttonheight,x=-1.5*navbuttonheight,y=spaceincrementer*navbuttonheight)

# 		spacer = cw.Separator(self.settingsframe,color=dark_color)
# 		spacer.place(x=+0.5*navbuttonheight,y=spaceincrementer*navbuttonheight+navbuttonheight,relwidth=1,width=-navbuttonheight,height=separatorwidth)

# 		spaceincrementer+=1.2


# 		self.additionaltools = cw.columnlabel(self.settingsframe,"MORE TOOLS\n(mouse over for details)",anchor="center",background=light_color)
# 		self.additionaltools.place(relx=0.5,width=5*navbuttonheight,x=-2.5*navbuttonheight,y=spaceincrementer*navbuttonheight)

# 		spaceincrementer+=1.8

# 		self.additionalsettingboxlist = []

		self.installpil = cw.navbutton(self.modulesframe,command_name=self.installpilmodule,text_string="INSTALL PILLOW",background=light_color)
		self.installpil.place(relx=0.5,width=4*navbuttonheight, x=-2*navbuttonheight, rely=0,y=2*(navbuttonheight+separatorwidth),height=navbuttonheight)
		self.pilttp = cw.tooltip(self.installpil,"""Install pillow module, this will use a different (better) 
image scaling method to display repo author images. 
You can also pip-install it manually and it will be 
automatically detected on launch.""")

		self.backtomain_button = cw.navbutton(self.modulesframe, image_object=self.returnimage, command_name=back_command)
		self.backtomain_button.place(relx=1, rely=1, x=-(separatorwidth+navbuttonheight), y=-(separatorwidth+navbuttonheight), height=navbuttonheight, width=navbuttonheight)

		self.save_button = cw.navbutton(self.settingframe, text_string="SAVE", command_name=self.save)
		self.save_button.place(relx=0.5, x=-navbuttonheight, rely=1, y=-(separatorwidth+navbuttonheight), height=navbuttonheight, width=2*navbuttonheight)


		settinglist = [
		{
		"value" : "automatically_check_for_repo_updates", 
		"text" : "Automatically check for repo updates",
		},
		# {
		# "value" : "display_author_image",
		# "text" : "Display author image in software pages"
		# },
		
		]

		v_increment = 60
		v_spacer = v_increment
		self.settings_box_list = []

		for setting in settinglist:
			settingbox = cw.settingbox(self.settingframe, setting["value"], "- {}".format(setting["text"]),)
			settingbox.place(x=+15,y=v_spacer,relwidth = 1, width = -15, height=navbuttonheight)
			self.settings_box_list.append(settingbox)
			v_spacer += v_increment

		for settingbox in self.settings_box_list:
			settingbox.set(guicore.checkguisetting("guisettings", settingbox.v))


	# self.updatesettingsstate()

	# def updatesettingsstate(self):


	def save(self):
		settings = {}
		for settingbox in self.settings_box_list:
			settings = dict(settings, **settingbox.get_setting())

		guicore.setguisetting({"guisettings" : settings})

	def installpilmodule(self):
		webhandler.installpipmodule("pillow")