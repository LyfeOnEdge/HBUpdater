import tkinter as tk
from tkinter.constants import *
from modules.format import *
import platform, os

#Basic Widgets

#Frame to use instead of default tk.frame, by default themed with light_color
class ThemedFrame(tk.Frame):
	def __init__(self,parent,frame_borderwidth = 0,frame_highlightthickness = 0,background_color = dark_color,frame_highlightcolor=dark_color):
		tk.Frame.__init__(self,parent, 
			background = background_color,
			highlightcolor = frame_highlightcolor,
			highlightthickness=frame_highlightthickness,
			highlightbackground=light_color,
			borderwidth = frame_borderwidth,
			)


#listbox themed properly from format.py
class ThemedListbox(tk.Listbox):
	def __init__(self,frame,font=listbox_font, **kw,):
		tk.Listbox.__init__(self,frame,
			highlightthickness=0,
			highlightbackground=light_color,
			borderwidth=0,
			exportselection = False, 
			background=dark_color,
			foreground=listbox_font_color,
			font=font,
			disabledforeground=dark_listbox_font_color,
			selectbackground=listboxselectionbackground,
			selectforeground=listboxselectionforeground,
			)

#themed author/ etc label
class ThemedLabel(tk.Label):
	def __init__(self,frame,label_text,label_font=smalltext,text_variable=None,background = light_color,foreground=lgray,anchor="w",wraplength = None):
		tk.Label.__init__(self,frame,
			background = background,
			highlightthickness=0,
			anchor=anchor,
			text = label_text,
			font=label_font,
			foreground= foreground,
			textvariable = text_variable,
			)
		if not wraplength == None:
			self.configure(wraplength=wraplength)
	def set(self,text):
		self.configure(text=text)


#Separator, defaults to light color
class Separator(ThemedLabel):
	def __init__(self,frame,color = None):
		if color:
			bgc = color
		else:
			bgc = light_color
		ThemedLabel.__init__(self,frame,"",background=bgc)


#Custom button
#A tkinter label with a bound on-click event to fix some issues 
#that were happening with normal tkinter buttons on MacOS.
#Unfortunately MacOS was causing a weird white translucent
#effect to be applied to all classes that used the tk.Button Widget.
#This fixes it but making our own "button" by binding a callback to 
#an on_click event. Feel free to use this in other projects where mac
#compatibility is an issue, also special thanks to Kabiigon for testing
#this widget until I got it right since I don't have a mac
class navbutton(tk.Label):
	def __init__(self,frame,command_name=None,image_object= None,text_string=None,background=dark_color):
		self.command = command_name

		tk.Label.__init__(self,frame,
			background=background,
			foreground= w,
			borderwidth= 0,
			activebackground=light_color,
			image=image_object,
			text = text_string,
			font = navbuttonfont,
			)
		self.bind('<Button-1>', self.on_click)

	#Use callback when our makeshift "button" clicked
	def on_click(self, event=None):
		if self.command:
			self.command()

	#Function to update the button's set command
	def setcommand(self,command):
		self.command = command

	#Function to set the button's image
	def setimage(self,image):
		self.configure(image=image)

	#Function to set the button's text
	def settext(self,text):
		self.configure(text=text)




#Black box with white text to spew log or text to user
class consolebox(ThemedFrame):
	def __init__(self,frame,):
		ThemedFrame.__init__(self,frame)

		self.textoutput = tk.Text(self,
			wrap="word",
			background = b,
			foreground = w,
			font=consoletext,
			borderwidth = 0,
			state=DISABLED,
			)
		self.textoutput.place(x=0,y=0,relwidth=1,relheight=1)

	def print(self,textToPrint):
		self.textoutput.config(state=NORMAL)
		self.textoutput.insert(END, textToPrint)
		self.textoutput.config(state=DISABLED)
		self.textoutput.see(END)

	def see(self, index):
		self.textoutput.see(index)

#easily loop-generated setting widget
class settingbox(ThemedFrame):
	def __init__(self,frame,value,settingtext,anchor="w"):
		#Value edited by setting
		self.v = value
		checkbox_bool = tk.IntVar()
		
		ThemedFrame.__init__(self,frame)
		self.c = tk.Checkbutton(self, text=settingtext, variable=checkbox_bool,
			anchor="w",
			foreground=dgray,
			activeforeground=dgray,
			background=light_color,
			activebackground=light_color,
			borderwidth=0,
			highlightthickness=0,
			font=smallboldtext
			)
		self.c.v = checkbox_bool
		self.c.place(x=0,y=0,relwidth=1,relheight=1,)

	

	def set(self,bool):
		self.c.v.set(bool)

	def get(self):
		return self.c.v.get()

	def get_setting(self):
		return {self.v : self.get()}


#More mac compatibility, custom combobox
class cbox(ThemedFrame):
	def __init__(self, frame, opt, placeholder, height=30):
		self.frame = frame #Parent frame
		self.opt = opt #options
		self.height = height #Height of entry bar
		self.placeholder = placeholder

		self.state = True #enabled = true
		self.dropdown_state = False #Variable to track if the dropdown is up or not

		# cbox_height = 
		cbox_dropdown_button_width = 20
		cbox_dropdown_separator_width = 2
		ThemedFrame.__init__(self, frame,
			background_color=light_color)

		self.textbox = entrybox(self, placeholder=placeholder)
		self.textbox.place(relwidth=1,height=self.height,width=-(cbox_dropdown_button_width+cbox_dropdown_separator_width))
		self.bsep = Separator(self, color=light_color)
		self.bsep.place(relx=1,x=-(cbox_dropdown_separator_width+cbox_dropdown_button_width),width=cbox_dropdown_separator_width,height=self.height)
		self.dropdown_button = navbutton(self, text_string="▼")
		self.dropdown_button.place(height=self.height, relx=1, width=cbox_dropdown_button_width, x=-cbox_dropdown_button_width)
		self.dropdown_button.bind('<Button-1>', self.on_click)
		#dropdown box, filled with placed children but not placed itself until it is needed
		self.dropdown_box = ThemedFrame(frame, background_color=light_color)
		self.dropdown_options = ScrolledListBox(self.dropdown_box,
			selectmode=SINGLE,
			font=smalltext
			)
		self.dropdown_box_separator = Separator(self.dropdown_box, color = light_color)
		self.dropdown_box_separator.place(x=+cbox_dropdown_button_width/2,height=cbox_dropdown_separator_width,relwidth=1,width=-cbox_dropdown_button_width)
		self.dropdown_options.place(relheight=1,relwidth=1,y=+cbox_dropdown_separator_width,height=-cbox_dropdown_separator_width)
		for o in opt:
			self.dropdown_options.insert(END, o)
		self.dropdown_options.bind('<Button-1>', self.on_select)

	def on_click(self, event=None):
		#If the widget is enabled
		if self.state:
			#If the widget is currently dropped down:
			if self.dropdown_state:
				self.collapse()
			#If the widget is not dropped down, drop it
			else:
				#Place it
				self.expand()

	#Gets the item selected from the listbox and sets it in the entry box
	def on_select(self, event):
		y = event.y
		# try:
		widget = event.widget
		sel = widget.nearest(y)
		picked = widget.get(sel)
		self.set_text(picked)
		self.collapse()
		# except:
		# 	pass

	def setbutton(self):
		if self.dropdown_state:
			self.dropdown_button.settext("▲")
			return
		self.dropdown_button.settext("▼")

	# #Opens dropdown box
	def expand(self):
		eheight = self.textbox.winfo_height()
		bheight = 90 #Height of box with options
		bwidth = self.textbox.winfo_width()
		bx = self.winfo_x()
		by = self.winfo_y()

		self.dropdown_box.place(x=bx,y=by + eheight,height=bheight,width=bwidth)
		self.dropdown_state = True
		self.setbutton()

	#Hides dropdown box
	def collapse(self):
		self.dropdown_box.place_forget()
		self.dropdown_state = False
		self.setbutton()

	#Disables typing in textbox and clicking dropdown
	def disable(self):
		self.collapse()
		self.textbox.disable()
		self.state = False
		
	#Enables typing in textbox and clicking dropdown
	def enable(self):
		self.textbox.enable()
		self.state = True
		
	#Disables typing in text box but not clicking dropdown
	def disabletext(self):
		self.textbox.disable()

	#There is no enabletext(), there is no reason to use this widget for text but not dropdown 

	#Gets the content of the entry
	def get(self):
		return self.textbox.get()

	#Sets the contents of the 
	def set_text(self, text):
		status = self.textbox.cget('state')
		self.textbox.enable()
		self.textbox.set_text(text)
		if status == "disabled":
			self.disabletext()

	def clear(self):
		self.textbox.clear()

class ProgressBar(tk.Frame):
	def __init__(self, parent, progress = None, foreground = dark_color, background = light_color):
		ThemedFrame.__init__(self, parent,
			background = background)
		self.progressframe = ThemedFrame(self, background=foreground)
		self.setValue(progress)

		def setValue(self, val):
			self.progressframe.place(x=0,relheight=1,relwidth=val)






















#compound widgets for different pages
#Used to navigate list pages
class navbox(ThemedFrame):
	def __init__(self,frame,
		
		primary_button_command,
		etc_button_command,
		left_context_command,
		right_context_command,
		etc_button_image,
		etc_button_text = "",
		primary_button_text = "INSTALL",
		left_context_text = "PREV",
		right_context_text = "NEXT",
		):
		ThemedFrame.__init__(self,frame, background_color=light_color, frame_borderwidth=0)

		#big button
		self.primary_button = navbutton(self, text_string = primary_button_text, command_name = primary_button_command)
		self.primary_button.place(relx=0.0, rely=0, x=+navbuttonspacing, height=navbuttonheight, width=(navboxwidth - navbuttonheight) - 3.5 * navbuttonspacing)

		#etc button
		self.etc_button = navbutton(self, text_string = etc_button_text, image_object=etc_button_image, command_name=etc_button_command)
		self.etc_button.place(relx=0, rely=0, x=navboxwidth - (navbuttonheight + 1.5 * navbuttonspacing), height=navbuttonheight, width=navbuttonheight)

		#previous in context
		self.left_context_button = navbutton(self, text_string = left_context_text, command_name = left_context_command)
		self.left_context_button.place(relx=0.0, rely=0, x=+navbuttonspacing, y=navbuttonheight + navbuttonspacing,  height=navbuttonheight, width = ((navboxwidth)*0.5) - 1.5 * navbuttonspacing)

		#next in context
		self.right_context_button = navbutton(self, text_string=right_context_text, command_name=right_context_command)
		self.right_context_button.place(relx=0, rely=0, y=navbuttonheight + navbuttonspacing, height=navbuttonheight, x=((navboxwidth + navbuttonspacing) *0.5), width = ((navboxwidth)*0.5) - 2 * navbuttonspacing)






class titledlistboxframe(ThemedFrame):
	def __init__(self,frame,title):
		ThemedFrame.__init__(self,frame)
		self.label_frame = ThemedFrame(self)
		self.label_frame.place(relx=0.0, rely=0.0, height=columtitlesheight, relwidth=1)
		self.listbox_label = ThemedLabel(self.label_frame, title, label_font = columnlabelfont, background = dark_color, foreground = columnlabelcolor, anchor="w")
		self.listbox_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)


class titledlistbox(ThemedFrame):
	def __init__(self,frame,title):
		ThemedFrame.__init__(self,frame)
		self.label_frame = ThemedFrame(self)
		self.label_frame.place(relx=0.0, rely=0.0, height=columtitlesheight, relwidth=1)
		self.listbox_label = ThemedLabel(self.label_frame, title, label_font = columnlabelfont, background = dark_color, foreground = columnlabelcolor, anchor="w")
		self.listbox_label.place(relx=0, x=+columnoffset, rely=0, height=columtitlesheight-separatorwidth/2, relwidth=1, width = -columnoffset)
		self.listbox_separator = Separator(self) 
		self.listbox_separator.place(y=columtitlesheight-separatorwidth/2,relwidth=1,height=separatorwidth/2)
		self.listbox_frame = ThemedFrame(self)
		self.listbox_frame.place(relx=0, x=+2*columnoffset,rely=0, y=+columtitlesheight, relheight=1,height=-columtitlesheight, relwidth=1,width=-2*columnoffset)
		self.listbox = ThemedListbox(self.listbox_frame)
		self.listbox.place(relheight=1,relwidth=1)

	def activate(self,sel):
		self.listbox.activate(sel)

	def bind(self,event,callback):
		self.listbox.bind(event,callback)

	def configure(self, **args):
		self.listbox.configure(args)

	def itemconfig(self,index,**args):
		self.listbox.itemconfig(index,args)

	def insert(self, index, item):
		self.listbox.insert(index, item)

	def curselection(self):
		return self.listbox.curselection()

	def get(self, arg):
		return self.listbox.get(arg)

	def selection_clear(self,index,end):
		self.listbox.selection_clear(index,end)

	def selection_set(self,index):
		self.listbox.selection_set(index)

	def see(self, index):
		self.listbox.see(index)

	def yview(self,event,delta,units):
		self.listbox.yview(event,delta,units)

	def delete(self, index,end):
		self.listbox.delete(index,end)

	def size(self):
		return self.listbox.size()



class themedtable(ThemedFrame):
	def __init__(self,frame,columns,columnwidth):
		self.listboxes = {}
		ThemedFrame.__init__(self,frame)
		numcolumns = len(columns)
		curcolumn = 0
		curx = 0
		for column in reversed(columns):
			listbox = titledlistbox(self, column)
			
			#if we are on last column, make it fill the rest of the available space
			if curcolumn == numcolumns-1:
				listbox.place(relx=0,relwidth=1,width=-curx,relheight=1)
			else:
				listbox.place(relx=1,x=-(curx+columnwidth-separatorwidth/2),relheight=1,width=(columnwidth-separatorwidth/2))
				lbseparator = Separator(self)
				lbseparator.place(relx=1,x=-(curx+columnwidth),relheight=1,width=separatorwidth/2)
				curx += columnwidth

			self.listboxes[column] = listbox
			curcolumn += 1

	def clear(self):
		for lb in self.listboxes:
			self.listboxes[lb].delete(0,END)

class cwdevlabel(tk.Label):
	def __init__(self,frame,label_text,anchor="w"):
		tk.Label.__init__(self,frame,
			background = light_color, 
			foreground = lgray,
			borderwidth = 0,
			highlightthickness = 0,
			font = mediumboldtext,
			anchor = anchor,
			text = label_text,
			)


class cwdevtext(tk.Text):
	def __init__(self,frame,background=light_color):
		tk.Text.__init__(self,frame,
			background=background,
			foreground=lgray,
			borderwidth = 0,
			highlightthickness = 0,
			font = smalltext,
			)

class devbox(ThemedFrame):
	def __init__(self,frame,devname,devtext,devimage,command_name=None):
		ThemedFrame.__init__(self,frame,background_color=light_color)

		self.devimage = navbutton(self,image_object=devimage,command_name=command_name,background=light_color)
		self.devimage.place(x=0,y=0,width=2*navbuttonheight,height=2*navbuttonheight)

		self.devname = cwdevlabel(self,devname)
		self.devname.place(x=2*navbuttonheight+separatorwidth,y=0,relwidth=1)

		self.devtext = cwdevtext(self)
		self.devtext.place(x=2*navbuttonheight+separatorwidth,y=0.5*navbuttonheight+separatorwidth,relwidth=1,width=-(2*navbuttonheight+separatorwidth))
		self.devtext.insert(END,devtext)
















#Tooltip
class ToolTipBase:
	def __init__(self, button):
		self.button = button
		self.tipwindow = None
		self.id = None
		self.x = self.y = 0
		self._id1 = self.button.bind("<Enter>", self.enter)
		self._id2 = self.button.bind("<Leave>", self.leave)
		self._id3 = self.button.bind("<ButtonPress>", self.leave)

	def enter(self, event=None):
		self.schedule()

	def leave(self, event=None):
		self.unschedule()
		self.hidetip()

	def schedule(self):
		self.unschedule()
		self.id = self.button.after(10, self.showtip)

	def unschedule(self):
		id = self.id
		self.id = None
		if id:
			self.button.after_cancel(id)

	def showtip(self):
		if self.tipwindow:
			return
		# The tip window must be completely outside the button;
		# otherwise when the mouse enters the tip window we get
		# a leave event and it disappears, and then we get an enter
		# event and it reappears, ad naseum.
		x = self.button.winfo_rootx() + 20
		y = self.button.winfo_rooty() + self.button.winfo_height() + 1
		self.tipwindow = tw = tk.Toplevel(self.button)
		tw.wm_overrideredirect(1)
		tw.wm_geometry("+%d+%d" % (x, y))
		self.showcontents()

	def showcontents(self, text=""):
		label = tk.Label(self.tipwindow, text=text, justify=LEFT,
					  background=dark_color, 
					  relief=SOLID, 
					  borderwidth=2,
					  foreground=lgray,
					  font=mediumboldtext
					  )
		label.pack()

	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()

class tooltip(ToolTipBase):
	def __init__(self, button, text):
		ToolTipBase.__init__(self, button)
		self.text = text

	def showcontents(self):
		ToolTipBase.showcontents(self, self.text)













#User Entry Boxes:
class Placeholder_State(object):
	 __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'contains_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
	normal_color = entry.cget("fg")
	normal_font = entry.cget("font")

	if font is None:
		font = normal_font

	state = Placeholder_State()
	state.normal_color=normal_color
	state.normal_font=normal_font
	state.placeholder_color=color
	state.placeholder_font=font
	state.placeholder_text = placeholder
	state.contains_placeholder=True

	def on_focusin(event, entry=entry, state=state):
		if state.contains_placeholder:
			entry.delete(0, "end")
			entry.config(fg = state.normal_color, font=state.normal_font)
		
			state.contains_placeholder = False

	def on_focusout(event, entry=entry, state=state):
		if entry.get() == '':
			entry.insert(0, state.placeholder_text)
			entry.config(fg = state.placeholder_color, font=state.placeholder_font)
			
			state.contains_placeholder = True

	entry.insert(0, placeholder)
	entry.config(fg = color, font=font)

	entry.bind('<FocusIn>', on_focusin, add="+")
	entry.bind('<FocusOut>', on_focusout, add="+")
	
	entry.placeholder_state = state

	return state

#Search box, use enter to exec bound callback
class SearchBox(tk.Frame):
	def __init__(self, master, entry_width=30, 
		entry_font=search_font, 
		entry_background=dark_color, 
		entry_foreground=search_font_color, 
		button_text="Search", button_ipadx=10, 
		button_background=dark_color, 
		button_foreground="white", button_font=None, 
		placeholder=place_holder_text, 
		placeholder_font=place_holder_font, 
		placeholder_color=place_holder_color, 
		spacing=3, 
		command=None,
		command_on_keystroke = False,
		):

		tk.Frame.__init__(self, master, borderwidth=0, highlightthickness=0,background=entry_background)

		self._command = command

		self.entry = tk.Entry(self, width=entry_width, background=entry_background, highlightcolor=button_background, highlightthickness=0, foreground = entry_foreground,borderwidth=0)
		self.entry.place(x=+searchoffset,y=0,relwidth=1,relheight=1,width=-searchoffset)
		
		if entry_font:
			self.entry.configure(font=entry_font)

		if placeholder:
			add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=placeholder_font)

		if command_on_keystroke:
			self.entry.bind("<KeyRelease>", self._on_execute_command)

		self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())
		self.entry.bind("<Return>", self._on_execute_command)

	def get_text(self):
		entry = self.entry
		if hasattr(entry, "placeholder_state"):
			if entry.placeholder_state.contains_placeholder:
				return ""
		return entry.get()
		
	def set_text(self, text):
		entry = self.entry
		if hasattr(entry, "placeholder_state"):
			entry.placeholder_state.contains_placeholder = False

		entry.delete(0, END)
		entry.insert(0, text)
		
	def clear(self):
		self.entry_var.set("")
		
	def focus(self):
		self.entry.focus()

	def _on_execute_command(self, event):
		text = self.get_text()
		if self._command:
			self._command(text)

#Smaller version of the search box (above)
class entrybox(tk.Frame):
	def __init__(self, master, 
		entry_width=30, 
		entry_font=entrybox_font, 
		entry_background=dark_color, 
		entry_foreground=search_font_color, 
		placeholder=place_holder_text,
		placeholder_font=repo_placeholder_font, 
		placeholder_color=place_holder_color, 
		spacing=10, 
		command=None, 
		justification="left"
	):

		tk.Frame.__init__(self, master, borderwidth=0, highlightthickness=0,background=entry_background,)
		
		self._command = command

		self.entry = tk.Entry(self, 
			width=entry_width, 
			background=entry_background, 
			disabledbackground=entry_background,
			foreground = entry_foreground,
			disabledforeground=w,
			highlightcolor=dark_color, 
			highlightthickness=0, 
			borderwidth=0,
			justify=justification
			)
		self.entry.place(x=0,y=0,relwidth=1,relheight=1)
		
		if entry_font:
			self.entry.configure(font=entry_font)

		if placeholder:
			add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=repo_placeholder_font)

		self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())

		self.focus()
		self.on_focusout()

		self.last = None

	def get(self):
		entry = self.entry
		if hasattr(entry, "placeholder_state"):
			if entry.placeholder_state.contains_placeholder:
				return ""
		return entry.get().strip().strip("/")

	def cget(self, kw):
		entry = self.entry
		return entry.cget(kw)

	def set_text(self, text):
		if not text == None and not text == "":
			self.last = self.get()
			self.on_focusin()
			self.entry.insert(0, text)
			self.on_focusout()
		else:
			self.focus()


	def on_focusin(self):
		entry = self.entry
		state = entry.placeholder_state
		
		if state.contains_placeholder:
			entry.config(fg = state.normal_color, font=state.normal_font)
			state.contains_placeholder = False

		entry.delete(0, "end")

	def on_focusout(self):
		entry = self.entry
		state = entry.placeholder_state

		if entry.get() == '':
			entry.insert(0, state.placeholder_text)
			entry.config(fg = state.placeholder_color, font=state.placeholder_font)
			
			state.contains_placeholder = True

		if state.contains_placeholder:
			entry.configure(disabledforeground = state.placeholder_color, font = state.placeholder_font)
		else:
			entry.configure(disabledforeground = state.normal_color, font = state.normal_font)

	def clear(self):
		self.entry.delete(0, END)
		self.focus()
		
	def focus(self):
		self.entry.nametowidget(".").focus()

	def disable(self):
		self.entry.configure(state=DISABLED)

	def enable(self):
		self.entry.configure(state=NORMAL)















#Widgets with scroll bars that appear when needed and supporting code
#Automatic scrollbars on certain text boxes
class AutoScroll(object):
	def __init__(self, master):
		try:
			vsb = tk.Scrollbar(master, orient='vertical', command=self.yview)
		except:
			pass
		hsb = tk.Scrollbar(master, orient='horizontal', command=self.xview)

		try:
			self.configure(yscrollcommand=self._autoscroll(vsb))
		except:
			pass
		self.configure(xscrollcommand=self._autoscroll(hsb))

		self.grid(column=0, row=0, sticky='nsew')
		try:
			vsb.grid(column=1, row=0, sticky='ns')
		except:
			pass
		hsb.grid(column=0, row=1, sticky='ew')

		master.grid_columnconfigure(0, weight=1)
		master.grid_rowconfigure(0, weight=1)

		methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
			| tk.Place.__dict__.keys()

		for meth in methods:
			if meth[0] != '_' and meth not in ('config', 'configure'):
				setattr(self, meth, getattr(master, meth))

	@staticmethod
	def _autoscroll(sbar):
		'''Hide and show scrollbar as needed.'''
		def wrapped(first, last):
			first, last = float(first), float(last)
			if first <= 0 and last >= 1:
				sbar.grid_remove()
			else:
				sbar.grid()
			sbar.set(first, last)
		return wrapped

	def __str__(self):
		return str(self.master)

def _create_container(func):
	'''Creates a tk Frame with a given master, and use this new frame to
	place the scrollbars and the widget.'''
	def wrapped(cls, master, **kw):
		container = tk.Frame(master)
		container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
		container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
		return func(cls, container, **kw)
	return wrapped

class ScrolledText(AutoScroll, tk.Text):
	'''A standard Tkinter Text widget with scrollbars that will
	automatically show/hide as needed.'''
	@_create_container
	def __init__(self, master, **kw):
		tk.Text.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

class ScrolledListBox(AutoScroll, ThemedListbox):
	@_create_container
	def __init__(self, master, **kw):
		ThemedListbox.__init__(self, master, **kw,)
		AutoScroll.__init__(self, master)

def _bound_to_mousewheel(event, widget):
	child = widget.winfo_children()[0]
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
	else:
		child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
		child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		widget.unbind_all('<MouseWheel>')
		widget.unbind_all('<Shift-MouseWheel>')
	else:
		widget.unbind_all('<Button-4>')
		widget.unbind_all('<Button-5>')
		widget.unbind_all('<Shift-Button-4>')
		widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
	if platform.system() == 'Windows':
		widget.yview_scroll(-1*int(event.delta/120),'units')
	elif platform.system() == 'Darwin':
		widget.yview_scroll(-1*int(event.delta),'units')
	else:
		if event.num == 4:
			widget.yview_scroll(-1, 'units')
		elif event.num == 5:
			widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
	if platform.system() == 'Windows':
		widget.xview_scroll(-1*int(event.delta/120), 'units')
	elif platform.system() == 'Darwin':
		widget.xview_scroll(-1*int(event.delta), 'units')
	else:
		if event.num == 4:
			widget.xview_scroll(-1, 'units')
		elif event.num == 5:
			widget.xview_scroll(1, 'units')