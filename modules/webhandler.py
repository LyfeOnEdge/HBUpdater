import threading, os, sys, imp, shutil, json, subprocess
import modules.locations as locations

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
	except Exception as e: 
		print(e)
		print("Failed to download {}".format(filename))
		return False

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

def downloadFileAs(fileURL,filename):
	try:
		downloadlocation = os.path.join(locations.downloadsfolder,filename)
		urllib.request.urlretrieve(fileURL,downloadlocation)
		print("downloaded {} from url {}".format(filename, fileURL))
		return downloadlocation
	except Exception as e: 
		print(e)
		return None


def cacheimage(url,softwarename):
	try:
		with urllib.request.urlopen(url) as response:
			info = response.info()
			type=info.get_content_subtype()
			file = "{}.{}".format(softwarename,type)
			file = os.path.join(locations.imagecachefolder,file)
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
		jsonfile = os.path.join(locations.jsoncachefolder, softwarename + ".json")

		if softwarechunk["projectpage"] == None or softwarechunk["projectpage"] == "":
			softwarechunk["projectpage"] = parse_api_to_standard_github(githubjsonlink)

		getJsonThread(softwarename, githubjsonlink, jsonfile, softwarechunk)

	dicttopopulate = sorted(dicttopopulate, key = lambda i: i["software"])
	return dicttopopulate

def getJsonThread(softwarename, apiurl, jsonfile, softwarechunk):
	try:
		urllib.request.urlretrieve(apiurl,jsonfile)
		print("Downloaded new json file for {}".format(softwarename))
		softwarechunk["githubjson"] = jsonfile
		return jsonfile
	except Exception as e:
		print("getJson error - {}".format(e))
		if os.path.isfile(jsonfile):
				print("could not get updated link, falling back on older version")
				softwarechunk["githubjson"] = jsonfile
		else:
			print("No fallback available, software will be unavailable")

def getJsonSoftwareLinks(dicttopopulate):
	if not os.path.isdir(locations.jsoncachefolder):
		of.mkdir(locations.jsoncachefolder)
	for softwarechunk in dicttopopulate:
		githubjsonlink = softwarechunk["githubapi"]
		softwarename = softwarechunk["software"]

		jsonfile = os.path.join(locations.jsoncachefolder, softwarename + ".json")
		softwarechunk["githubjson"] = jsonfile
		print("using previously downloaded json file {}".format(jsonfile))

		if softwarechunk["projectpage"] == None or softwarechunk["projectpage"] == "":
			print("No project page found for {}, generating from github api link".format(softwarename))
			softwarechunk["projectpage"] = parse_api_to_standard_github(githubjsonlink)

	dicttopopulate = sorted(dicttopopulate, key = lambda i: i["software"])
	return dicttopopulate

def getJson(softwarename, apiurl):
	try:
		jsonfile = os.path.join(locations.jsoncachefolder, softwarename + ".json")
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

def parse_api_to_standard_github(url):
	remove = [
	"api.",
	"/releases",
	"/repos",
	]
	try:
		for item in remove:
			url = url.replace(item,"")
		return(url)
	except:
		return None

def grabgravatar(url):
	downloadedfile = urllib.request.urlretrieve(url)[0]
	dljsonfile = url.rsplit("/",1)[1]
	imagename = dljsonfile.rsplit(".",1)[0]
	downloadlocation = os.path.join(locations.downloadsfolder,dljsonfile)
	shutil.move(downloadedfile, downloadlocation)
	with open(downloadlocation) as jsonfile:
		jfile = json.load(jsonfile)
		avatarurl = jfile["entry"][0]["thumbnailUrl"]
	return cacheimage(avatarurl,imagename)

def getcachedimage(imagename):
		photopath = imagename + ".png"
		photopath = os.path.join(locations.imagecachefolder, photopath)
		photoexists = os.path.isfile(photopath)
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
	found = False
	try:
		imp.find_module(module)
		found = True
	except ImportError:
		found = False

	if not found: 
		reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list'])
		installed_packages = [r.decode().split(' ')[0] for r in reqs.split()]
		if module in installed_packages:
			found = True

	if not found:
		print("module {} not installed".format(module))
	return found

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



