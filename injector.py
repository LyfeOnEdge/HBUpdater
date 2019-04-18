import HBUpdater
from format import * 
import homebrewcore

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


def injectpayload(payload):

		print("Injecting payload {}".format(payload))

		fusee_file = homebrewcore.joinpaths(fusee_path, "fusee-launcher.py")
		script_path = homebrewcore.get_path(fusee_file)
		payload_file = payload
		print("injecting payload {}".format(payload_file))
		p = subprocess.Popen([sys.executable, '-u', script_path, payload_file],
		          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
		with p.stdout:
		    for line in iter(p.stdout.readline, b''):
		        spewBytesToTextOutput(line)
		p.wait()

