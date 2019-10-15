#!/usr/bin/env python
version = "2.0"
print("HBUpdater version %s" % version)

import os, sys, platform, json, threading
from timeit import default_timer as timer
#print version, exit if minimum version requirements aren't met
print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6: #Trying to import tkinter in the new syntax after python 2 causes a crash
	sys.exit("Python 3.6 or greater is required to run this program.")

#This is called before the below module imports to ensure no exception is encountered trying to import tk
try:
	import tkinter as tk
except:
	input("Cannot start: Tkinter not installed, consult the readme for more information.")
	sys.exit()

#This is called before the below module imports to ensure no exception is encountered trying to import pil
try:
	import PIL #Import pillow library
except:
	input("Cannot start: Pillow module not installed, try `pip install Pillow` or consult the readme for more information.")
	sys.exit()

print("Using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))

#Import local modules
from customwidgets import frameManager
from appstore import getPackageIcon, appstore_handler
from HBUpdater import parser, HBUpdater_handler
from webhandler import getJson
from modules.locations import update_url
from asyncthreader import asyncThreader
from github_updater import updater
from widgets import icon_dict
from pages import pagelist
from fusee_wrapper import fusee_object as injector

print("Checking for updates...")
if updater.check_for_update(version):
	print("Update detected.")
else:
	print("Up to date.")

#Async threader tool for getting downloads and other functions asyncronously
threader = asyncThreader()

toolsfolder = os.path.join(sys.path[0], "tools")
if not os.path.isdir(toolsfolder):
	print("Initing tools folder")
	os.mkdir(toolsfolder)
#Tool to manage local packages (downloaded payloads, etc)
local_packages_handler = HBUpdater_handler("GENERIC")
local_packages_handler.set_path(toolsfolder, silent = True)
#Init tracking file for local packages as needed
if not local_packages_handler.check_if_get_init():
	local_packages_handler.init_get()

print("Getting updated HBUpdater repo file")
repos_github_api = getJson("repos_api","https://api.github.com/repos/LyfeOnEdge/HBUpdater_API/releases")
with open(repos_github_api, encoding = "utf-8") as package_repos:
	repo = json.load(package_repos)
	assets = repo[0]["assets"]
#Borrow HBUpdater findasset function 
repo_remote = local_packages_handler.findasset([["repos"], "json"], assets, silent = True)
packages_json = getJson("repos",repo_remote)

#Parse the json into categories
repo_parser = parser()
repo_parser.blacklist_categories(["payloads"])
threader.do_async(repo_parser.load, [packages_json], priority = "high")
#Shared tool for installing and managing hbas apps via the switchbru site on the sd card
store_handler = HBUpdater_handler("SWITCH")

image_sharer = icon_dict()

rcminjector = injector(print_function = print)

geometry = {
	"width" : 780,
	"height" : 575
}

def startGUI():
	#frameManager serves to load all pages and stack them on top of each other (all 2 of them)
	#also serves to make many important objects and functions easily available to children frames
	gui = frameManager(pagelist,
		geometry,
		local_packages_handler,
		store_handler,
		repo_parser,
		threader,
		image_sharer,
		updater,
		rcminjector,
		)

	#Set title formattedwith version
	gui.title("HBUpdater %s" % version)

	#Set icon
	favicon = None
	if platform.system() == 'Windows':
		print("Windows detected, setting icon")
	elif platform.system() == "Linux":
		print("Linux detected, setting icon")
		favicon = os.path.join("assets", 'favicon.xbm')
	elif platform.system() == "Darwin":
		print("Mac detected, not setting icon as it is not supported")

	if favicon:
		if os.path.exists(favicon):
			#Set icon
			gui.iconbitmap(favicon)
		else:
			print("Icon file not found, not setting favicon")

	gui.mainloop()

if __name__ == '__main__':
	startGUI()