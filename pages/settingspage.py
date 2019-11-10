import os
import tkinter as tk
from tkinter.constants import *
from widgets import button, ThemedLabel
import style




class customOptionMenu(tk.OptionMenu):
	def __init__(self, frame, opts):
		option = tk.StringVar()
		tk.OptionMenu.__init__(self, frame, option, *opts)
		self.configure(foreground = style.w)
		self.configure(background = style.color_1)
		self.configure(highlightthickness = 0)
		self.configure(borderwidth = 0)
		self.option = option
		self.option.set(opts[0])

class settingsPage(tk.Frame):
	def __init__(self, parent, settings):
		tk.Frame.__init__(self,parent,background=style.color_2)
		self.settings = settings

		self.settings_page_header = ThemedLabel(self, label_text = "Most settings will not take effect until next launch", background = style.color_2, label_font = style.mediumboldtext)
		self.settings_page_header.place(y = style.offset, x = style.offset, height = style.buttonsize - 2 * style.offset, relwidth = 1, width = - 2 * style.offset)
		
		thumbnail_sizes = ["tiny", "small", "medium", "large", "huge"]
		self.thumbnail_size_dropdown = customOptionMenu(self, thumbnail_sizes)
		self.thumbnail_size_dropdown.place(y = style.offset + style.buttonsize, x = style.offset, height = style.buttonsize - 2 * style.offset, width = 200 - style.offset)
		self.thumbnail_size_dropdown_label = ThemedLabel(self, label_text = "~ Tile Size\n(No restart)", background = style.color_2)
		self.thumbnail_size_dropdown_label.place(y = style.offset + style.buttonsize, x = 200 + style.offset, height = style.buttonsize - 2 * style.offset, width = 200)

		maximized_options = [ "fullscreen", "maximized", "windowed"]
		self.maximized_on_launch_dropdown = customOptionMenu(self, maximized_options)
		self.maximized_on_launch_dropdown.place(y = 2 * (style.offset + style.buttonsize), x = style.offset, height = style.buttonsize - 2 * style.offset, width = 200 - style.offset)
		self.maximized_dropdown_label = ThemedLabel(self, label_text = "~ Maximized on launch", background = style.color_2)
		self.maximized_dropdown_label.place(y = 2 * (style.offset + style.buttonsize), x = 200 + style.offset, height = style.buttonsize - 2 * style.offset, width = 200)

		topmost_options = [ "true", "false"]
		self.topmost_dropdown = customOptionMenu(self, topmost_options)
		self.topmost_dropdown.place(y = 3 * (style.offset + style.buttonsize), x = style.offset, height = style.buttonsize - 2 * style.offset, width = 200 - style.offset)
		self.topmost_dropdown_label = ThemedLabel(self, label_text = "~ Keep window topmost?", background = style.color_2)
		self.topmost_dropdown_label.place(y = 3 * (style.offset + style.buttonsize), x = 200 + style.offset, height = style.buttonsize - 2 * style.offset, width = 200)

		self.savebutton = button(self, callback=self.save,text_string="Save",background=style.color_1)
		self.savebutton.place(relx=0.5, x = - 0.5 * style.sidecolumnwidth, width = style.sidecolumnwidth, height = style.buttonsize, rely = 1, y = - (style.offset + style.buttonsize))
		#Bind frame raise
		self.bind("<<ShowFrame>>", self.configure)

	def configure(self, event):
		self.thumbnail_size_dropdown.option.set(self.settings.get_setting("thumbnail_size"))
		self.maximized_on_launch_dropdown.option.set(self.settings.get_setting("maximized"))
		self.topmost_dropdown.option.set(self.settings.get_setting("keep_topmost"))

	def save(self):
		self.settings.set_setting("thumbnail_size", self.thumbnail_size_dropdown.option.get())
		self.settings.set_setting("maximized", self.maximized_on_launch_dropdown.option.get())
		self.settings.set_setting("keep_topmost", self.topmost_dropdown.option.get())
		self.settings.save()

	def show(self):
		self.place(relwidth = 1, relheight = 1)

	def hide(self):
		self.place_forget()