import threading, os, sys, imp, shutil, json, subprocess
import modules.locations as locations
import modules.etags as etags

#archive handling
from zipfile import ZipFile

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

def getUpdatedSoftwareLinks(dicttopopulate):
	global filedict
	if not os.path.isdir(locations.jsoncachefolder):
		os.mkdir(locations.jsoncachefolder)
	for softwarechunk in dicttopopulate:
		githubjsonlink = softwarechunk["githubapi"]
		softwarename = softwarechunk["software"]
		projectname = get_project_from_github_api_link(githubjsonlink)

		try:
			file = filedict[projectname]
			#Exit reuse path if not yet downloaded
			if not file:
				raise HBUError('Not yet downloaded')
			softwarechunk["githubjson"] = file
			print("using already downloaded file for {}".format(projectname))
		#If not downloaded file yet
		except:
			jsonfile = os.path.join(locations.jsoncachefolder, projectname + ".json")

			#Download it, set the chunk's json file path to it, and update the filedict in case it's a shared file
			file = getJsonThread(githubjsonlink, jsonfile, softwarename)
			softwarechunk["githubjson"] = file
			filedict[projectname] = file

		#If project page was not pre-defined set it to the base github project link
		if softwarechunk["projectpage"] == None or softwarechunk["projectpage"] == "":
			softwarechunk["projectpage"] = parse_api_to_standard_github(githubjsonlink)

	dicttopopulate = sorted(dicttopopulate, key = lambda i: i["software"])
	return dicttopopulate

def getJsonThread(apiurl, jsonfile, softwarename):
	try:
		jfile = etags.accessETaggedFile(apiurl,jsonfile)
		if jfile:
			return jfile
		else:
			pass
	except Exception as e:
		print("getJson error - {}".format(e))

	if os.path.isfile(jsonfile):
		print("could not get updated link for {}, falling back on older version".format(softwarename))
		return jsonfile
	else:
		print("No fallback available, software will be unavailable")

def getJsonSoftwareLinks(dicttopopulate):

	if not os.path.isdir(locations.jsoncachefolder):
		os.mkdir(locations.jsoncachefolder)
	for softwarechunk in dicttopopulate:
		githubjsonlink = softwarechunk["githubapi"]
		softwarename = softwarechunk["githubapi"]
		projectname = get_project_from_github_api_link(githubjsonlink)

		jsonfile = os.path.join(locations.jsoncachefolder, projectname + ".json")
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
		jfile = etags.accessETaggedFile(apiurl,jsonfile)

		print("Downloaded new json file for {}".format(softwarename))
		return jfile
	except:
		print("failed to download json file for {}".format(softwarename))
		return None


def getrepochunkfromurl(url,description,):
	apiurl = webhandler.parse_standard_github_to_api(url)
	if apiurl == None:
		print("error parsing link")
		return
	print(apiurl)
	repo = apiurl.rsplit("/",2)[1]
	author = apiurl.rsplit("/",3)[1]

	jsonfile = webhandler.getJson(repo, apiurl)

	#make new entry
	chunk = {
			"software" : repo,
			"githuburl" : url,
			"githubapi" : apiurl,
			"githubjson" : jsonfile,
			"github_asset" : None,
			"author" : author,
			"projectpage" : None,
			"description" : description,
			"githubjson" : jsonfile,
			"photopath" : None,
			}
		
	# print(json.dumps(newentry,indent=4))

	return chunk


###URL Parsing
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

def get_project_from_github_api_link(url):
	remove = [
		"https:",
		"http:",
		"github.com",
		"releases",
		"api",
		"repos",
		".",
	]

	for r in remove:
		url = url.replace(r, "")

	url=url.strip("/")

	project_and_author = url.split('/')

	return project_and_author[1]






###Image handling
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

def getcachedimage(imagename):
	import os
	photopath = None

	#Optimizations >:)
	because_there_is_a_high_chance_its_png = os.path.join(locations.imagecachefolder,"{}.png".format(imagename))
	if os.path.isfile(because_there_is_a_high_chance_its_png):
		return because_there_is_a_high_chance_its_png

	for file in os.listdir(locations.imagecachefolder):
		strippedfile = file.strip(".jpeg").strip(".png").strip(".gif")
		if imagename == strippedfile:
			photopath = os.path.join(locations.imagecachefolder, file)
			break
	if photopath:
		if os.path.isfile(photopath):
			return photopath

	# photopath = imagename + ".png"
	# photopath = os.path.join(locations.imagecachefolder, photopath)
	# if os.path.isfile(photopath):
	# 	return photopath
	return False

def grabgravatar(user):
	base_gravatar = "http://de.gravatar.com/"
	user_json = "{}.json".format(user)
	gravatar_url = "{}{}".format(base_gravatar,user_json)
	tempdownloadedfile, headers = urllib.request.urlretrieve(gravatar_url)
	downloadsfolderlocation = os.path.join(locations.downloadsfolder,user_json)
	shutil.move(tempdownloadedfile, downloadsfolderlocation)
	with open(downloadsfolderlocation) as jsonfile:
		jfile = json.load(jsonfile)
		avatarurl = jfile["entry"][0]["thumbnailUrl"]
	return cacheimage(avatarurl,user)

def guessgithubavatar(author):
	imageurl = "https://avatars.githubusercontent.com/{}".format(author)
	try:
		image, headers = urllib.request.urlretrieve(imageurl)
		filename = headers["Content-Disposition"].split("filename=",1)[1]
		cachelocation = os.path.join(locations.imagecachefolder,filename)
		shutil.move(image, cachelocation)
		print("downloaded guessed avatar image {} for author {} from url {}".format(cachelocation, author, fileURL))
		return filename
	except Exception as e: 
		print("failed to find github avatar for author {}".format(author))
		return None





###Pip module handling
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
		try:
			reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list'])
			installed_packages = [r.decode().split(' ')[0] for r in reqs.split()]
			if module in installed_packages:
				found = True
		except:
			found = False

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




