import os, sys, shutil
import locations
from .etags import accessETaggedFile

#web handling
import urllib.request 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

#Variable to map previously downloaded jsons to minimize repeated downloads
filedict = {}

#opens a url in a new tab
def opentab(url):
	import webbrowser
	webbrowser.open_new_tab(url)

#Download a file at a url, returns file path
def download(fileURL):
	try:
		downloadedfile, headers = urllib.request.urlretrieve(fileURL)
		print(headers)
		filename = headers["Content-Disposition"].split("filename=",1)[1]
		downloadlocation = os.path.join(locations.downloadsfolder,filename)
		shutil.move(downloadedfile, downloadlocation)
		print("downloaded {} from url {}".format(filename, fileURL))
		return filename
	except Exception as e: 
		print(e)
		return None

def getJson(softwarename, apiurl):
	try:
		jsonfile = os.path.join(locations.jsoncachefolder, softwarename + ".json")
		jfile = accessETaggedFile(apiurl,jsonfile)
		return jfile
	except:
		print("failed to download json file for {}".format(softwarename))
		return None

def getCachedJson(softwarename):
	return os.path.join(locations.jsoncachefolder, softwarename + ".json")
