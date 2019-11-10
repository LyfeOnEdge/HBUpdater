import os
import tkinter as tk
from tkinter.constants import *
from widgets import button, ThemedLabel
import style

class settingsPage(tk.Frame):
	def __init__(self, parent, settings):
		tk.Frame.__init__(self,parent,background=style.color_2)
		self.settings = settings
		
		thumbnail_sizes = ["tiny", "small", "medium", "large", "huge"]

		self.selected_thumbnail_size = tk.StringVar()
		self.selected_thumbnail_size.set(thumbnail_sizes[0])
		self.thumbnail_size_dropdown = tk.OptionMenu(self,self.selected_thumbnail_size,*thumbnail_sizes)
		self.thumbnail_size_dropdown.configure(foreground = style.w)
		self.thumbnail_size_dropdown.configure(background = style.color_1)
		self.thumbnail_size_dropdown.configure(highlightthickness = 0)
		self.thumbnail_size_dropdown.configure(borderwidth = 0)
		self.thumbnail_size_dropdown.place(y = style.offset, x = style.offset, height = style.buttonsize, width = 200 - style.offset)
		self.thumbnail_size_dropdown_label = ThemedLabel(self, label_text = "~ Tile Size", background = style.color_2)
		self.thumbnail_size_dropdown_label.place(y = style.offset, x = 200 + style.offset, height = style.buttonsize, width = 200)

		self.savebutton = button(self, callback=self.save,text_string="Save",background=style.color_1)
		self.savebutton.place(relx=0.5, x = - 0.5 * style.sidecolumnwidth, width = style.sidecolumnwidth, height = style.buttonsize, rely = 1, y = - (style.offset + style.buttonsize))

		#Bind frame raise
		self.bind("<<ShowFrame>>", self.configure)

	def configure(self, event):
		self.selected_thumbnail_size.set(self.settings.get_setting("thumbnail_size"))

	def save(self):
		self.settings.set_setting("thumbnail_size", self.selected_thumbnail_size.get())
		self.settings.save()

	def show(self):
		self.place(relwidth = 1, relheight = 1)

	def hide(self):
		self.place_forget()



