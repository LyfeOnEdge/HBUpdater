import modules.homebrewcore as homebrewcore
import json
import shutil

#archive handling
from zipfile import ZipFile

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
		print(headers)
		filename = headers["Content-Disposition"].split("filename=",1)[1]
		downloadlocation = homebrewcore.joinpaths(homebrewcore.downloadsfolder,filename)
		shutil.move(downloadedfile, downloadlocation)
		print("downloaded {} from url {}".format(filename, fileURL))
		return filename
	except Exception as e: 
		print(e)
		return None


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
	# print("Downloading software json files from github")
	for softwarechunk in dicttopopulate:
		githubjsonlink = softwarechunk["githubapi"]
		softwarename = softwarechunk["software"]
		jsonfile = homebrewcore.joinpaths(homebrewcore.jsoncachefolder, softwarename + ".json")

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
		print("using previously downloaded json file {}".format(jsonfile))

	dicttopopulate = sorted(dicttopopulate, key = lambda i: i["software"])
	return dicttopopulate

def getJson(softwarename, apiurl):
	try:
		jsonfile = homebrewcore.joinpaths(homebrewcore.jsoncachefolder, softwarename + ".json")
		urllib.request.urlretrieve(apiurl,jsonfile)
		print("Downloaded new json file for {}".format(softwarename))
		return jsonfile
	except:
		print("failed to download json file for {}".format(softwarename))
		return None









def parse_standard_github_to_api(url):
	remove = [
	"/pulls",
	"/releases",
	"/latest",
	"/issues",
	"/projects",
	"/wiki",
	"/pulse",
	]
	try:
		for item in remove:
			url = url.replace(item,"")
		base = "https://api.github.com/repos/"
		url = base + url.rsplit("https://github.com/",1)[1]
		url = url + "/releases"
		return(url)
	except:
		return None

def grabgravatar(url):
	downloadedfile = urllib.request.urlretrieve(url)[0]
	dljsonfile = url.rsplit("/",1)[1]
	downloadlocation = homebrewcore.joinpaths(homebrewcore.downloadsfolder,dljsonfile)
	shutil.move(downloadedfile, downloadlocation)
	with open(downloadlocation) as jsonfile:
		jfile = json.load(jsonfile)
		avatarurl = jfile["entry"][0]["thumbnailUrl"]
	return cacheimage(avatarurl,dljsonfile)





