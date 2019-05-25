#file handling
import os, sys, shutil
from zipfile import ZipFile
import json

#stop script if running without a frontend
if __name__ == '__main__':
	sys.exit("This script was not meant to run without a frontend. Exiting...")

version = "0.6 (BETA)"
print("HBUpdater version {}".format(version))

#My modules
from modules.format import *
import modules.homebrewcore as homebrewcore
import modules.locations as locations
import modules.webhandler as webhandler

chosensdpath = None
sdpathset = False
trackingfolder = ""
trackingfile = ""


#update global "chosensdpath"
def setSDpath(sdpath):
	global chosensdpath
	global trackingfolder
	global trackingfile
	global sdpathset
	if not(str(sdpath) == ""):
		chosensdpath = sdpath
		print("SD path set to: {}".format(str(chosensdpath)))
		sdpathset = True

		trackingfolder = homebrewcore.joinpaths(chosensdpath, homebrewcore.trackingfolder)
		if not homebrewcore.direxist(trackingfolder):
			os.mkdir(trackingfolder)
		trackingfile = homebrewcore.joinpaths(trackingfolder, homebrewcore.trackingfile)
		if not homebrewcore.exists(trackingfile):
			with open(trackingfile, "w+") as jfile:
				initdata = {}
				initdata["created_with"] = version
				json.dump(initdata, jfile, indent=4,)

	else:
		print("invalid path chosen")
		sdpathset = False

	print("sdpathset = {}".format(sdpathset))

def installitem(dicty, option, suboption):
	print("\n")
	softwarename = dicty[option]["software"]

	location = getlogitem(softwarename, "location")

	with open(dicty[option]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
		jfile = json.load(json_file)	
		asset = dicty[option]["github_asset"] 
		if asset == None:
			asset = 0
		downloadlink = jfile[suboption]["assets"][asset]["browser_download_url"]

		tag = jfile[suboption]["tag_name"]
	print("installing {} version {}".format(softwarename,tag))
	downloadedfile = webhandler.download(downloadlink)

	if not downloadedfile == None:

		if type(location) is list:
			for loc in location:
				if homebrewcore.exists(loc):
					os.remove(loc)
					print("removed old file {}".format(loc))
		elif type(location) is str:
			if homebrewcore.exists(location):
				os.remove(location)
				print("removed {}".format(location))

		installlocation = installfiletosd(downloadedfile, dicty[option]["install_subfolder"])
		
		if not (installlocation) == None:
			newentry = {
				dicty[option]["software"] : {
					"version": tag,
					"location": installlocation,
				}
			}
			updatelog(newentry)

def installfiletosd(filename,subfolder):
	global chosensdpath

	file = homebrewcore.joinpaths(homebrewcore.downloadsfolder, filename)

	if not subfolder == None:
		subdir = homebrewcore.joinpaths(chosensdpath,subfolder)
	else: 
		subdir = chosensdpath

	sdlocation = homebrewcore.joinpaths(subdir, filename)

	if not homebrewcore.direxist(subdir):
		os.mkdir(subdir)

	if filename.endswith(".nro") or filename.endswith(".py"):
		try:
			shutil.move(file, sdlocation)
			print("Successfully copied {} to SD".format(filename))
			return sdlocation
		except: 
		 	print("Failed to copy {} to SD".format(filename) )
		 	return None

	elif filename.endswith(".zip"):
		with ZipFile(file, 'r') as zipObj:
			# try:
				zipObj.extractall(subdir)
				print("Sucessfully extracted {} to SD".format(filename))
				sdlocation = zipObj.namelist()
				namelist = []
				for location in sdlocation:
					namelist.append(homebrewcore.joinpaths(subdir,location))
				print("files copied: \n {}".format(namelist))
				print(subdir)
				return namelist
	else:
		print("file handling method not found")
		return None


def uninstallsoftware(softwarename):
	if not sdpathset:
		print("SD path not set, can't uninstall")
		return
	if checkversion(softwarename) == "not installed":
		print("Not installed.")
		return


	filestoremove = getlogitem(softwarename,"location")
	print("removing {}".format(filestoremove))
	if 'str' in str(type(filestoremove)):
		os.remove(filestoremove)
		print("removed {}".format(filestoremove))
	else:
		for path in filestoremove: 
			if os.path.isfile(path):  
			    os.remove(path)
			    print("removed {}".format(path))
		# for file in filestoremove:
		# 	if os.path.isdir(file):
		# 		shutil.rmtree(file)
		# 		print("removed folder {}".format(file))

	newentry = {
				softwarename : {
					"version": "not installed",
					"location": None,
				}
			}
	updatelog(newentry)
	print("uninstalled {}".format(softwarename))



def updatelog(newentry):
	if not homebrewcore.direxist(trackingfolder):
		os.mkdir(trackingfolder)

	#create log is it doesn't exist
	if homebrewcore.exists(trackingfile):
		pass
		# print("Found Tracking File")
	else:
		open(trackingfile, "w")

	#open log
	with open(trackingfile, 'r') as json_file:  
		originaljfile = json.load(json_file)

	#update value
	originaljfile.update(newentry)

	#write updated log
	with open(trackingfile, 'w') as jfile:
		json.dump(originaljfile, jfile, indent=4,)

def getlogitem(software, key):
	try:
		with open(trackingfile, 'r') as json_file:  
			jfile = json.load(json_file)

		try:
			info = jfile[software][key]
		except:
			info = None
	except:
		info = None

	return info

def checkversion(software):
	try:
		with open(trackingfile, 'r') as json_file:
			jfile = json.load(json_file)
			# print(software)
			if software in jfile.keys():
				version = jfile[software]["version"]
				return version
			else:
				return "not installed"
	except:
		return "not installed"



