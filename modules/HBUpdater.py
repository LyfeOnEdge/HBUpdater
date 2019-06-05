#file handling
import os, sys, shutil
from zipfile import ZipFile
import json

#stop script if running without a frontend
if __name__ == '__main__':
	sys.exit("This script was not meant to run without a frontend. Exiting...")

version = "0.9 (Beta)"
print("HBUpdater version {}".format(version))

#My modules
from modules.format import *
import modules.locations as locations
import modules.webhandler as webhandler

chosensdpath = None
sdpathset = False

#folders and files for tracking installed apps on the sd
trackingfolder = ""
trackingfile = ""



#update global "chosensdpath"
def setSDpath(sdpath):
	global chosensdpath
	global trackingfoldername
	global trackingfolder
	global trackingfilename
	global trackingfile
	global sdpathset
	if not(str(sdpath) == ""):
		chosensdpath = sdpath
		print("SD path set to: {}".format(str(chosensdpath)))
		sdpathset = True

		trackingfolder = os.path.join(chosensdpath, locations.trackingfolder)
		if not os.path.isdir(trackingfolder):
			os.mkdir(trackingfolder)
		trackingfile = os.path.join(trackingfolder, locations.trackingfile)
		if not os.path.isfile(trackingfile):
			with open(trackingfile, "w+") as jfile:
				initdata = {}
				initdata["created_with"] = version
				initdata["cfw"] = "not installed"
				json.dump(initdata, jfile, indent=4,)

	else:
		print("invalid path chosen")
		sdpathset = False

	print("sdpathset = {}".format(sdpathset))






def installitem(dicty, option, suboption, group):
	print("\n")
	softwarename = dicty[option]["software"]

	location = getlogvalue(group, softwarename, "location")

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
				if os.path.isfile(loc):
					os.remove(loc)
					print("removed old file {}".format(loc))
		elif type(location) is str:
			if os.path.isfile(location):
				os.remove(location)
				print("removed {}".format(location))

		installlocation = installfiletosd(downloadedfile, dicty[option]["install_subfolder"])
		
		if not (installlocation) == None:
			newentry = {
				"software": dicty[option]["software"],
				"version": tag,
				"location": installlocation,
			}
			updatelog(group, newentry)

def installfiletosd(filename,subfolder):
	global chosensdpath

	file = os.path.join(locations.downloadsfolder, filename)

	if not subfolder == None:
		subdir = os.path.join(chosensdpath,subfolder)
	else: 
		subdir = chosensdpath

	sdlocation = os.path.join(subdir, filename)

	if not os.path.isdir(subdir):
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
					namelist.append(os.path.join(subdir,location))
				print("files copied: \n {}".format(namelist))
				print(subdir)
				return namelist
	else:
		print("file handling method not found")
		return None


def uninstallsoftware(group, softwarename):
	if not sdpathset:
		print("SD path not set, can't uninstall")
		return
	if getlogstatus(group,softwarename) == "not installed":
		print("Not installed.")
		return


	filestoremove = getlogvalue(group, softwarename,"location")
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
				"software": softwarename,
				"version": "not installed",
				"location": None,
			}

	updatelog(group, newentry)
	print("uninstalled {}".format(softwarename))





def updatelog(group, newentry):
	if not os.path.isdir(trackingfolder):
		os.mkdir(trackingfolder)

	#create log is it doesn't exist
	if os.path.isfile(trackingfile):
		pass
		# print("Found Tracking File")
	else:
		open(trackingfile, "w")

	#open log
	with open(trackingfile, 'r') as json_file:  
		originaljfile = json.load(json_file)

	# print(json.dumps(originaljfile,indent=4))
	#update value
	try:
		groupdict = originaljfile[group]
		if groupdict == "not installed":
			groupdict = {}
	except:
		groupdict = {}

	location = newentry["location"]

	entry = {	
		"version" : newentry["version"],
		"location" : location
	}

	softwarename = newentry["software"]
	groupdict[softwarename] = entry

	originaljfile[group] = groupdict

	#write updated log
	with open(trackingfile, 'w') as newjfile:
		json.dump(originaljfile, newjfile, indent=4,)

def getlogvalue(group, software, keyword):
	try:
		with open(trackingfile, 'r') as json_file:  
			jfile = json.load(json_file)

		try:
			status = jfile[group][software][keyword]
		except:
			status = None
	except:
		status = None

	return status


def getlogstatus(group, software):
	return getlogvalue(group, software, "version")



