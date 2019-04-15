version = "0.2 (BETA)"
print("HBUpdater version {}".format(version))

#file handling
import os, sys, shutil
from zipfile import ZipFile
import json


#stop script if running without a frontend
if __name__ == '__main__':
	sys.exit("This file was not meant to run without a frontend. Exiting...")

#My modules
import webhandler 
import homebrewcore
import locations
from format import *
import webhandler

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
	chosensdpath = sdpath
	trackingfolder = homebrewcore.joinpaths(chosensdpath, homebrewcore.trackingfolder)
	if not homebrewcore.direxist(trackingfolder):
		os.mkdir(trackingfolder)

	trackingfile = homebrewcore.joinpaths(trackingfolder, homebrewcore.trackingfile)
	if not homebrewcore.exists(trackingfile):
		with open(trackingfile, "w+") as jfile:
			json.dump({}, jfile, indent=4,)


	print("SD path set to: {}".format(str(chosensdpath)))

	if not(str(chosensdpath) == ""):
		print("sd path set")
		sdpathset = True
	else:
		print("invalid path chosen")
		sdpathset = False

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

	if filename.endswith(".nro"):
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
					namelist.append(homebrewcore.joinpaths(chosensdpath,location))
				print("files copied: \n {}".format(namelist))
				return namelist
	else:
		print("file handling method not found")
		return None

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


#not used yet
# #checks if PyUSB is installed (required for the injector)
# def checkifpyusbinstalled():
# 	reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
# 	installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
# 	if "pyusb" in installed_packages:
# 		return True
# 	return False

# #installs PyUSB on-demand for use with py
# def installPyUSB():
#     try:
#     	print(subprocess.call([sys.executable, "-m", "pip", "install", "pyusb"]))
#     except:
#     	print("Error installing pyUSB, do you have pip installed?")


# def injectpayload():
# 	#check if pyusb installed, if not ask if user wants to install it
# 	if not checkifpyusbinstalled():
# 		installpyusb = tkinter.messagebox.askyesno("Install PyUSB?", "PyUSB is required for fusee-launcher to work, install?")
# 		if installpyusb == True:
# 			spewToTextOutput("Got answer: yes")
# 			spewToTextOutput("Installing PyUSB.")
# 			installPyUSB()
# 			pyusbinstalled = True

# 	#check again to see if installed
# 	if checkifpyusbinstalled():
# 		# payloadtoinject = payloadlistbox.curselection()
# 		if payloadVar == None:
# 			spewToTextOutput("No payload selected")
# 			return

# 		payloadtoinject = payloadVar.get()
# 		print("injecting {}".format(payloadtoinject))
# 		downloadfileas = ""
# 		for softwarechunk in payloads:
# 			if softwarechunk["software"] == payloadtoinject:
# 				fileurl = softwarechunk["directlink"]
# 				filename = fileurl.rsplit('/', 1)[-1]
# 				downloadFile(filename, fileurl)	#regardless of zip format we need to start by downloading the file
# 				if not softwarechunk["itemslist"] == None: #IF WE HAVE SPECIFIED AN ITEM TO EXTRACT, IT'S A ZIP
# 					downloadedfilename = os.path.join(get_path(downloadsfolder), filename)
# 					print("File exists: {}".format(exists(downloadedfilename)))
# 					with ZipFile(downloadedfilename, 'r') as zipObj:
# 						# try:
# 							zipObj.extractall(get_path(downloadsfolder))
# 							filename = os.path.join(get_path(downloadsfolder), softwarechunk["itemslist"]["payload"])
# 						# except:
# 						# 	spewToTextOutput("Failed to unzip or copy files")	
# 						# 	return
# 				else:
# 					filename = get_path(os.path.join(downloadsfolder, filename))



# 		spewToTextOutput("Injecting payload {}".format(filename))

# 		fusee_file = os.path.join(fusee_path, "fusee-launcher.py")
# 		script_path = get_path(fusee_file)
# 		payload_path = filename
# 		print("injecting path {}".format(payload_path))
# 		p = subprocess.Popen([sys.executable, '-u', script_path, payload_path],
# 		          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
# 		with p.stdout:
# 		    for line in iter(p.stdout.readline, b''):
# 		        spewBytesToTextOutput(line)
# 		p.wait()
