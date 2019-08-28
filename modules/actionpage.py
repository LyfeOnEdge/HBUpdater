import modules.framework as framework
import modules.customwidgets as cw
from modules.format import * 
from tkinter.constants import *
import modules.guicore as guicore
import os
import tkinter as tk

entryboxheight = 90
entryboxwidth = 500

class actionPage(framework.Frame):
    def __init__(self, parent, controller, page_name, back_command, action = None, entry_text = None, on_key_do = False, title = None):
        framework.Frame.__init__(self,parent,controller)
        self.back_command = back_command
        self.controller = controller
        self.action = action
        self.activestatus = False
        self.on_key_do = on_key_do

        self.title = cw.ThemedLabel(self,None,anchor="center",label_font=hugeboldtext, background = dark_color)
        self.title.place(relx=0.5,rely=.1, x=-0.5*entryboxwidth, y=+0.5*entryboxheight,width=entryboxwidth)
        if title: self.title.set(title)

        self.returnimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder,"returnbutton.png")).zoom(3).subsample(5)
        self.returnbutton = cw.navbutton(self,command_name=self.back,image_object=self.returnimage)
        self.returnbutton.place(relx=1,rely=1,x=-2*navbuttonheight,y=-2*navbuttonheight,width=navbuttonheight,height=navbuttonheight)

        self.entry = cw.entrybox(self, entry_background = light_color, command=self.action, entry_font=mondoboldtext, placeholder=entry_text,justification="center")
        self.entry.place(relx=0.5,rely=.5, x=-0.5*entryboxwidth, y=-0.5*entryboxheight, width=entryboxwidth, height=entryboxheight)
        self.entry.entry.bind("<KeyRelease>", self.on_key)

        self.status = cw.ThemedLabel(self,None,anchor="center",label_font=hugeboldtext, background = dark_color)
        self.status.place(relx=0.5,rely=.5, x=-0.5*entryboxwidth, y=+0.5*entryboxheight,width=entryboxwidth)

    def on_show_frame(self,event):
        self.entry.enable()
        self.activestatus = True

    def on_key(self,event):
        if self.on_key_do:
            self.on_action()

    def on_action(self, event = None):
        if self.activestatus:
            entrytext = self.entry.get()
            result = self.action(entrytext)
            self.status.set(result)

    def back(self):
        self.entry.disable()
        self.activestatus = False
        self.back_command()


        