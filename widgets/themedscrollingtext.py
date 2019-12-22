from .customwidgets import scrolledText
from style import *

class themedScrollingText(scrolledText):
	def __init__(self, frame, text = "", font = mediumtext):
		scrolledText.__init__(self, frame, wrap = "word", font = font)
		self.set(text)

	def clear(self):
		self.configure(state="normal")
		self.delete('1.0', "end")
		self.configure(state="disabled")

	def set(self, string):
		self.configure(state="normal")
		self.delete('1.0', "end")
		self.insert("1.0", string)
		self.configure(state="disabled")