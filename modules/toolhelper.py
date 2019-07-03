from modules.format import *
import modules.customwidgets as cw
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import modules.webhandler as webhandler
import json, os, shutil, subprocess, sys, threading
from zipfile import ZipFile

fluffylist = []

def getnut():
		downloadNUTandinstalldependencies()
		starthelper("nut")

def getfluffy():
	downloadFLUFFYandinstalldependencies()
	starthelper("fluffy")


def checkifhelperdownloaded(helper):
	if guicore.checkguisetting(helper, "version") == "not installed" or guicore.checkguisetting(helper, "version") == None:
		return False
	else:
		print(guicore.checkguisetting(helper, "version"))
		return True
	return False

def starthelper(helper):
	if not checkifhelperdownloaded(helper):
		nutnotdownloadedwarningframe.tkraise()
		print("not installed")
		return
	script_path = guicore.checkguisetting(helper, "location")
	print("starting {} server at {}".format(helper,script_path))
	if script_path == None:
		print("invalid path")
		return
	subprocess.Popen([sys.executable,script_path])

def downloadNUTandinstalldependencies():
	if not os.path.isdir(locations.nutfolder):
		os.mkdir(locations.nutfolder)
		print("initializing nut folder")

	nutjson = webhandler.getJson("nut", locations.nutserverdict["githubapi"])
	with open(nutjson, encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
		jfile = json.load(json_file)
		if jfile == [] or jfile == None:
			print("Error: empty json nut file")
			return

		zipurl = jfile[0]["zipball_url"]
		version = jfile[0]["tag_name"]
		if zipurl == None:
			print("zip file url invalid, can't download nut assets")

		nutzip = webhandler.download(zipurl)
		nutzip = os.path.join(locations.downloadsfolder, nutzip)

		with ZipFile(nutzip, 'r') as zipObj:
			zipObj.extractall(locations.nutfolder)
			print("Sucessfully extracted {} to nut folder\n".format(nutzip))

			extractedfiles = zipObj.namelist()

			serverfile = None
			for possibleserverfile in extractedfiles:
				if possibleserverfile == extractedfiles[0] + "server.py":
					serverfile = possibleserverfile
			if serverfile == None:
				print("Could not find server file in extracted files")
				return 

			serverfile = os.path.join(locations.nutfolder, serverfile)

		newentry = {
			"nut" : {
				"version": version,
				"location": serverfile,
			}
		}
		guicore.setguisetting(newentry)

	print("checking nut dependencies")

	dependencies = locations.nutserverdict["dependencies"]
	webhandler.installmodulelist(dependencies)

def downloadFLUFFYandinstalldependencies():
	if not os.path.isdir(locations.fluffyfolder):
		os.mkdir(locations.fluffyfolder)
		print("initializing fluffy folder")

	global fluffylist
	if fluffylist == []:
		fluffydict = locations.fluffydict
		fluffylist = [fluffydict]
		fluffylist = webhandler.getUpdatedSoftwareLinks(fluffylist)

	fluffyjson = fluffylist[0]["githubjson"]
	with open(fluffyjson, encoding="utf-8") as json_file: #jsonfile is path, json_file is file obj
		jfile = json.load(json_file)
		if jfile == [] or jfile == None:
			print("Error: empty json nut file")
			return

		version = jfile[0]["tag_name"]
		version = version.strip("v")
		if float(version) > 2.8:
			asset = 1
		else:
			asset = 0
		scripturl = jfile[0]["assets"][asset]["browser_download_url"]
		licenseurl = jfile[0]["assets"][asset+1]["browser_download_url"]
		

		#download and move fluffy and license
		script = webhandler.download(scripturl)
		license = webhandler.download(licenseurl)
		scriptpath = os.path.join(locations.downloadsfolder, script)
		licensepath = os.path.join(locations.downloadsfolder, license)
		newscriptpath = os.path.join(locations.fluffyfolder, script)
		newlicensepath = os.path.join(locations.fluffyfolder, license)
		shutil.move(scriptpath,newscriptpath)
		shutil.move(licensepath,newlicensepath)

		newentry = {
			"fluffy" : {
				"version": version,
				"location": newscriptpath,
			}
		}
		guicore.setguisetting(newentry)

	print("checking and installing fluffy dependencies")

	threads = []
	dependencies = locations.fluffydict["dependencies"]
	webhandler.installmodulelist(dependencies)



