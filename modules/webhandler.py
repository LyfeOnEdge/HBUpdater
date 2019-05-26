import modules.homebrewcore as homebrewcore
import threading, sys, imp, shutil, json, subprocess

#archive handling
from zipfile import ZipFile

#web handling
import webbrowser
import urllib.request 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

def opentab(url):
	webbrowser.open_new_tab(url)

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

		getJsonThread(softwarename, githubjsonlink, jsonfile, softwarechunk)

	dicttopopulate = sorted(dicttopopulate, key = lambda i: i["software"])
	return dicttopopulate

def getJsonThread(softwarename, apiurl, jsonfile, softwarechunk):
	try:
		urllib.request.urlretrieve(apiurl,jsonfile)
		print("Downloaded new json file for {}".format(softwarename))
		softwarechunk["githubjson"] = jsonfile
		return jsonfile
	except:
		if homebrewcore.exists(jsonfile):
				print("could not get updated link, falling back on older version")
				softwarechunk["githubjson"] = jsonfile
		else:
			print("No fallback available, software will be unavailable")




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
	imagename = dljsonfile.rsplit(".",1)[0]
	downloadlocation = homebrewcore.joinpaths(homebrewcore.downloadsfolder,dljsonfile)
	shutil.move(downloadedfile, downloadlocation)
	with open(downloadlocation) as jsonfile:
		jfile = json.load(jsonfile)
		avatarurl = jfile["entry"][0]["thumbnailUrl"]
	return cacheimage(avatarurl,imagename)

def getcachedimage(imagename):
		photopath = imagename + ".png"
		photopath = homebrewcore.joinpaths(homebrewcore.imagecachefolder, photopath)
		photoexists = homebrewcore.exists(photopath)
		if photoexists:
			return photopath
		else:
			return False

def installpipmodule(module):
    try:
        print("installing {} via pip".format(module))
        print(subprocess.call([sys.executable, "-m", "pip", "install", module]))
        return(True)
    except:
        print("Error installing module")
        return(False)
   
def checkifmoduleinstalled(module):
        try:
            imp.find_module(module)
            return True
        except ImportError:
            print("module {} not installed".format(module))
            return False

def installmodulelist(modules):
    threads = []
    for module in modules:
        if not checkifmoduleinstalled(module):
            modulethread = threading.Thread(target=installpipmodule, args=(module,))
            threads.append(modulethread)

    # Start all threads
    if not threads == []:
        for thread in threads:
            thread.start()
        # Wait for all of them to finish
        for thread in threads:
            thread.join()



