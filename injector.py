import HBUpdater
from format import * 
import homebrewcore
import locations
import webhandler
from zipfile import ZipFile

import tkinter as tk
from tkinter.constants import *
import customwidgets as cw

import json

import sys,subprocess



def checkifpyusbinstalled():
	reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
	installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
	if "pyusb" in installed_packages:
		return True
	return False

#installs PyUSB on-demand for use with py
def installPyUSB():
    try:
    	print(subprocess.call([sys.executable, "-m", "pip", "install", "pyusb"]))
    	return(True)
    except:
    	print("Error installing pyUSB, do you have pip installed?")
    	return(False)


def injectpayload(payload,console):
	if HBUpdater.checkguitag("fusee-launcher", "version") == "not installed" or HBUpdater.checkguitag("fusee-launcher", "version") == "none":
		# console.print("fusee-launcher not installed, downloading")
		with open(HBUpdater.payloadinjector[0]["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
			jfile = json.load(json_file)
			downloadurl = jfile[0]["zipball_url"]
			file = webhandler.download(downloadurl)
			file = homebrewcore.joinpaths(homebrewcore.downloadsfolder, file)
			version = jfile[0]["tag_name"]
			with ZipFile(file, 'r') as zipObj:
				zipObj.extractall(homebrewcore.payloadsfolder)
				console.print("Sucessfully extracted {} to payloads folder".format(file))
				files = zipObj.namelist()
				injector = None
				for possiblepayloadfile in files:
					if possiblepayloadfile.startswith(files[0] + "fusee"):
						injector = possiblepayloadfile
				if injector == None:
					console.print("Could not find injector in extracted files")
					return 
			newentry = {
				"fusee-launcher" : {
					"version": version,
					"location": injector,
				}
			}
			HBUpdater.updateguilog(newentry)

	script_path = HBUpdater.checkguitag("fusee-launcher", "location")
	script_path = homebrewcore.joinpaths(homebrewcore.payloadsfolder, script_path)
	payload_file = payload
	p = subprocess.Popen([sys.executable, '-u', script_path, payload_file],
	          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
	with p.stdout:
	    for line in iter(p.stdout.readline, b''):
	    	print(line)
	p.wait()

