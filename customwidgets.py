import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from format import *

#Mit License
def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))

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

#Searchbox, mit license.
class SearchBox(tk.Frame):
    def __init__(self, master, entry_width=30, entry_font=search_font, entry_background=dark_color, entry_foreground=search_font_color, button_text="Search", button_ipadx=10, button_background=dark_color, button_foreground="white", button_font=None, opacity=0.8, placeholder=place_holder_text, placeholder_font=place_holder_font, placeholder_color=place_holder_color, spacing=3, command=None):
        tk.Frame.__init__(self, master, borderwidth=0, highlightthickness=0,background=entry_background)
        
        self._command = command

        self.entry = tk.Entry(self, width=entry_width, background=entry_background, highlightcolor=button_background, highlightthickness=0, foreground = entry_foreground,borderwidth=0)
        self.entry.place(x=0,y=0,relwidth=1,relheight=1)
        
        if entry_font:
            self.entry.configure(font=entry_font)

        if placeholder:
            add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=placeholder_font)

        self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())
        self.entry.bind("<Return>", self._on_execute_command)

        opacity = float(opacity)

        if button_background.startswith("#"):
            r,g,b = hex2rgb(button_background)
        else:
            # Color name
            r,g,b = master.winfo_rgb(button_background)

        r = int(opacity*r)
        g = int(opacity*g)
        b = int(opacity*b)

        if r <= 255 and g <= 255 and b <=255:
            self._button_activebackground = '#%02x%02x%02x' % (r,g,b)
        else:
            self._button_activebackground = '#%04x%04x%04x' % (r,g,b)

        self._button_background = button_background

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

    def _state_normal(self, event):
        self.button_label.configure(background=self._button_background)

    def _state_active(self, event):
        self.button_label.configure(background=self._button_activebackground)



#Automatic scrollbar on labels
class AutoScroll(object):
	def __init__(self, master):
		try:
			vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
		except:
			pass
		hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

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
		# 	methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
		# 		+ tk.Place.__dict__.keys()

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
		container = ttk.Frame(master)
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
	def __init__(self,parent,frame_borderwidth = 0,frame_highlightthickness = 1,background_color = dark_color):
		tk.Frame.__init__(self,parent, 
			background = background_color,
			highlightcolor = background_color,
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
			background = light_color, 
			activebackground = light_color,
			borderwidth = 0,
			highlightthickness = 0,
			image = image_object,
			command = command_name,
			)

#themed colum label
class columnlabel(tk.Label):
	def __init__(self,frame,label_text):
		tk.Label.__init__(self,frame,
			background = dark_color, 
			foreground = columnlabelcolor,
			borderwidth = 0,
			highlightthickness = 0,
			font = columnlabelfont,
			anchor = "w",
			text = label_text,
			)

#themed nav button
class navbutton(tk.Button):
	def __init__(self,frame,image_object,command_name):
		tk.Button.__init__(self,frame,
			background=light_color,
			borderwidth=0,
			activebackground=light_color,
			#pady="0",
			image=image_object,
			command=command_name,
			)

class navbox(themedframe):
	def __init__(self,frame,
		primary_button_image,
		primary_button_command,
		etc_button_image,
		etc_button_command,
		left_context_image,
		left_context_command,
		right_context_image,
		right_context_command,
		):
		themedframe.__init__(self,frame, background_color=light_color)

		#back to list button
		self.etc_button = navbutton(self, image_object=etc_button_image, command_name=etc_button_command)
		self.etc_button.place(relx=1, rely=0, x=-etc_button_image.width(), height=etc_button_image.height(), width=etc_button_image.width())

		#install_button
		self.primary_button = navbutton(self, image_object = primary_button_image, command_name = primary_button_command)
		self.primary_button.place(relx=0.00, rely=0, height=primary_button_image.height(), width=primary_button_image.width())

		#previous button in details menu
		self.left_context_button = navbutton(self, image_object = left_context_image, command_name = left_context_command)
		self.left_context_button.place(relx=0.00, rely=1,y=-left_context_image.height(),  height=left_context_image.height(), width=left_context_image.width())

		#next button in details menu
		self.right_context_button = navbutton(self, image_object=right_context_image, command_name=right_context_command)
		self.right_context_button.place(relx=1, rely=1, y=-right_context_image.height(), height=right_context_image.height(), x=-right_context_image.width(), width =right_context_image.width())




#themed author/ etc label
class themedlabel(tk.Label):
	def __init__(self,frame,label_text,label_font=smalltext,label_color=w,text_variable=None):
		tk.Label.__init__(self,frame,
			background = light_color,
			highlightthickness=0,
			anchor="n",
			text = label_text,
			font=label_font,
			foreground= label_color,
			textvariable = text_variable,
			)






class infobox(themedframe):
	def __init__(self,frame):
		themedframe.__init__(self,frame,background_color=light_color)

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
		self.project_title_label.place(relx=0.0, rely=0.0, y=infoframewidth-30, relwidth=1.0)


		#author name
		self.authorvar = tk.StringVar()
		self.authorvar.set("author_var")
		self.author_name_label = themedlabel(self,
			label_text = "author_name", 
			text_variable = self.authorvar, 
			label_color=info_author_color, 
			label_font=info_author_font
			)
		self.author_name_label.place(relx=0.0, rely=0, y=+infoframewidth, relwidth=1.0)


		#Description
		self.project_description = ScrolledText(self)
		self.project_description.place(relx=0.0, rely=0.0, y=+infoframewidth+30, relheight=1, height=-(infoframewidth+30+100), relwidth=.98)
		self.project_description.configure(background=light_color)
		self.project_description.configure(foreground=info_description_color)
		self.project_description.configure(font=info_description_font)
		self.project_description.configure(wrap="word")
		self.project_description.configure(state=NORMAL)
		self.project_description.delete('1.0', END)
		self.project_description.insert(END, "Project description")
		self.project_description.configure(state=DISABLED)
		self.project_description.configure(borderwidth=0)

	def updatetitle(self,title):
		self.titlevar.set(title)

	#update author information
	def updateauthor(self,author):
		self.authorvar.set("by {}".format(author))

	def updateimage(self,art_image):

		imagemax = infoframewidth
		while not (art_image.width() > (imagemax - 80) and not (art_image.width() > imagemax)):
			if art_image.width() > imagemax:
				art_image = art_image.subsample(2)
			if art_image.width() < (imagemax - 80):
				art_image = art_image.zoom(3)

		self.project_art_label.configure(image=art_image)
		self.project_art_label.image = art_image

	#update project description
	def updatedescription(self, desc):
		self.project_description.configure(state=NORMAL)
		self.project_description.delete('1.0', END)
		self.project_description.insert(END, desc)
		self.project_description.configure(state=DISABLED)

	#update all info in the info box
	def updateinfo(self, softwarechunknumber):

		self.updateAuthorImage()

		self.updatedescription(hbdict[softwarechunknumber]["description"])
