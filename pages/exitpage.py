import os, sys
import tkinter as tk
from tkinter.constants import *
from widgets import ThemedLabel, button
import style

class exitPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,background=style.color_1)
        self.exit_callback = controller.async_threader.exit

        self.usertext = ThemedLabel(self, label_text="Exit?", label_font = style.hugeboldtext, anchor = "center", background = style.color_1, foreground = style.w)
        self.usertext.place(relwidth = 1, relheight = 1, height = - (style.buttonsize + 2 * style.offset))

        self.yesnobuttonframe = tk.Frame(self,background=style.color_1, borderwidth = 0, highlightthickness = 0)
        self.yesnobuttonframe.place(relx=0.5,rely=1,y=- (style.buttonsize + style.offset),width=300,x=-150,height=style.buttonsize)

        self.yesbutton = button(self.yesnobuttonframe, callback=self.on_yes,text_string="Yes",background=style.color_2)
        self.yesbutton.place(relx=0.33,relwidth=0.34,relheight=1)

    def on_yes(self):
        print("Exiting...")
        self.exit_callback()
        sys.exit()