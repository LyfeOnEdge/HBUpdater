import os, sys, platform

print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    sys.exit("Python 3.6 or greater is required to run this program.")

version = "0.2 (BETA)"
print("HBUpdaterGUI version {}".format(version))

#My modules
import webhandler 
import homebrewcore
import locations
from format import *
import customwidgets as cw

#Backend will not rin standalone
import HBUpdater


import tkinter as tk
from tkinter.constants import *
# import tkinter.font as tkFont
# import tkinter.ttk as ttk
print("using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))
py3 = True


#import pages for appManager (Needs to be done after dict is populated)
import injectorpage as ip
import mainpage as mp
import settingspage as sp
#Main frame handler, raises and lowers pages in z layer
class FrameManager(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		if platform.system() == 'Windows':
			print("Windows detected, setting icon")
			self.iconbitmap(homebrewcore.joinpaths(homebrewcore.assetfolder, 'HBUpdater.ico'))

		# self.resizable(False,False)
		self.geometry("790x510")   #startup size 720p
		self.minsize(width=790, height=510) #minimum size currently supported
		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		container.configure(borderwidth = 0)
		container.configure(highlightthickness = 0)


		self.frames = {}
		for F in (mp.mainPage,ip.injectorScreen,sp.settingsPage):
			page_name = F.__name__
			frame = F(parent=container, controller=self, back_command = lambda: self.controller.show_frame("mainPage"))
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("mainPage") #Show the main page frame

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()



def UseCachedJson():
	HBUpdater.setDict(webhandler.getJsonSoftwareLinks(locations.softwarelist)) #Get software links from pre-downloaded jsons (TESTING FUNCTION, IF YOU GET AN ERROR FROM THIS LINE BECUASE I FORGOT TO COMMENT IT ON A COMMIT JUST COMMENT THIS LINE AND UNCOMMENT THE ONE BEFORE)
	HBUpdater.setIJDict(webhandler.getJsonSoftwareLinks(locations.payloadlist))

def GetUpdatedJson():
	HBUpdater.setDict(webhandler.getUpdatedSoftwareLinks(locations.softwarelist)) #Get fresh software links, falls back on old ones if they don't exist
	HBUpdater.setIJDict(webhandler.getUpdatedSoftwareLinks(locations.payloadlist))

if __name__ == '__main__':  
	#UseCachedJson()
	GetUpdatedJson()
	#HBUpdater.setDict(webhandler.getMissingJson(locations.softwarelist)) 
	
	for softwarechunk in HBUpdater.hbdict:
		softwarechunk["photopath"] = None

	gui = FrameManager()
	gui.title("HBUpdater")
	gui.mainloop()



# #launch with a passed software list
# def startGui(dicty):
#     setDict(HBUpdater.software)
#     gui = appManagerGui()
#     gui.mainloop()
