from modules.format import * 
import modules.customwidgets as cw
# import modules.guicore as guicore
# import modules.HBUpdater as HBUpdater
# import modules.webhandler as webhandler

import os
# import tkinter as tk
from tkinter.constants import *

class errorPage(cw.themedframe):
    def __init__(self, parent, controller,back_command):
        self.back_command = back_command
        self.controller = controller
        self.return_frame = "homePage"
        self.yes_command = None

        cw.themedframe.__init__(self,parent,background_color= dark_color)

        self.errortext = cw.themedguidelabel(self,"Welcome to the error page.\n\nIf you are seeing this, there was an error with the error page.\n\nFML",anchor="center",wraplength=500)

        errorframeheight = 2*navbuttonheight
        self.errortext.place(relx=0.5,rely=0.5,x=-250, width=500,height=2*errorframeheight,y=-(errorframeheight))

        self.backbuttonframe = cw.themedframe(self,background_color=dark_color)
        self.backbuttonframe.place(relx=0.5,rely=0.5,y=+(3*navbuttonheight + separatorwidth),width=300,x=-150,height=navbuttonheight)

        self.backbutton = cw.navbutton(self.backbuttonframe, command_name=self.back_command,text_string="RIP. Take me back to the app.")
        self.backbutton.place(relwidth=1,relheight=1)

        self.yesnobuttonframe = cw.themedframe(self,background_color=dark_color)
        self.yesnobuttonframe.place(relx=0.5,rely=0.5,y=+(3*navbuttonheight + separatorwidth),width=300,x=-150,height=navbuttonheight)

        self.yesbutton = cw.navbutton(self.yesnobuttonframe, command_name=self.on_yes,text_string="Yes")
        self.yesbutton.place(relx=0,relwidth=0.33,relheight=1)

        self.nobutton = cw.navbutton(self.yesnobuttonframe, command_name=self.on_no,text_string="No")
        self.nobutton.place(relx=0.67,relwidth=0.33,relheight=1)

        self.backbuttonframe.tkraise()

    def raiseError(self, error_string):
        print("Error has been raised {}".format(error_string))
        self.errortext.set(error_string)
        self.backbuttonframe.tkraise()

    def getanswer(self, return_screen, question, yes_command):
        print("Question raised {}".format(question))
        self.errortext.set(question)
        self.yesnobuttonframe.tkraise()
        self.return_screen = return_screen
        self.yes_command = yes_command

    def on_yes(self):
        self.yes_command()
        self.controller.show_frame(self.return_frame)

    def on_no(self):
        self.controller.show_frame(self.return_frame)

