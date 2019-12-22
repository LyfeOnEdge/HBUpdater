import tkinter as tk
from style import *
#Custom button
#A tkinter label with a bound on-click event to fix some issues 
#that were happening with normal tkinter buttons on MacOS.
#Unfortunately MacOS was causing a weird white translucent
#effect to be applied to all classes that used the tk.Button Widget.
#This fixes it but making our own "button" by binding a callback to 
#an on_click event. Feel free to use this in other projects where mac
#compatibility is an issue, also special thanks to Kabiigon for testing
#this widget until I got it right since I don't have a mac
class button(tk.Label):
	def __init__(self,frame,callback=None,image_object= None,text_string=None,background=color_2, font=smallboldtext, borderwidth = 0):
		self.callback = callback
		self.background = background
		self.selected = False

		tk.Label.__init__(self,frame,
			background=background,
			foreground= w,
			borderwidth= borderwidth,
			activebackground=color_1,
			image=image_object,
			text = text_string,
			font = font,
			anchor="center"
			)
		self.bind('<Button-1>', self.on_click)

	#Use callback when our makeshift "button" clicked
	def on_click(self, event=None):
		self.configure(background = lg)
		if not self.selected:
			self.after(100, self.on_click_color_change)
		if self.callback:
			self.callback()
	
	#Function to set the button's image
	def setimage(self,image):
		self.configure(image=image)

	#Function to set the button's text
	def settext(self,text):
		self.configure(text=text)

	def select(self):
		self.selected = True
		self.configure(background = lg)

	def deselect(self):
		self.selected = False
		self.configure(background = self.background)

	def on_click_color_change(self):
		if not self.selected:
			self.configure(background = self.background)
