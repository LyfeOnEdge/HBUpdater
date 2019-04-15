import homebrewcore
import json
import shutil

#archive handling
from zipfile import ZipFile
import tarfile

import urllib.request 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

#Download a file as a specfic name, returns true if successful
def downloadFile(fileURL, filename): #Download 
	try:
		urllib.request.urlretrieve(fileURL, filename)
		print("Downloaded {} as {}".format(fileURL,filename))
		return True #Return true if download is successful
	except:
		print("Failed to download {}".format(filename))
		return False

def download(fileURL):
	try: 
		downloadedfile, headers = urllib.request.urlretrieve(fileURL)
		filename = headers["Content-Disposition"].split("filename=",1)[1]
		downloadlocation = homebrewcore.joinpaths(homebrewcore.downloadsfolder,filename)
		shutil.move(downloadedfile, downloadlocation)
		print("downloaded {} from url {}".format(filename, fileURL))
		return filename
	except: 
		return None


#Will properly download files now
def cacheimage(url,softwarename):
	try:
		with urllib.request.urlopen(url) as response:
			info = response.info()
			type=info.get_content_subtype()
			file = "{}.{}".format(softwarename,type)
			file = homebrewcore.joinpaths(homebrewcore.imagecachefolder,file)
			imagefile = open(file, 'wb')
			shutil.copyfileobj(response, imagefile)
			print("downloaded image {}".format(file))
	except: 
		print("failed to download file {} from url {}".format(file, url))
		return None
	return file






def getUpdatedSoftwareLinks(dicttopopulate):
	for softwarechunk in dicttopopulate:
		githubjsonlink = softwarechunk["githubapi"]
		softwarename = softwarechunk["software"]

		jsonfile = homebrewcore.joinpaths(homebrewcore.jsoncachefolder, softwarename + ".json")

		print("Downloading software json files from github")
		try:
			urllib.request.urlretrieve(githubjsonlink,jsonfile)
			print("Successfully downloaded {} to {}".format(githubjsonlink, jsonfile))
			softwarechunk["githubjson"] = jsonfile

		except:
			if homebrewcore.exists(jsonfile):
				print("could not get updated link, falling back on older version")
				softwarechunk["githubjson"] = jsonfile
			else:
				print("No fallback available, software will be unavailable")

	dicttopopulate = sorted(dicttopopulate, key = lambda i: i["software"])
	return dicttopopulate

def getJsonSoftwareLinks(dicttopopulate):
	for softwarechunk in dicttopopulate:
		githubjsonlink = softwarechunk["githubapi"]
		softwarename = softwarechunk["software"]

		jsonfile = homebrewcore.joinpaths(homebrewcore.jsoncachefolder, softwarename + ".json")
		softwarechunk["githubjson"] = jsonfile
		print("using downloaded json file {}".format(jsonfile))



	dicttopopulate = sorted(dicttopopulate, key = lambda i: i["software"])
	return dicttopopulate

def getMissingJson(dicttopopulate):
	for softwarechunk in dicttopopulate:
		githubjsonlink = softwarechunk["githubapi"]
		softwarename = softwarechunk["software"]

		jsonfile = homebrewcore.joinpaths(homebrewcore.jsoncachefolder, softwarename + ".json")

		if not homebrewcore.exists(jsonfile):
			try:
				urllib.request.urlretrieve(githubjsonlink,jsonfile)
				print("Successfully downloaded {} to {}".format(githubjsonlink, jsonfile))
				softwarechunk["githubjson"] = jsonfile

			except:
				print("failed to download json for missing file {}".format(jsonfile))
		else:
			print("using pre-downloaded json")


	dicttopopulate = sorted(dicttopopulate, key = lambda i: i["software"])
	return dicttopopulate









