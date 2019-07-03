from modules.format import * 
import modules.customwidgets as cw
# import modules.guicore as guicore
# import modules.HBUpdater as HBUpdater
# import modules.webhandler as webhandler

import os
# import tkinter as tk
from tkinter.constants import *

class errorPage(cw.ThemedFrame):
    def __init__(self, parent, controller,page_name,back_command):
        self.back_command = back_command
        self.controller = controller
        self.return_frame = "homePage"
        self.yes_command = None

        cw.ThemedFrame.__init__(self,parent,background_color= dark_color)

        self.errortext = cw.ThemedLabel(self,"Welcome to the error page.\n\nIf you are seeing this, there was an error with the error page.\n\nFML",anchor="center",wraplength=500)

        errorframeheight = 2*navbuttonheight
        self.errortext.place(relx=0.5,rely=0.5,x=-250, width=500,height=2*errorframeheight,y=-(errorframeheight))

        self.backbuttonframe = cw.ThemedFrame(self,background_color=dark_color)
        self.backbuttonframe.place(relx=0.5,rely=0.5,y=+(3*navbuttonheight + separatorwidth),width=300,x=-150,height=navbuttonheight)

        self.backbutton = cw.navbutton(self.backbuttonframe, command_name=self.on_back,text_string="RIP. Take me back.",background=light_color)
        self.backbutton.place(relwidth=1,relheight=1)

        self.yesnobuttonframe = cw.ThemedFrame(self,background_color=dark_color)
        self.yesnobuttonframe.place(relx=0.5,rely=0.5,y=+(3*navbuttonheight + separatorwidth),width=300,x=-150,height=navbuttonheight)

        self.yesbutton = cw.navbutton(self.yesnobuttonframe, command_name=self.on_yes,text_string="Yes",background=light_color)
        self.yesbutton.place(relx=0,relwidth=0.33,relheight=1)

        self.nobutton = cw.navbutton(self.yesnobuttonframe, command_name=self.on_no,text_string="No",background=light_color)
        self.nobutton.place(relx=0.67,relwidth=0.33,relheight=1)

        self.backbuttonframe.tkraise()

    def raiseError(self, error_string, return_screen="homePage"):
        print("-------------------------------\nERROR raised - \n{}".format(error_string))
        self.return_frame = return_screen
        self.errortext.set(error_string)
        self.backbuttonframe.tkraise()

    def getanswer(self, return_screen, question, yes_command):
        print("-------------------------------\nQuestion raised - \n{}".format(question))
        self.errortext.set(question)
        self.yesnobuttonframe.tkraise()
        self.return_frame = return_screen
        self.yes_command = yes_command
        self.controller.show_frame("errorPage")

    def on_yes(self):
        print("Got yes\n-------------------------------")
        self.yes_command()
        self.controller.show_frame(self.return_frame)

    def on_no(self):
        print("Got no\n-------------------------------")
        self.controller.show_frame(self.return_frame)

    def on_back(self):
        print("Returning to {}\n-------------------------------".format(self.return_frame))
        self.controller.show_frame(self.return_frame)

