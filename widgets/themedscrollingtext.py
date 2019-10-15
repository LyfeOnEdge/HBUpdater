from .customwidgets import scrolledText
from style import *

class themedScrollingText(scrolledText):
	def __init__(self, text = ""):
		scrolledText.__init__(wrap = "word", font = mediumtext)
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

		self.abouttext.insert("1.0", abouttext)
		self.abouttext.configure(state="disabled")