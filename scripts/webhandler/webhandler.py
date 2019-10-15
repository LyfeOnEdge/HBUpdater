import os, sys, shutil
from .etags import accessETaggedFile

#web handling
import urllib.request 

#Variable to map previously downloaded jsons to minimize repeated downloads
filedict = {}

def start(header):
	opener = urllib.request.build_opener()
	opener.addheaders = [header, ('User-agent', 'Mozilla/5.0')]
	urllib.request.install_opener(opener)

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
		downloadlocation = os.path.join("downloads",filename)
		shutil.move(downloadedfile, downloadlocation)
		print("downloaded {} from url {}".format(filename, fileURL))
		return filename
	except Exception as e: 
		print(e)
		return None

def getJson(softwarename, apiurl):
	try:
		jsonfile = os.path.join("downloads", softwarename + ".json")
		jfile = accessETaggedFile(apiurl,jsonfile)
		return jfile
	except Exception as e:
		print("failed to download json file for {} - {}".format(softwarename, e))
		return None