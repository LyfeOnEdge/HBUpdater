import tkinter as tk
from tkinter.constants import *
from modules.format import *
import modules.guicore as guicore
import platform

if guicore.getpilstatus():
	from PIL import Image, ImageTk


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

class SearchBox(tk.Frame):
	def __init__(self, master, entry_width=30, entry_font=search_font, entry_background=dark_color, entry_foreground=search_font_color, button_text="Search", button_ipadx=10, button_background=dark_color, button_foreground="white", button_font=None, placeholder=place_holder_text, placeholder_font=place_holder_font, placeholder_color=place_holder_color, spacing=3, command=None):
		tk.Frame.__init__(self, master, borderwidth=0, highlightthickness=0,background=entry_background)
		
		self._command = command

		self.entry = tk.Entry(self, width=entry_width, background=entry_background, highlightcolor=button_background, highlightthickness=0, foreground = entry_foreground,borderwidth=0)
		self.entry.place(x=+searchoffset,y=0,relwidth=1,relheight=1,width=-searchoffset)
		
		if entry_font:
			self.entry.configure(font=entry_font)

		if placeholder:
			add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=placeholder_font)

		self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())
		self.entry.bind("<Return>", self._on_execute_command)

	def get_text(self):
		entry = self.entry
		if hasattr(entry, "placeholder_state"):
			if entry.placeholder_state.contains_placeholder:
				return ""
			else:
				return entry.get()
		else:
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
		self._command(text)

class entrybox(tk.Frame):
	def __init__(self, master, entry_width=30, entry_font=entrybox_font, entry_background=dark_color, entry_foreground=search_font_color, button_text="Search", button_ipadx=10, button_background=dark_color, button_foreground="white", button_font=None, placeholder=place_holder_text, placeholder_font=repo_placeholder_font, placeholder_color=place_holder_color, spacing=3, command=None, justification="left"):
		tk.Frame.__init__(self, master, borderwidth=0, highlightthickness=0,background=entry_background,)
		
		self._command = command

		self.entry = tk.Entry(self, 
			width=entry_width, 
			background=entry_background, 
			disabledbackground=entry_background,
			foreground = entry_foreground,
			disabledforeground=w,
			highlightcolor=button_background, 
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

		#This entry never gets placed, 
		#it's just used to jump to whenever 
		#text is set so that the placeholder 
		#gets filled when there is no text inserted
		self.dummyentry = tk.Entry(self)
		self.dummyentry.configure(state=DISABLED)
		self.focus()

	def get_text(self):
		entry = self.entry
		if hasattr(entry, "placeholder_state"):
			if entry.placeholder_state.contains_placeholder:
				return ""
			else:
				return entry.get()
		else:
			return entry.get()
		
	def set_text(self, text):
		entry = self.entry
		if hasattr(entry, "placeholder_state"):
			entry.placeholder_state.contains_placeholder = False

		if not text == None and not text == "":
			entry.delete(0, END)
			entry.insert(0, text)
		else:
			self.focus()

	def clear(self):
		self.entry.delete(0, END)
		self.focus()
		
	def focus(self):
		self.entry.focus()
		self.dummyentry.configure(state=NORMAL)
		self.dummyentry.focus()
		self.dummyentry.configure(state=DISABLED)

	def unfocus(self):
		self.dummyentry.configure(state=NORMAL)
		self.dummyentry.focus()
		self.dummyentry.configure(state=DISABLED)

	def disable(self):
		self.entry.configure(state=DISABLED)

	def enable(self):
		self.entry.configure(state=NORMAL)



#Automatic scrollbar on labels
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

		# if py3:
		methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
			| tk.Place.__dict__.keys()
		# else:
		#   methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
		#       + tk.Place.__dict__.keys()

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
	'''Creates a ttk Frame with a given master, and use this new frame to
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

class ScrolledListBox(AutoScroll, tk.Listbox):
	@_create_container
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
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

#Frame themed properly from format.py
class themedframe(tk.Frame):
	def __init__(self,parent,frame_borderwidth = 0,frame_highlightthickness = 0,background_color = dark_color,frame_highlightcolor=dark_color):
		tk.Frame.__init__(self,parent, 
			background = background_color,
			highlightcolor = frame_highlightcolor,
			highlightthickness=frame_highlightthickness,
			highlightbackground=light_color,
			borderwidth = frame_borderwidth,
			)

#listbox themed properly from format.py
class customlistbox(tk.Listbox):
	def __init__(self,frame, **kw, ):
		tk.Listbox.__init__(self,frame,**kw,
			highlightthickness=0,
			highlightbackground=light_color,
			borderwidth=0,
			exportselection = False, 
			background=dark_color,
			foreground=listbox_font_color,
			font=listbox_font,
			disabledforeground=dark_listbox_font_color,
			selectbackground=listboxselectionbackground,
			selectforeground=listboxselectionforeground,
			)

#search bar icons with theme
class iconbutton(tk.Listbox):
	def __init__(self,frame, image_object,command_name,):
		tk.Button.__init__(self,frame,
			background = dark_color, 
			activebackground = light_color,
			borderwidth = 0,
			highlightthickness = 0,
			image = image_object,
			command = command_name,
			)

#themed colum label
class columnlabel(tk.Label):
	def __init__(self,frame,label_text,anchor="w",background=dark_color):
		tk.Label.__init__(self,frame,
			background = background, 
			foreground = columnlabelcolor,
			borderwidth = 0,
			highlightthickness = 0,
			font = columnlabelfont,
			anchor = anchor,
			text = label_text,
			)

#themed nav button
class navbutton(tk.Button):
	def __init__(self,frame,command_name=None,image_object= None,text_string=None,background=dark_color):
		tk.Button.__init__(self,frame,
			background=background,
			borderwidth=0,
			activebackground=background,
			#pady="0",
			image=image_object,
			command=command_name,
			text = text_string,
			font = navbuttonfont,
			foreground = w
			)
	def setcommand(self,command):
		self.configure(command=command)

	def setimage(self,image=None):
		self.configure(image=image)



class navbox(themedframe):
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
		themedframe.__init__(self,frame, background_color=light_color, frame_borderwidth=0)

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




#themed author/ etc label
class themedlabel(tk.Label):
	def __init__(self,frame,label_text,label_font=smalltext,label_color=w,text_variable=None,background = light_color,anchor="n",justify=None):
		tk.Label.__init__(self,frame,
			background = background,
			highlightthickness=0,
			anchor=anchor,
			text = label_text,
			font=label_font,
			foreground= label_color,
			textvariable = text_variable,
			)

		if not justify == None:
			self.configure()
class themedguidelabel(tk.Label):
	def __init__(self,frame,label_text,label_font=smalltext,label_color=w,text_variable=None,anchor="w",background=light_color,wraplength = None):
		tk.Label.__init__(self,frame,
			background = background,
			highlightthickness=0,
			anchor=anchor,
			text = label_text,
			font=label_font,
			foreground= label_color,
			textvariable = text_variable,
			) 
		if not wraplength == None:
			self.configure(wraplength=wraplength)
	def set(self,text):
		self.configure(text=text)

class separator(themedlabel):
	def __init__(self,frame):
		themedlabel.__init__(self,frame,"")

class darkseparator(themedlabel):
	def __init__(self,frame):
		themedlabel.__init__(self,frame,"",background=dark_color)


class infobox(themedframe):
	def __init__(self,frame):
		themedframe.__init__(self,frame,background_color=light_color,frame_borderwidth=0)

		#holds author picture
		self.project_art_label =themedlabel(self,label_text = "project_art",)
		self.project_art_label.place(relx=0.0, rely=0.0, height=infoframewidth, relwidth=1)

		#Homebrew Title
		self.titlevar = tk.StringVar()
		self.titlevar.set("title_var")
		self.project_title_label = themedlabel(self, 
			label_text = "project_title", 
			text_variable = self.titlevar, 
			label_color=info_softwarename_color, 
			label_font=info_softwarename_font
			)
		self.project_title_label.place(relx=0.0, rely=0.0, y=infoframewidth, relwidth=1.0)


		#author name
		self.authorvar = tk.StringVar()
		self.authorvar.set("author_var")
		self.author_name_label = themedlabel(self,
			label_text = "author_name", 
			text_variable = self.authorvar, 
			label_color=info_author_color, 
			label_font=info_author_font
			)
		self.author_name_label.place(relx=0.0, rely=0, y=infoframewidth + 25,  relwidth=1.0)

		self.topsep = themedframe(self,
			background_color = lgray,
			frame_borderwidth = 2,
		)
		self.topsep.place(x = (infoframewidth / 2), y = infoframewidth+52, height = 4, relwidth = 0.9, anchor="center")

		#Description
		self.project_description = ScrolledText(self)
		self.project_description.place(relx=0.5, rely=0.0, y=+infoframewidth+55, relheight = 1, height=-(infoframewidth + 55 + 100), relwidth=0.85, anchor = "n")
		self.project_description.configure(background=light_color)
		self.project_description.configure(foreground=info_description_color)
		self.project_description.configure(font=info_description_font)
		self.project_description.configure(wrap="word")
		self.project_description.configure(state=NORMAL)
		self.project_description.delete('1.0', END)
		self.project_description.insert(END, "Project description")
		self.project_description.configure(state=DISABLED)
		self.project_description.configure(borderwidth=0)

		self.topsep = themedframe(self,
			background_color = lgray,
			frame_borderwidth = 2,
		)
		self.topsep.place(x = (infoframewidth / 2), rely = 1, y = -95, height = 4, relwidth = 0.9, anchor="center")


	def updatetitle(self,title):
		self.titlevar.set(title)

	#update author information
	def updateauthor(self,author):
		self.authorvar.set("by {}".format(author))

	def updateimage(self,image_path):
		#Default image handling method
		if not guicore.getpilstatus():
			imagemax = infoframewidth
			art_image = tk.PhotoImage(file=image_path)
			while not (art_image.width() > (imagemax - 80) and not (art_image.width() > imagemax)):
				if art_image.width() > imagemax:
					art_image = art_image.subsample(2)
				if art_image.width() < (imagemax - 80):
					art_image = art_image.zoom(3)
		else:
		#Pillow handling
			art_image = Image.open(image_path)
			art_image = art_image.resize((infoframewidth, infoframewidth), Image.ANTIALIAS)
			art_image = ImageTk.PhotoImage(art_image)
		

		self.project_art_label.configure(image=art_image)
		self.project_art_label.image = art_image

	#update project description
	def updatedescription(self, desc):
		self.project_description.configure(state=NORMAL)
		self.project_description.delete('1.0', END)
		self.project_description.insert(END, desc)
		self.project_description.configure(state=DISABLED)

	# #update all info in the info box
	# def updateinfo(self, list, softwarechunknumber):

	# 	self.updateAuthorImage()

	# 	self.updatedescription(list[softwarechunknumber]["description"])


class consolebox(themedframe):
	def __init__(self,frame,):
		themedframe.__init__(self,frame)

		self.textoutput = tk.Text(self,wrap="word")
		self.textoutput.place(x=0,y=0,relwidth=1,relheight=1)
		self.textoutput.configure(background = b)
		self.textoutput.configure(foreground = w)
		self.textoutput.configure(state=DISABLED)
		self.textoutput.configure(font=consoletext)
		self.textoutput.configure(borderwidth = 0)

	def print(self,textToPrint):
		self.textoutput.config(state=NORMAL)
		self.textoutput.insert(END, textToPrint)
		self.textoutput.config(state=DISABLED)
		self.textoutput.see(END)

	def see(self, index):
		self.textoutput.see(index)

	# def printbytes(self,bytesToPrint):
	#   self.textoutput.config(state=NORMAL)
	#   self.textoutput.insert(END, (bytesToPrint.decode("utf-8")))
	#   self.textoutput.config(state=DISABLED)
	#   self.textoutput.see(END)

class titledlistboxframe(themedframe):
	def __init__(self,frame,title):
		themedframe.__init__(self,frame)
		self.label_frame = themedframe(self)
		self.label_frame.place(relx=0.0, rely=0.0, height=columtitlesheight, relwidth=1)
		self.listbox_label = columnlabel(self.label_frame, title)
		self.listbox_label.place(relx=0, x=+5, rely=0, relheight=1, relwidth=1, width = -5)


class titledlistbox(themedframe):
	def __init__(self,frame,title):
		themedframe.__init__(self,frame)
		self.label_frame = themedframe(self)
		self.label_frame.place(relx=0.0, rely=0.0, height=columtitlesheight, relwidth=1)
		self.listbox_label = columnlabel(self.label_frame, title)
		self.listbox_label.place(relx=0, x=+columnoffset, rely=0, height=columtitlesheight-separatorwidth/2, relwidth=1, width = -columnoffset)
		self.listbox_separator = separator(self)
		self.listbox_separator.place(y=columtitlesheight-separatorwidth/2,relwidth=1,height=separatorwidth/2)
		self.listbox_frame = themedframe(self)
		self.listbox_frame.place(relx=0, x=+2*columnoffset,rely=0, y=+columtitlesheight, relheight=1,height=-columtitlesheight, relwidth=1,width=-2*columnoffset)
		self.listbox = customlistbox(self.listbox_frame)
		self.listbox.place(relheight=1,relwidth=1)

	def bind(self,event,callback):
		self.listbox.bind(event,callback)

	def configure(self, **args):
		self.listbox.configure(**args)

	def itemconfig(self,index,**args):
		self.listbox.itemconfig(index,**args)

	def insert(self, index, item):
		self.listbox.insert(index, item)

	def curselection(self):
		return self.listbox.curselection()

	def get(self, **args):
		return self.listbox.get(**args)

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



class themedtable(themedframe):
	def __init__(self,frame,columns,columnwidth):
		self.listboxes = {}
		themedframe.__init__(self,frame)
		numcolumns = len(columns)
		curcolumn = 0
		curx = 0
		self.listbox = {}
		for column in reversed(columns):
			self.listbox[column] = titledlistbox(self, column)
			
			#if we are on last column, make it fill the rest of the available space
			if curcolumn == numcolumns-1:
				self.listbox[column].place(relx=0,relwidth=1,width=-curx,relheight=1)
			else:
				self.listbox[column].place(relx=1,x=-(curx+tablecolumnwidth-separatorwidth/2),relheight=1,width=(tablecolumnwidth-separatorwidth/2))
				self.separator = separator(self)
				self.separator.place(relx=1,x=-(curx+tablecolumnwidth),relheight=1,width=separatorwidth/2)
				curx += tablecolumnwidth

			self.listboxes[column] = self.listbox[column]
			curcolumn += 1

class cwdevlabel(tk.Label):
	def __init__(self,frame,label_text,anchor="w"):
		tk.Label.__init__(self,frame,
			background = dark_color, 
			foreground = lgray,
			borderwidth = 0,
			highlightthickness = 0,
			font = mediumboldtext,
			anchor = anchor,
			text = label_text,
			)


class cwdevtext(tk.Text):
	def __init__(self,frame):
		tk.Text.__init__(self,frame,
			background=dark_color,
			foreground=lgray,
			borderwidth = 0,
			highlightthickness = 0,
			font = smalltext,
			)

class devbox(themedframe):
	def __init__(self,frame,devname,devtext,devimage,command_name=None):
		themedframe.__init__(self,frame)

		self.devimage = navbutton(self,image_object=devimage,command_name=command_name)
		self.devimage.place(x=0,y=0,width=2*navbuttonheight,height=2*navbuttonheight)

		self.devname = cwdevlabel(self,devname)
		self.devname.place(x=2*navbuttonheight+separatorwidth,y=0,relwidth=1)

		self.devtext = cwdevtext(self)
		self.devtext.place(x=2*navbuttonheight+separatorwidth,y=0.5*navbuttonheight+separatorwidth,relwidth=1,width=-(2*navbuttonheight+separatorwidth))
		self.devtext.insert(END,devtext)



class settingbox(themedframe):
	def __init__(self,frame,settingtext):
		v = tk.IntVar()
		themedframe.__init__(self,frame)
		
		self.c = tk.Checkbutton(self, text=settingtext, variable=v,
			anchor="w",
			foreground=dgray,
			activeforeground=dgray,
			background=light_color,
			activebackground=light_color,
			borderwidth=0,
			highlightthickness=0,
			font=mediumboldtext
			)

		self.c.var = v
		self.c.place(x=0,relwidth=1,relheight=1,y=0)

	def set(self,bool):
		self.c.var.set(bool)

	def get(self):
		return self.c.var.get()

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
        # event and it reappears, and so on forever :-(
        x = self.button.winfo_rootx() + 20
        y = self.button.winfo_rooty() + self.button.winfo_height() + 1
        self.tipwindow = tw = tk.Toplevel(self.button)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        self.showcontents()

    def showcontents(self, text="Your text here"):
        # Override this in derived class
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

