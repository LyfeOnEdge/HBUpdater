import os
import tkinter as tk
from tkinter.constants import *
from widgets import scrolledText, button
import style

class yesnoPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent,background=style.color_1)
        self.yes_command = None

        self.usertext = scrolledText(self, wrap = 'word', font = style.hugeboldtext, padx = 4 * style.offset, pady = 4 * style.offset, background = style.color_1, foreground = style.w)
        self.usertext.place(relwidth = 1, relheight = 1, height = - (style.buttonsize + 2 * style.offset))

        self.yesnobuttonframe = tk.Frame(self,background=style.color_1, borderwidth = 0, highlightthickness = 0)
        self.yesnobuttonframe.place(relx=0.5,rely=1,y=- (style.buttonsize + style.offset),width=300,x=-150,height=style.buttonsize)

        self.yesbutton = button(self.yesnobuttonframe, callback=self.on_yes,text_string="Yes",background=style.color_2)
        self.yesbutton.place(relx=0,relwidth=0.33,relheight=1)

        self.nobutton = button(self.yesnobuttonframe, callback=self.on_no,text_string="No",background=style.color_2)
        self.nobutton.place(relx=0.67,relwidth=0.33,relheight=1)

    def show(self):
        self.place(relwidth = 1, relheight = 1)

    def hide(self):
        self.place_forget()


    def getanswer(self, question, yes_command):
        self.yes_command = yes_command

        print("-------------------------------\nQuestion raised - \n{}".format(question))
        self.usertext.configure(state="normal")
        self.usertext.delete("1.0", END)
        self.usertext.insert(END, question)
        self.usertext.configure(state="disabled")
        self.show()

    def on_yes(self):
        print("Got yes\n-------------------------------")
        self.yes_command()
        self.yes_command = None
        self.hide()

    def on_no(self):
        print("Got no\n-------------------------------")
        self.yes_command = None
        self.hide()