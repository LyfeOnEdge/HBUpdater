import HBUpdater
from format import * 
import homebrewcore
import webhandler
import locations
import webbrowser


import tkinter as tk
from tkinter.constants import *
import customwidgets as cw

thankyoutext = """Ktempkin and Qyraid, for writing and maintaining fusee-launcher.py, and making it available via the github api upon my request.

Blarwar (Vertigo) for for writing and maintaining nut, you can find more of his software at https://github.com/blawar.

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

		self.creditsframe = cw.themedframe(self.outer_frame,frame_highlightthickness=0,frame_borderwidth=0)
		self.creditsframe.place(relx=1,y=0,relheight=1,x=-1.5*infoframewidth,width=1.5*infoframewidth)

		self.devlabel = cw.columnlabel(self.creditsframe,"DEVELOPERS",anchor="center")
		self.devlabel.place(y=+separatorwidth,x=(2*separatorwidth+0.5*navbuttonheight),relwidth=1,width=-2*(2*separatorwidth+0.5*navbuttonheight))

		#I get an object named after me :D
		self.lyfeonedgeimage = tk.PhotoImage(file=webhandler.grabgravatar(locations.developers["LyfeOnEdge"]["gravatar_url"]))
		self.lyfeonedge = cw.devbox(self.creditsframe,"LyfeOnEdge",locations.developers["LyfeOnEdge"]["dev_flavor_text"],self.lyfeonedgeimage,command_name=lambda: webbrowser.open_new_tab(locations.developers["LyfeOnEdge"]["project_page_url"]))
		self.lyfeonedge.place(y=+2*separatorwidth+0.5*navbuttonheight,x=separatorwidth,relwidth=1,width=-2*separatorwidth,height=3*navbuttonheight)

		# try:
		self.pprmintimage = tk.PhotoImage(file=webhandler.grabgravatar(locations.developers["pprmint"]["gravatar_url"]))
		self.pprmint = cw.devbox(self.creditsframe,"pprmint",locations.developers["pprmint"]["dev_flavor_text"],self.pprmintimage,command_name=lambda: webbrowser.open_new_tab(locations.developers["pprmint"]["project_page_url"]))
		self.pprmint.place(y=+3*navbuttonheight+separatorwidth,x=separatorwidth,relwidth=1,width=-2*separatorwidth,height=3*navbuttonheight)
		# except:
		# 	self.pprmint = tk.PhotoImage(file=webhandler.grabgravatar(locations.gravatars["pprmint"]))



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

		self.backtomain_button = cw.navbutton(self.outer_frame, image_object=self.returnimage, command_name=lambda: controller.show_frame("mainPage"))
		self.backtomain_button.place(relx=1, rely=1, x=-(separatorwidth+navbuttonheight), y=-(separatorwidth+navbuttonheight), height=navbuttonheight, width=navbuttonheight)

		

	def prevcredit(self):
		print("dunnit")

	def nextcredit(self):
		print("ndunnit")