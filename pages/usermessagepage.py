import os
import tkinter as tk
from tkinter.constants import *
from widgets import scrolledText, button
import style

class usermessagePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent,background=style.color_1)

        self.usertext = scrolledText(self, wrap = 'word', font = style.hugeboldtext, padx = 4 * style.offset, pady = 4 * style.offset, background = style.color_1, foreground = style.w)
        self.usertext.place(relwidth = 1, relheight = 1, height = - (style.buttonsize + 2 * style.offset))

        self.yesnobuttonframe = tk.Frame(self,background=style.color_1, borderwidth = 0, highlightthickness = 0)
        self.yesnobuttonframe.place(relx=0.5,rely=1,y=- (style.buttonsize + style.offset),width=300,x=-150,height=style.buttonsize)

        self.yesbutton = button(self.yesnobuttonframe, callback=self.hide,text_string="OK",background=style.color_2)
        self.yesbutton.place(relx=0.5,x = -50, width=100,height = style.buttonsize)

    def show(self):
        self.place(relwidth = 1, relheight = 1)

    def hide(self):
        print("-------------------------------")
        self.place_forget()

    def telluser(self, message):
        print("-------------------------------\nInformed User - \n{}".format(message))
        self.usertext.configure(state="normal")
        self.usertext.delete("1.0", END)
        self.usertext.insert(END, message)
        self.usertext.configure(state="disabled")
        self.show()