from style import *
import tkinter as tk

class searchBox(tk.Frame):
    def __init__(self, frame, entry_width=30, 
        entry_font=mediumboldtext, 
        entry_background=w, 
        entry_foreground=b,
        placeholder="Search", 
        placeholder_font=mediumboldtext, 
        placeholder_color=lg,
        command=None,
        command_on_keystroke = True,
        borderwidth = 2
        ):

        tk.Frame.__init__(self, frame, borderwidth=0, highlightthickness=0,background=entry_background)

        self._command = command

        self.entry = tk.Entry(self,
            width=entry_width,
            background=entry_background,
            highlightcolor=b, highlightthickness=0,
            foreground = entry_foreground,
            borderwidth=borderwidth,
            relief = tk.constants.RIDGE)
        self.entry.place(x=0,y=0,relwidth=1,relheight=1)
        
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

        entry.delete(0, tk.constants.END)
        entry.insert(0, text)
        
    def clear(self):
        self.entry_var.set("")
        
    def focus(self):
        self.entry.focus()

    def _on_execute_command(self, event):
        text = self.get_text()
        if self._command:
            self._command(text)

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