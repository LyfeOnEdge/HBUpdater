#!/usr/bin/python3
# -*- coding: utf-8 -*-
version = "2.4"
print("HBUpdater version %s" % version)

import os, sys, platform, json, threading, argparse
from timeit import default_timer as timer
#print version, exit if minimum version requirements aren't met
print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6: #Trying to import tkinter in the new syntax after python 2 causes a crash
	sys.exit("Python 3.6 or greater is required to run this program.")

#This is called before the below module imports to ensure no exception is encountered trying to import tk
try:
	import tkinter as tk
	print("Using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))
except:
	input("Cannot start: Tkinter not installed, consult the readme for more information. Press enter to exit program.") #Input is called to prevent the cli from closing until the user has seen the message 
	sys.exit()

try:
	TKVERSION = float(tk.Tcl().eval('info patchlevel')[0:3])
except Exception as e:
	TKVERSION = 0
	print("Failed to get tkinter version ~ {}".format(e))
print(TKVERSION)

#This is called before the below module imports to ensure no exception is encountered trying to import pil
try:
	import PIL #Import pillow library
except:
	input("Cannot start: Pillow module not installed, try `pip install Pillow` or consult the readme for more information. Press enter to exit program.")
	sys.exit()

#Import local modules
from customwidgets import frameManager
from appstore import getPackageIcon
from HBUpdater import repo_parser, store_handler, local_packages_handler
from webhandler import getJson, getCachedJson
from locations import update_url
from asyncthreader import threader
from github_updater import updater
from pages import pagelist
from fusee_wrapper import injector
from settings_tool import settings
import style

print("Checking for updates...")
if updater.check_for_update(version):
	print("Update detected.")
else:
	print("Up to date.")

#Async threader tool for getting downloads and other functions asyncronously
threader.set_max_threads(int(settings.get_setting("gui_threads")))

def create_arg_parser():
	parser = argparse.ArgumentParser(description='pass a repo.json to load a local one instead of one downloaded from github')
	parser.add_argument('repo',
					help='repo.json path')
	return parser

parsed_args = None
if len(sys.argv) > 1:
	arg_parser = create_arg_parser()
	parsed_args = arg_parser.parse_args(sys.argv[1:])

toolsfolder = os.path.join(sys.path[0], "tools")
if not os.path.isdir(toolsfolder):
	print("Initing tools folder")
	os.mkdir(toolsfolder)
#Tool to manage local packages (downloaded payloads, etc)
local_packages_handler.set_path(toolsfolder, silent = True)
#Init tracking file for local packages as needed
if not local_packages_handler.check_if_get_init():
	local_packages_handler.init_get()

if not parsed_args:
	print("Getting updated HBUpdater api file")
	repos_github_api = getJson("repos_api","https://api.github.com/repos/LyfeOnEdge/HBUpdater_API/releases")
	if repos_github_api:
		with open(repos_github_api, encoding = "utf-8") as package_repos:
			repo = json.load(package_repos)
			assets = repo[0]["assets"]
		#Borrow HBUpdater findasset function 
		repo_remote = local_packages_handler.findasset([["repo"], "json"], assets, silent = True)
		print("Getting updated HBUpdater repo file")
		packages_json = getJson("repos",repo_remote)
	else:
		print("Failed to download packages json repo file, falling back on old version")
		packages_json = os.path.join(sys.path[0], "cache/json/repos.json")
else:
	if parsed_args.repo.lower() == "test":
		print("Using local json")
		packages_json = getCachedJson("repos")
	else:
		print("Using passed repo json {}".format(parsed_args.repo))
		packages_json = parsed_args.repo

#Parse the json into categories
repo_parser.blacklist_categories(["payloads"])
threader.do_async(repo_parser.load, [packages_json], priority = "high")
#Shared tool for installing and managing hbas apps via the switchbru site on the sd card


def startGUI(args = None):
	#frameManager serves to load all pages and stack them on top of each other (all 2 of them)
	#also serves to make many important objects and functions easily available to children frames
	gui = frameManager(pagelist,
		args
		)

	#Set title formatted with version
	version_string = "HBUpdater %s" % version
	gui.set_version(version_string)
	gui.title(version_string)
	#Wheteher to keep window topmost
	gui.attributes("-topmost", True if settings.get_setting("keep_topmost") == "true" else False)

	maximized_options = {
		"fullscreen" : "-fullscreen",
		"maximized" : "-zoomed",
		"windowed" : None
	}
	if maximized_options[settings.get_setting("maximized")]:
		opt = maximized_options[settings.get_setting("maximized")]

		if platform.system() == 'Windows':
			try:
				gui.state(opt.strip("-"))
			except Exception as e:
				print("Error setting window launch type for windows, this is a bug please report it:\n     {}".format(e))
		else:
			gui.attributes(opt, True)

	#Set icon
	favicon = None
	if platform.system() in ['Windows', 'Linux']:
		print("{} detected, setting icon".format(platform.system()))
		favicon = 'assets/favicon.png'
	elif platform.system() == "Darwin":
		print("MacOS detected, not setting icon as it is not supported")

	if favicon:
		if os.path.exists(favicon):
			#Set icon
			gui.tk.call('wm', 'iconphoto', gui._w, tk.PhotoImage(file=favicon))
		else:
			print("Icon file not found, not setting favicon")

	if (True if settings.get_setting("borderless") == "true" else False):
		if platform.system() in ['Windows']:
			gui.overrideredirect(1)
		else:
			try:
				if TKVERSION > 8.5:
					if gui.tk.call('tk','windowingsystem') == "x11":
						gui.wm_attributes('-type', 'splash')
			except:
				print("Failed to set window type to borderless")

	gui.mainloop()

if __name__ == '__main__':
	startGUI(parsed_args)